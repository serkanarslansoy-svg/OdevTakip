#!/usr/bin/env python3
"""Argo DidUP Famiglia'daki "compiti assegnati" ve "promemoria" listelerini çekip
dersi uygulamadaki derse eşler ve Ödev Avcısı'nın Firebase veritabanına velinin
onay kutusuna (odevAvci/argoInbox) yazar. Metin çevrilmez, İtalyanca kalır.
Promemoria kayıtları kind="promemoria" ile yazılır; veli onaylarken Sınav ya da
Görev olarak ekler (verifica/interrogazione → Sınav önerilir). Notlar (voti)
odevAvci/argoGrades altına yazılır; uygulama bunları sınavlarla eşleyip veliye
"Notu Uygula" önerisi olarak gösterir.

GitHub Actions'ta zamanlanmış olarak çalışır (.github/workflows/argo-sync.yml).
Depo herkese açık olduğu için Actions kayıtları da herkese açıktır: bu betik
ödev metnini, ders adını ya da kişisel bilgiyi ASLA yazdırmaz; yalnızca sayılar
ve hata türü yazdırılır.

Gerekli ortam değişkenleri (GitHub Secrets):
  ARGO_SCUOLA, ARGO_USERNAME, ARGO_PASSWORD   -> Argo veli girişi
  FB_EMAIL, FB_PASSWORD                       -> Firebase aile hesabı
"""

from __future__ import annotations

import hashlib
import os
import re
import sys
from datetime import date, datetime, timedelta, timezone

import requests

FB_API_KEY = "AIzaSyDgmhNj0Rc3E5ZNx5Yg3uUh_rTHQIEGkBQ"
DB_URL = "https://odev-avcisi-35857-default-rtdb.us-central1.firebasedatabase.app"
ROOT = "odevAvci"

# Argo ders adı (büyük/küçük harf fark etmez) -> uygulamadaki ders anahtarı.
# Sıra önemli: "scienze motorie" "scienze"den önce gelmeli.
SUBJECT_RULES = [
    ("motori", "gym"), ("fisica", "gym"),
    ("matemat", "mat"), ("geometr", "mat"), ("aritmet", "mat"),
    ("italian", "ita"), ("lettere", "ita"),
    ("scienz", "sci"),
    ("storia", "sto"),
    ("geograf", "geo"),
    ("ingles", "ing"), ("english", "ing"),
    ("frances", "fra"), ("seconda lingua", "fra"),
    ("arte", "art"), ("immagine", "art"),
    ("musica", "mus"), ("strumento", "mus"),
    ("tecnolog", "tec"),
    ("religion", "rel"), ("alternativ", "rel"),
]
SUBJECT_TR = {
    "mat": "Matematik", "ita": "İtalyanca", "sci": "Fen Bilimleri", "sto": "Tarih",
    "geo": "Coğrafya", "ing": "İngilizce", "fra": "Fransızca", "art": "Görsel Sanatlar",
    "mus": "Müzik", "tec": "Teknoloji", "rel": "Din Kültürü", "gym": "Beden Eğitimi",
}


def log(msg: str) -> None:
    print(msg, flush=True)


def map_subject(materia: str) -> str:
    low = (materia or "").lower()
    for needle, key in SUBJECT_RULES:
        if needle in low:
            return key
    return ""


def parse_day(text: str) -> date | None:
    try:
        return date.fromisoformat((text or "")[:10])
    except ValueError:
        return None


def task_key(materia: str, due: str, text: str) -> str:
    raw = f"{materia.strip().lower()}|{due}|{' '.join(text.split()).lower()}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def guess_reward(text_it: str) -> tuple[int, str]:
    low = text_it.lower()
    if re.search(r"verifica|interrogazion|compito in classe|\btest\b", low):
        return 300, "boss"
    if re.search(r"\bportare\b|\bporta\b", low) and len(low) < 120:
        return 50, "normal"
    return 100, "normal"


EXAM_RE = re.compile(r"verific|interrogazi|compito in classe|\btest\b|\bprova\b|esame|simulazione", re.I)


def promemoria_kind(text_it: str) -> str:
    """Promemoria'nın önerilen türü: sınav mı, görev mi."""
    return "exam" if EXAM_RE.search(text_it or "") else "task"


def promemoria_key(day: str, text: str) -> str:
    raw = f"promemoria|{day}|{' '.join(text.split()).lower()}"
    return "p" + hashlib.sha1(raw.encode("utf-8")).hexdigest()[:15]


def clean_time(value: str) -> str:
    m = re.match(r"^\s*(\d{1,2}):(\d{2})", value or "")
    if not m or (m.group(1) in ("0", "00") and m.group(2) == "00"):
        return ""
    return f"{int(m.group(1)):02d}:{m.group(2)}"


def promemoria_subject(text: str, teacher_subjects: list[str]) -> str:
    """Önce metindeki ders adı; yoksa öğretmenin tek bir derse eşlenmesi. Belirsizse boş (veli seçer)."""
    from_text = map_subject(text)
    if from_text:
        return from_text
    keys = {k for k in (map_subject(m) for m in teacher_subjects) if k}
    return keys.pop() if len(keys) == 1 else ""


def short_title(subject: str, text: str) -> str:
    text = " ".join(text.split()).strip(" .:-")
    if len(text) > 48:
        text = text[:46].rsplit(" ", 1)[0] + "…"
    text = text[:1].upper() + text[1:]
    return f"{SUBJECT_TR[subject]}: {text}" if subject else text


# -------------------------------------------------------------- firebase ---
class Firebase:
    def __init__(self, email: str, password: str) -> None:
        r = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FB_API_KEY}",
            json={"email": email, "password": password, "returnSecureToken": True},
            timeout=30,
        )
        if r.status_code != 200:
            raise RuntimeError(f"Firebase girişi başarısız (HTTP {r.status_code})")
        self.token = r.json()["idToken"]

    def _url(self, path: str) -> str:
        return f"{DB_URL}/{ROOT}/{path}.json"

    def get(self, path: str, **params: str):
        r = requests.get(self._url(path), params={"auth": self.token, **params}, timeout=30)
        if r.status_code != 200:
            raise RuntimeError(f"Firebase okuma başarısız (HTTP {r.status_code})")
        return r.json()

    def patch(self, path: str, data: dict) -> None:
        r = requests.patch(self._url(path), params={"auth": self.token}, json=data, timeout=30)
        if r.status_code != 200:
            raise RuntimeError(f"Firebase yazma başarısız (HTTP {r.status_code})")

    def put(self, path: str, data) -> None:
        r = requests.put(self._url(path), params={"auth": self.token}, json=data, timeout=30)
        if r.status_code != 200:
            raise RuntimeError(f"Firebase yazma başarısız (HTTP {r.status_code})")


# ------------------------------------------------------------------ argo ---
# Ekim 2026'dan beri Argo, consent adımından sonra doğrudan yönlendirmek yerine bir
# "onay ekranı" (TRAS-1928) gösteriyor: HTTP 200 sayfa, içinde data-auth-app-redirect
# bağlantısı var; tarayıcı bunu JavaScript ile otomatik açıyor. Kütüphane yalnızca
# Location başlığını izlediği için orada duruyordu. Bu sayfayı yakalayıp bağlantısını
# normal bir 302 yönlendirmesine çeviriyoruz. Sayfa yapısını da hata teşhisi için tutuyoruz.
_CONSENT_HTML: list[str] = []
_CONSENT_HOPS: list[str] = []


def consent_redirect_target(page: str) -> str | None:
    """Onay ekranındaki [data-auth-app-redirect] bağlantısının href'i (HTML çözülmüş)."""
    from html.parser import HTMLParser

    found: list[str] = []

    class P(HTMLParser):
        def handle_starttag(self, tag, attrs):  # type: ignore[no-untyped-def]
            a = dict(attrs)
            if "data-auth-app-redirect" in a and (a.get("href") or "").strip():
                found.append(a["href"].strip())

    try:
        P().feed(page)
    except Exception:  # noqa: BLE001
        pass
    return found[0] if found else None


def _capture_consent_pages() -> None:
    """httpx yanıtlarında /auth/sso/consent sayfasını yakalar; onay ekranıysa 302'ye çevirir."""
    import httpx

    if getattr(httpx.AsyncClient.send, "_odev_patched", False):
        return
    original = httpx.AsyncClient.send
    drop = {"content-length", "content-encoding", "transfer-encoding", "content-type", "location"}

    async def send(self, request, *args, **kwargs):  # type: ignore[no-untyped-def]
        resp = await original(self, request, *args, **kwargs)
        try:
            if "/auth/sso/consent" in request.url.path:
                await resp.aread()
                _CONSENT_HTML.append(resp.text[:200000])
                if resp.status_code == 200:
                    target = consent_redirect_target(resp.text)
                    if target:
                        target = str(request.url.join(target))
                        headers = [(k, v) for k, v in resp.headers.multi_items() if k.lower() not in drop]
                        headers.append(("location", target))
                        _CONSENT_HOPS.append(target.split("?")[0])
                        await resp.aclose()
                        return httpx.Response(302, headers=headers, request=request)
        except Exception:  # noqa: BLE001
            pass
        return resp

    send._odev_patched = True  # type: ignore[attr-defined]
    httpx.AsyncClient.send = send  # type: ignore[method-assign]


def describe_consent_page() -> str:
    """Consent sayfasının yalnızca yapısı: başlık, form hedefi (sorgusuz), alan adları/türleri,
    düğme etiketleri ve birkaç anahtar kelimenin var/yok bilgisi. Hiçbir alan DEĞERİ ve
    serbest metin (ad-soyad olabilir) yazılmaz."""
    if not _CONSENT_HTML:
        return "consent sayfası yakalanamadı"
    from html.parser import HTMLParser

    page = _CONSENT_HTML[-1]

    class P(HTMLParser):
        def __init__(self) -> None:
            super().__init__()
            self.title, self.in_title, self.in_button = "", False, False
            self.forms: list[dict] = []
            self.scripts = 0

        def handle_starttag(self, tag, attrs):  # type: ignore[no-untyped-def]
            a = dict(attrs)
            if tag == "title":
                self.in_title = True
            elif tag == "script":
                self.scripts += 1
            elif tag == "form":
                act = (a.get("action") or "").split("?")[0]
                self.forms.append({"method": (a.get("method") or "get").lower(), "action": act, "fields": []})
            elif tag in ("input", "select", "textarea") and self.forms:
                t = (a.get("type") or tag).lower()
                f = {"name": a.get("name", ""), "type": t}
                if t in ("submit", "button") and a.get("value") and len(a.get("value", "")) <= 30:
                    f["label"] = a["value"]
                if t == "checkbox":
                    f["checked"] = "checked" in a
                self.forms[-1]["fields"].append(f)
            elif tag == "button" and self.forms:
                self.in_button = True
                self.forms[-1]["fields"].append({"name": a.get("name", ""), "type": "button",
                                                 "value": (a.get("value") or "")[:30], "label": ""})

        def handle_endtag(self, tag):  # type: ignore[no-untyped-def]
            if tag == "title":
                self.in_title = False
            elif tag == "button":
                self.in_button = False

        def handle_data(self, data):  # type: ignore[no-untyped-def]
            if self.in_title:
                self.title += data.strip()
            elif self.in_button and self.forms:
                self.forms[-1]["fields"][-1]["label"] = (self.forms[-1]["fields"][-1]["label"] + " " + data.strip()).strip()[:30]

    p = P()
    try:
        p.feed(page)
    except Exception:  # noqa: BLE001
        pass
    low = page.lower()
    words = [w for w in ("privacy", "consenso", "autorizz", "accett", "condizion", "termini", "informativa",
                         "rifiut", "grant_scope", "window.location", "submit()", "http-equiv=\"refresh\"") if w in low]
    # Argo hata sayfasıysa teknik nedeni (OAuth hata açıklaması) al; kişisel veri içermez.
    detail = ""
    m = re.search(r'id="collapseOne"[^>]*>(.*?)</div>', page, re.S)
    if m:
        import html as _html
        detail = " ".join(_html.unescape(re.sub(r"<[^>]+>", " ", m.group(1))).split())
        detail = re.sub(r"https?://\S+", lambda x: x.group(0).split("?")[0], detail)[:300]
    is_error = "auth-error" in page or "Error Id" in page
    import json as _json
    return "consent sayfası yapısı: " + _json.dumps({"title": p.title[:60], "forms": p.forms, "scripts": p.scripts,
                                                     "keywords": words, "length": len(page),
                                                     "argo_hata_sayfasi": is_error, "hata_detayi": detail,
                                                     "onay_ekrani_baglantisi": consent_redirect_target(page) is not None,
                                                     "izlenen_onay_hoplari": _CONSENT_HOPS},
                                                    ensure_ascii=False)


def fetch_argo(scuola: str, user: str, password: str) -> tuple[list[dict], list[dict] | None, list | None]:
    """(ödevler, promemoria, notlar). Promemoria/notlar alınamazsa None döner; ödevler yine yazılır."""
    from didupwrapper import DiDUPClientSync

    _capture_consent_pages()

    items: list[dict] = []
    notes: list[dict] | None = None
    grades: list | None = None
    # Öğretmen -> verdiği dersler (promemoria'da ders alanı yok, öğretmenden çıkarıyoruz).
    teacher_subjects: dict[str, set[str]] = {}
    with DiDUPClientSync(scuola, user, password, auto_versione=True) as didup:
        for lezione in didup.get_registro():
            for tkey in (lezione.pk_docente, " ".join((lezione.docente or "").split()).lower()):
                if tkey and lezione.materia:
                    teacher_subjects.setdefault(tkey, set()).add(lezione.materia)
            for compito in lezione.compiti:
                text = " ".join((compito.compito or "").split())
                due = parse_day(compito.data_consegna)
                if not text or due is None:
                    continue
                items.append({
                    "materia": lezione.materia or "",
                    "assigned": (lezione.dat_giorno or "")[:10],
                    "due": due,
                    "text": text,
                })
        try:
            notes = []
            for p in didup.get_promemoria():
                if not p.flg_visibile_famiglia:
                    continue
                text = " ".join((p.des_annotazioni or "").split())
                day = parse_day(p.dat_giorno)
                if not text or day is None:
                    continue
                subs = teacher_subjects.get(p.pk_docente) or teacher_subjects.get(
                    " ".join((p.docente or "").split()).lower()) or set()
                notes.append({"day": day, "text": text, "subjects": sorted(subs),
                              "time": clean_time(p.ora_inizio)})
        except Exception as exc:  # noqa: BLE001 - ödevler yine de yazılsın
            log(f"Promemoria alınamadı: {type(exc).__name__}")
            notes = None
        try:
            grades = list(didup.get_voti())
        except Exception as exc:  # noqa: BLE001
            log(f"Notlar alınamadı: {type(exc).__name__}")
            grades = None
    return items, notes, grades


def build_entries(items: list[dict], known: set[str], today: date, now_iso: str) -> tuple[dict, dict]:
    """Yeni ödevleri onay kutusu kayıtlarına çevirir (çeviri hariç)."""
    entries: dict[str, dict] = {}
    for it in items:
        if it["due"] < today - timedelta(days=1):
            continue  # eski ödevleri getirme
        key = task_key(it["materia"], it["due"].isoformat(), it["text"])
        if key in known or key in entries:
            continue
        subject = map_subject(it["materia"])
        xp, difficulty = guess_reward(it["text"])
        entries[key] = {
            "id": key,
            "subject": subject,
            "subjectIt": it["materia"],
            "descIt": it["text"],
            "dueDate": it["due"].isoformat(),
            "assignedDate": it["assigned"],
            "xp": xp,
            "difficulty": difficulty,
            "createdAt": now_iso,
        }
    seen = {k: today.isoformat() for k in entries}
    return entries, seen


def build_promemoria_entries(notes: list[dict], known: set[str], today: date, now_iso: str) -> dict:
    """Yeni promemoria kayıtlarını onay kutusu kayıtlarına çevirir (kind="promemoria")."""
    entries: dict[str, dict] = {}
    for n in notes:
        if n["day"] < today - timedelta(days=1):
            continue  # geçmiş hatırlatmaları getirme
        key = promemoria_key(n["day"].isoformat(), n["text"])
        if key in known or key in entries:
            continue
        kind = promemoria_kind(n["text"])
        subject = promemoria_subject(n["text"], n["subjects"])
        entries[key] = {
            "id": key,
            "kind": "promemoria",
            "suggest": kind,
            "subject": subject,
            "subjectIt": " / ".join(n["subjects"])[:80],
            "descIt": n["text"],
            "dueDate": n["day"].isoformat(),
            "time": n["time"],
            "xp": 300 if kind == "exam" else 50,
            "difficulty": "boss" if kind == "exam" else "normal",
            "createdAt": now_iso,
        }
    return entries


def build_grades(voti: list, today: date) -> dict:
    """Argo notlarını uygulamanın okuyacağı biçime çevirir (yalnızca sayısal notlar, son 150 gün)."""
    out: dict[str, dict] = {}
    for v in voti:
        value = getattr(v, "valore", None)
        day = parse_day(getattr(v, "dat_giorno", ""))
        if value is None or day is None or day < today - timedelta(days=150):
            continue
        try:
            value = round(float(value), 2)
        except (TypeError, ValueError):
            continue
        if not 0 <= value <= 10:
            continue
        materia = " ".join((v.des_materia or "").split())
        kind = (v.cod_voto_pratico or "").strip().upper()[:1]
        prg = v.prg_voto if v.prg_voto is not None else v.cod_codice
        raw = f"{day.isoformat()}|{v.pk_materia or materia.lower()}|{prg}|{kind}"
        key = "g" + hashlib.sha1(raw.encode("utf-8")).hexdigest()[:15]
        out[key] = {
            "id": key,
            "date": day.isoformat(),
            "subject": map_subject(materia),
            "subjectIt": materia[:60],
            "value": value,
            "code": (v.cod_codice or "").strip()[:8],
            "kind": kind,  # S = scritto (yazılı), N = orale (sözlü), P = pratico
            "desc": " ".join((v.descrizione_prova or "").split())[:120],
            "comment": " ".join((v.des_commento or "").split())[:200],
        }
    return out


def describe_error(exc: Exception) -> str:
    """Hatanın türü + kütüphanenin kısa açıklaması (ör. 'credenziali errate').

    Yalnızca kütüphanenin kendi mesajı ve HTTP kodu kullanılır; istek adresi,
    sunucu yanıtı (payload) ve sorgu parametreleri herkese açık kayda yazılmaz.
    """
    kind = type(exc).__name__
    msg = str(getattr(exc, "message", "") or "")
    msg = re.sub(r"https?://\S+", lambda m: m.group(0).split("?")[0], msg)  # adreslerden sorguyu at
    msg = " ".join(msg.split())[:160]
    code = getattr(exc, "status_code", None)
    out = kind + (f": {msg}" if msg else "")
    return out + (f" (HTTP {code})" if code else "")


def main() -> int:
    env = {k: os.environ.get(k, "").strip() for k in
           ("ARGO_SCUOLA", "ARGO_USERNAME", "ARGO_PASSWORD", "FB_EMAIL", "FB_PASSWORD")}
    missing = [k for k, v in env.items() if not v]
    if missing:
        log("Eksik GitHub Secrets: " + ", ".join(missing))
        return 1

    now = datetime.now(timezone.utc)
    now_iso = now.isoformat(timespec="seconds")
    today = now.date()

    fb = Firebase(env["FB_EMAIL"], env["FB_PASSWORD"])
    try:
        items, notes, voti = fetch_argo(env["ARGO_SCUOLA"], env["ARGO_USERNAME"], env["ARGO_PASSWORD"])
    except Exception as exc:  # noqa: BLE001 - ayrıntı herkese açık kayda düşmesin
        kind = describe_error(exc)
        fb.put("argoLastSync", {"at": now_iso, "ok": False, "error": kind})
        log(f"Argo'dan ödevler alınamadı: {kind}")
        if "consent" in kind:
            log(describe_consent_page())
        return 1
    log(f"Argo'da {len(items)} ödev kaydı bulundu.")
    if notes is not None:
        log(f"Argo'da {len(notes)} promemoria kaydı bulundu.")
    grades = build_grades(voti, today) if voti is not None else None
    if grades is not None:
        log(f"Argo'da {len(grades)} not bulundu (son 150 gün).")

    seen = fb.get("argoSeen", shallow="true") or {}
    inbox = fb.get("argoInbox", shallow="true") or {}
    known = set(seen) | set(inbox)
    entries, new_seen = build_entries(items, known, today, now_iso)
    p_entries = build_promemoria_entries(notes or [], known, today, now_iso)
    new_seen.update({k: today.isoformat() for k in p_entries})

    all_entries = {**entries, **p_entries}
    if all_entries:
        for e in all_entries.values():
            e["title"] = short_title(e["subject"], e["descIt"])
        fb.patch("argoInbox", all_entries)
        fb.patch("argoSeen", new_seen)

    status = {"at": now_iso, "ok": True, "added": len(entries), "found": len(items),
              "addedReminders": len(p_entries)}
    if notes is None:
        status["reminderError"] = True
    if grades is not None:
        fb.put("argoGrades", grades)
        status["grades"] = len(grades)
    else:
        status["gradeError"] = True
    fb.put("argoLastSync", status)
    log(f"Onay kutusuna {len(entries)} yeni ödev, {len(p_entries)} yeni promemoria eklendi.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RuntimeError as exc:  # kendi mesajlarımız: gizli bilgi içermez
        log(f"Senkron başarısız: {exc}")
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        log(f"Senkron başarısız: {type(exc).__name__}")
        sys.exit(1)
