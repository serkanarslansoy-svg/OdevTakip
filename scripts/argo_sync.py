#!/usr/bin/env python3
"""Argo DidUP Famiglia'daki "compiti assegnati" listesini çekip Türkçeye
çevirir ve Ödev Avcısı'nın Firebase veritabanına velinin onay kutusuna
(odevAvci/argoInbox) yazar.

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
import time
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


# ---------------------------------------------------------------- çeviri ---
def translate(texts: list[str]) -> list[str | None]:
    """İtalyanca -> Türkçe (ücretsiz Google çevirisi, olmazsa MyMemory)."""
    out: list[str | None] = [None] * len(texts)
    try:
        from deep_translator import GoogleTranslator
        gt = GoogleTranslator(source="it", target="tr")
        for i, t in enumerate(texts):
            try:
                out[i] = gt.translate(t) or None
            except Exception:  # noqa: BLE001 - tek metin başarısız olabilir
                out[i] = None
            time.sleep(0.3)
    except Exception:  # noqa: BLE001
        pass
    missing = [i for i, v in enumerate(out) if not v]
    if missing:
        try:
            from deep_translator import MyMemoryTranslator
            mm = MyMemoryTranslator(source="it-IT", target="tr-TR")
            for i in missing:
                try:
                    out[i] = mm.translate(texts[i][:450]) or None
                except Exception:  # noqa: BLE001
                    out[i] = None
                time.sleep(0.5)
        except Exception:  # noqa: BLE001
            pass
    return out


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
def fetch_homework(scuola: str, user: str, password: str) -> list[dict]:
    from didupwrapper import DiDUPClientSync

    items: list[dict] = []
    with DiDUPClientSync(scuola, user, password, auto_versione=True) as didup:
        for lezione in didup.get_registro():
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
    return items


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
        items = fetch_homework(env["ARGO_SCUOLA"], env["ARGO_USERNAME"], env["ARGO_PASSWORD"])
    except Exception as exc:  # noqa: BLE001 - ayrıntı herkese açık kayda düşmesin
        kind = type(exc).__name__
        fb.put("argoLastSync", {"at": now_iso, "ok": False, "error": kind})
        log(f"Argo'dan ödevler alınamadı: {kind}")
        return 1
    log(f"Argo'da {len(items)} ödev kaydı bulundu.")

    seen = fb.get("argoSeen", shallow="true") or {}
    inbox = fb.get("argoInbox", shallow="true") or {}
    known = set(seen) | set(inbox)
    entries, new_seen = build_entries(items, known, today, now_iso)

    if entries:
        keys = list(entries)
        translated = translate([entries[k]["descIt"] for k in keys])
        for k, tr in zip(keys, translated):
            e = entries[k]
            e["translated"] = bool(tr)
            e["descTr"] = tr or e["descIt"]
            e["titleTr"] = short_title(e["subject"], e["descTr"])
        fb.patch("argoInbox", entries)
        fb.patch("argoSeen", new_seen)

    fb.put("argoLastSync", {"at": now_iso, "ok": True, "added": len(entries), "found": len(items)})
    log(f"Onay kutusuna {len(entries)} yeni ödev eklendi.")
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
