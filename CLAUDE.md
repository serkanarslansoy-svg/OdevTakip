# CLAUDE.md — Ödev Avcısı (OdevTakip) proje hafızası

> **Bu dosya projenin kalıcı hafızasıdır.** Claude hesabı, oturumu ya da modeli değişse bile
> bu depoda çalışan her Claude önce bu dosyayı okumalı ve buradaki kurallara uymalıdır.
> Önemli bir değişiklik yaptığında **bu dosyayı da güncelle** (özellikle §11 Değişiklik Günlüğü
> ve §12 Açık İşler). Kod ile bu dosya çelişirse kod doğrudur; dosyayı düzelt.
>
> Depo **herkese açıktır** (GitHub Pages için). Bu dosyaya ve depoya **asla** şifre, token,
> okul kodu, Argo kullanıcı adı, e-posta, Firebase aile UID'si gibi gizli/kişisel bilgi yazma.

**For AI assistants (English summary):** This repo is "Ödev Avcısı", a gamified homework/exam
tracker that a Turkish-speaking parent built for his son ("Ruz"), who attends an Italian middle
school. The whole app is one file, `index.html` (vanilla JS, Tailwind CDN, Firebase Realtime DB
sync), served by GitHub Pages. `scripts/argo_sync.py`, run by GitHub Actions, pulls homework,
teacher reminders (promemoria) and grades from the school's Argo DidUP system into Firebase for
parent approval. The user is not a developer: **reply in Turkish**, keep it simple, **push every
change directly to `main`** (no branches or PRs), test in a browser before pushing, and never write
secrets into this public repo. Everything below is in Turkish. Start with §0.1.

---

## 0.1 Yeni Oturuma Başlarken (ilk iş bunları yap)

1. **Doğru depoda mısın?** Proje deposu: `serkanarslansoy-svg/OdevTakip`
   (https://github.com/serkanarslansoy-svg/OdevTakip). Oturum başka bir depoda açıldıysa bu depoyu
   oturuma ekle (Claude Code web'de `add_repo`) ve klonla:
   `git clone https://github.com/serkanarslansoy-svg/OdevTakip`. Sonra `git pull origin main`.
2. **Bu dosyayı baştan sona oku**, sonra gerekiyorsa `KURULUM.md`'ye bak (kullanıcının gördüğü rehber).
3. **Son durumu kontrol et:**
   - `git log --oneline -15` → son yapılanlar (commit mesajları Türkçe ve açıklayıcı).
   - Argo senkronu çalışıyor mu? (§7.6 adım 1–2). Son çalışmalar başarısızsa kullanıcı muhtemelen
     "senkron çalışmıyor" diyecek; önceden bak.
   - Canlı site açılıyor mu: https://serkanarslansoy-svg.github.io/OdevTakip/
4. **§12 Açık İşler**'e bak: kullanıcıya önceden önerilip cevap beklenen şeyler orada.
5. Kullanıcı ekran görüntüsüyle gelirse: görüntü uygulamanın bir ekranıdır (koyu tema, neon yeşil).
   Hangi ekran olduğunu §3.2'deki ekran listesinden bul; Türkçe etiketler doğrudan koddaki
   metinlerle aranabilir (`grep -n "Etiket" index.html`).
6. İş bitince: test (§8) → commit (Türkçe) → `git push origin main` → yayını doğrula (§8.4) →
   bu dosyayı güncelle (§13) → kullanıcıya Türkçe, kısa özet.

## 0.2 Sözlük (Türkçe / İtalyanca terimler)

| Terim | Anlamı |
|---|---|
| Veli / Komutan | Ebeveyn (baba); uygulamada yönetici rol, PIN ile girer. |
| Öğrenci / Ruz | Çocuk; görevleri yapan, XP/altın kazanan rol. |
| Görev / Ödev | Task. Uygulamada her ödev bir "görev"dir. |
| Sınav / Boss / Boss Savaşı | Exam; önemli sınav "Boss" (daha çok XP, rozet). |
| XP, Altın (🪙), Seviye, Seri, Rozet | Oyun puanı, ödül mağazası parası, level, ardışık gün, başarım. |
| Yapılmadı | Süresi geçmiş, yapılmamış görev (`status:'missed'`, XP cezası). |
| Onay bekliyor | Öğrenci "bitti" dedi, veli onayı bekleniyor (`status:'pending'`). |
| Panel, Görev Ata, Planla, Ödül, Ayarlar | Veli ekranları. |
| Görevler, Dersler, Takvim, Program, Sınavlar, Ödüller | Öğrenci ekranları. |
| Kelime Avı | Günlük İtalyanca→Türkçe kelime oyunu. |
| Argo / DidUP / portaleargo | Okulun elektronik kayıt sistemi (İtalya). |
| compiti assegnati | (İt.) Verilen ödevler. |
| promemoria | (İt.) Öğretmen hatırlatması (sınav duyurusu, "şunu getir" vb.). |
| voti | (İt.) Notlar. scritto = yazılı (S), orale = sözlü (N), pratico = uygulama (P). |
| verifica / interrogazione | (İt.) Yazılı sınav / sözlü sınav. |
| Terza Media | (İt.) Ortaokul 3. sınıf. |
| BES / DSA | (İt.) Özel eğitim ihtiyacı olan öğrenciler (ödev metinlerinde geçer). |

---

## 0. Kısa Özet

- **Ne:** Bir velinin (babanın) İtalya'da ortaokul 3. sınıfta (Terza Media) okuyan oğlu **Ruz**
  için yaptığı, oyunlaştırılmış ödev/sınav takip uygulaması. Arayüz **Türkçe**.
- **Nerede:** Tek dosya `index.html` → GitHub Pages: https://serkanarslansoy-svg.github.io/OdevTakip/
  Android uygulaması (Capacitor) bu adresi uzaktan açar; HTML değişikliği için APK gerekmez.
- **Veri:** Tarayıcıda `localStorage` + iki cihaz arası **Firebase Realtime Database** senkronu.
- **Okul entegrasyonu:** Okulun **Argo DidUP** sisteminden ödev / promemoria / notlar,
  GitHub Actions (`.github/workflows/argo-sync.yml` + `scripts/argo_sync.py`) ile günde 4 kez
  çekilir ve **veli onayına** düşer.
- **İki rol:** Öğrenci (Ruz) ve Veli ("Komutan", PIN ile). Veliye özel her işlem
  `ui.role === 'parent'` kontrolüyle korunur.

---

## 1. Kullanıcı ve Çalışma Kuralları (EN ÖNEMLİ BÖLÜM)

### 1.1 Kullanıcı hakkında
- Kullanıcı **veli**dir, yazılımcı değildir. **Türkçe** konuş; kısa, net, teknik olmayan dille
  anlat. Genelde telefondan ekran görüntüsü gönderir; mesajları kısadır ("Yap", "Pushla",
  "Oldu mu", "Bi bakar mısın").
- "Yap" / "Pushla" = hemen uygula ve yayınla. Gereksiz soru sorma; makul varsayımla ilerle,
  varsayımı cevapta tek cümleyle söyle.
- Bir şey "çalışmıyor" derse: önce kanıt topla (Actions kayıtları, canlı site, kod), kök nedeni
  bul, düzelt, gerçekten çalıştığını doğrula, sonra sade bir dille anlat.

### 1.2 Git / yayın kuralları
- **Bütün güncellemeler doğrudan `main` dalına push edilir.** Kullanıcının açık talimatı:
  *"Hayır bütün güncellemeler main e"*. Dal açma, PR açma (kullanıcı ayrıca istemedikçe).
- Düzenlemeden önce **her zaman** `git pull origin main` yap (bkz. §10 "Freebuff olayı").
- Commit mesajları **Türkçe**: kısa başlık + madde madde açıklama (ne, neden). Commit/PR/kod
  içine model adı yazma.
- `scripts/__pycache__/*.pyc` depoda izleniyor (eski hata). **Commit'leme:** commit öncesi
  `git checkout -- scripts/__pycache__` çalıştır, sadece ilgili dosyaları `git add` et.
- Push sonrası GitHub Pages yayınını bekle ("pages build and deployment" çalışması) ve canlı
  sitede yeni kodun olduğunu doğrula (bkz. §8.4). Kullanıcıya "uygulamayı kapatıp aç" de;
  Pages önbelleği `max-age=600` olduğundan birkaç dakika sürebilir.
- Kullanıcıya yönelik rehber **`KURULUM.md`**'dir (Türkçe). Kullanıcının göreceği bir özellik
  değişirse KURULUM.md'yi de güncelle.

### 1.3 Güvenlik ve gizlilik kuralları
- Depo ve **Actions kayıtları herkese açık.** `scripts/argo_sync.py` hiçbir zaman ödev metni,
  ders adı, not, öğretmen adı, kişisel bilgi **yazdırmaz**; yalnızca sayılar ve hata türü
  yazdırır. Yeni log satırı eklerken bu kurala uy.
- Gizli bilgiler yalnızca **GitHub Secrets**'ta: `ARGO_SCUOLA`, `ARGO_USERNAME`,
  `ARGO_PASSWORD`, `FB_EMAIL`, `FB_PASSWORD`. Asla koda/dosyaya/sohbete geri yazma.
- "Şimdi Senkronize Et" için GitHub token'ı yalnızca cihazın `localStorage`'ında
  (`odevAvciGhTokenV1`) durur; state'e/buluta yazılmaz.
- Kullanıcı geçmişte Argo şifresini sohbette paylaştı; değiştirmesi önerildi. Şifreyi tekrar etme.
- Firebase Web API anahtarı gizli değildir (kodda açık); erişim **Firebase kurallarıyla**
  korunur (§6.3).
- Oturum ortamının güvenlik kısıtları (önceki oturumlarda reddedildi, tekrar deneme):
  - Firebase'i aile kimlik bilgileriyle doğrudan okumak/yazmak (REST ile) → yapma.
  - `didupwrapper` kütüphanesini yerelde kurup gerçek Argo'ya bağlanmak → yapma. Test için
    sahte (fake) modül kullan (§8.2). Gerçek bağlantı yalnızca GitHub Actions'ta.

### 1.4 Ürün kararları (kullanıcının açıkça istedikleri — geri alma)
- **Argo ödev metni Türkçeye çevrilmez**, İtalyanca kalır; sadece **ders** eşlenir.
- Argo'dan gelen her şey (ödev, promemoria, not) **veli onayına** düşer; otomatik eklenmez.
- **Kelime Avı İtalyanca**dır (İngilizce değil): İtalyanca kelime → Türkçe karşılık.
- Görevlerde **saat yok**, sadece **teslim günü** (gün sonunda 23:59'da dolar).
- **PDF indirme yalnızca veli**de; sadece **devam eden** (aktif, süresi geçmemiş) ödevler,
  tek sayfa (en fazla ~20 ödev).
- Geriye dönük sınav ve not girişi **sadece veli**.
- Veli Panelinden kaldırılanlar: Tamamlananlar listesi, "Yapılmayan Görevler" kartı
  (`missedPanelCard` kodda duruyor ama kullanılmıyor), "Hızlı Görev Şablonları".
- Yapılmadı (missed) görevler **kırmızı** görünür ve kendi sekmesi vardır.
- Ders seçimleri **açılır liste** (`subjectSelect`) — yatay kayan çipler değil.
- Alt menü 6 sekme; telefonda 7.'ye yer yok → yeni bölümler kart içi sekme olarak eklenir
  (ör. Argo kartındaki Ödevler | Promemoria | Notlar).

---

## 2. Depo Yapısı

| Yol | Açıklama |
|---|---|
| `index.html` | **Tüm uygulama** (~3400 satır): HTML + Tailwind CDN + tek `<script>`. |
| `scripts/argo_sync.py` | Argo → Firebase senkron betiği (GitHub Actions'ta çalışır). |
| `.github/workflows/argo-sync.yml` | Cron `7 5,12,15,18 * * *` (UTC) + elle `workflow_dispatch`. |
| `.github/workflows/build-apk.yml` | Capacitor Android debug APK (yalnızca paket/config değişince). |
| `capacitor.config.js`, `package.json` | Android sarmalayıcı; `server.url` = Pages adresi. |
| `database.rules.json` | Firebase kuralları **şablonu** (`AILE_UID` yer tutucu; gerçek UID konsolda). |
| `KURULUM.md` | Kullanıcı rehberi (Türkçe). |
| `CLAUDE.md` | Bu dosya. |
| `cyberquest_scholar/DESIGN.md` | Tasarım sistemi (renk token'ları; koyu tema, neon yeşil/turuncu). |
| `ana_g_rev_ss/`, `dersler_devler/`, `s_nav_*`, `dev_ata_veli_modu/` vb. | İlk tasarım taslakları (code.html + screen.png). Uygulama bunları **kullanmaz**. |
| `.freebuff/project-id` | Eski bir yapay zekâ aracının izi (bkz. §10). |

---

## 3. Uygulama Mimarisi (`index.html`)

### 3.1 Teknoloji
- Vanilla JS, derleme yok. Tailwind **CDN** (`cdn.tailwindcss.com`, `line-clamp-*` vb. var),
  Material Symbols ikon fontu, Firebase **compat** SDK (app/database/auth, gstatic'ten),
  html2pdf.js 0.10.1 (cdnjs, **yalnızca PDF anında** `loadScriptOnce` ile yüklenir).
- Renkler Tailwind teması olarak tanımlı (`primary-container` = neon yeşil `#00ff88`,
  `secondary-container` = turuncu `#fe6b00`, `tertiary-fixed-dim`, `error` …). Hazır sınıflar:
  `card`, `inp`, `lbl`, `btn-green`, `btn-orange`, `btn-ghost`.
- iPhone çentiği: `#main` üst/alt boşluğu `env(safe-area-inset-top/bottom)` içerir.
- PWA manifest JS ile üretilir. `trUpper()` Türkçe büyük harf düzeltmesi yapar (CSS
  `uppercase` "i"yi "I" yapıyordu).

### 3.2 Kod bölümleri (sırayla) ve önemli fonksiyonlar
- **Yardımcılar:** `$`, `$$`, `esc` (**kullanıcı/Argo metnini HTML'e koymadan önce mutlaka
  `esc()`**), `uid`, `nf` (tr-TR sayı), `sha256Hex`, `hashPin`, `ymd` (yerel tarih
  `YYYY-MM-DD`), `todayStr`, `addDays`, `fmtDateTR`, `taskDue`, `fmtDue`, `isOverdue`,
  `taskGold`, `SUBJECTS`.
- **Varsayılan veri:** `realSchedule`, `realTasks`, `realExams`, `seedState` (ilk kurulum).
- **Durum:** `LS_KEY='odevAvciStateV1'`, `LS_UI='odevAvciUIV1'`, `loadState`, `migrate`,
  `loadUI/saveUI`, `save()` (localStorage + `fbPush`).
- **Firebase senkron:** `DEFAULT_FIREBASE_CONFIG`, `FB`, `stableJSON`, `fbDiff`, `applyPaths`,
  `fbPush`, `fbOnValue`, `fbListen`, `fbConnect`, `fbSignIn/fbSignOut`, `copyUid`.
- **Oyun:** `LEVEL_THRESHOLDS`, `LEVEL_TITLES`, `levelOf`, `goldForXp`, `BADGES`,
  `checkBadges`, `pruneBadges`, `addHistory/removeHistory`, `streakResetDay`, `recalcStreak`,
  `currentStreak`, `weekPenalty`, `weekStats`.
- **Ses/Bildirim:** `beep`, `askNotify`, `notifyExam`, `checkAlarms`.
- **Modallar:** `toast`, `askConfirm(title, msg, onOk, okLabel)`, `askPin`,
  `openDetail(html)` / `closeDetail()` (alt sayfa; formlar burada açılır).
- **Navigasyon:** `STUDENT_NAV` (Görevler, Dersler, Takvim, Program, Sınavlar, Ödüller),
  `PARENT_NAV` (Panel, Görev Ata, Takvim, Planla, Ödül, Ayarlar), `switchRole`, `showView`,
  `renderAll()` (aktif görünümü yeniden çizer; ekranlar `$('#main').innerHTML = ...`).
- **Ortak parçalar:** `subjectChip`, `xpBadge`, `statusChip`, `taskCard`, `openTaskDetail`,
  `nextExam`, `bossAlarmCard`, `renderHeader`, `renderNav`.
- **Öğrenci ekranları:** `renderHome` (Hero, Boss alarmı, `missedStudentCard`, `vocabCard`,
  bugünün görevleri), `renderDersler` (+ `statusTabs` Devam/Bitti/Yapılmadı/Tümü),
  `renderCalendar` (+ `calTaskRow`, `calExamRow`), `renderProgram` (+ `weekGrid`,
  `openSchedDetail`), `renderSinavlar`, `renderOduller`.
- **Kelime Avı:** `VOCAB` (≈270 "italyanca=türkçe" çifti, `|` ile ayrılmış tek string;
  nesnelerde alan adı tarihsel olarak `en` = İtalyanca, `tr` = Türkçe), `vocabQuestions`,
  `vocabCard`, `vocabOpen`, `vocabAnswer`, `vocabResult`, `vocabReward`.
- **Argo (uygulama tarafı):** bkz. §7.5.
- **Veli ekranları:** `renderPanel` (Argo kartı, `statsCard` XP/altın, onaylar, hızlı erişim +
  PDF, durum özeti), `renderGorev` (Görev Ata: form, toplu ekleme, liste + filtre),
  `renderPlanla` (sınav ekle, tüm sınavlar, haftalık program yönetimi), `renderOdulmgr`,
  `renderAyarlar` (PIN, bildirim, Firebase, Aile hesabı, Argo, yedek).
- **Görev işlemleri:** `submitTask`, `bulkParse/bulkAdd` (toplu ekleme), `openTaskEditor` /
  `saveTaskEdit` (tek form; `editTaskAll` bunu açar), `editTaskReward`, `deleteTask`,
  `parentTaskActions`, `completeTask` (öğrenci → pending), `approveTask`, `rejectTask`,
  `undoCompletedTask`, `markTaskDone`, `markTaskMissed`, `reactivateTask`, `autoMissCheck`,
  `applyPenalty`, `revertPenalty`, `completeAndReward`.
- **Sınav işlemleri:** `submitExam`, `openExamEditor` / `saveExamEdit`, `clearExamScore`,
  `deleteExam`, `examBonus`, `parseExamScore`, `recordExamScore`, `applyExamScore`.
- **PDF:** `openTasksForPdf` (aktif ve süresi geçmemiş), `tasksPdfHtml`, `exportOpenTasksPdf`
  (önce `scrollTo(0,0)`, html2canvas `scrollX/scrollY: 0`, yükseklik ≤1100px → tek A4).
- **Zamanlayıcılar:** 1 sn geri sayım; 60 sn'de bir `checkAlarms()` + `autoMissCheck()`.
- **Başlangıç:** `checkBadges(); checkAlarms(); renderAll(); autoMissCheck();` ve 250 ms sonra
  Firebase otomatik bağlanır (`DEFAULT_FIREBASE_CONFIG`).

### 3.3 Roller ve PIN
- Varsayılan PIN `1234`; `settings.pinHash = hashPin(pin)` (düz metin saklanmaz),
  `settings.pinDefault=true` iken Panelde uyarı çıkar. Veli moduna geçiş `askPin` ile.
- Her veli fonksiyonunun başında `if (ui.role !== 'parent') return;` olmalı. Veli düğmeleri
  render ederken de `ui.role === 'parent'` ile koşullanır (öğrenci görmez).

---

## 4. Veri Modeli (`state`)

`state.version = 11` (şu anki). **Yeni alan eklerken** `migrate()` sonunda varsayılan ver
(ör. `s.x = s.x || {}`); veri dönüştürme gerekiyorsa yeni `if (s.version < 12) {…; s.version = 12;}`
bloğu ekle ve `seedState().version`'ı da artır. Firebase'den gelen veri de `migrate()`'ten geçer.

| Alan | Açıklama |
|---|---|
| `student` | `{ name, nickname:'Ruz', grade:'Terza Media' }` |
| `xp`, `totalXp`, `gold` | Puanlar (`totalXp` seviyeyi belirler). |
| `streak`, `lastCompletionDate` | Seri (`recalcStreak` hesaplar). |
| `history[]` | `{ d:'YYYY-MM-DD', xp, n }` günlük kazanım. |
| `tasks[]` | Görevler (aşağıda). |
| `exams[]` | Sınavlar (aşağıda). |
| `schedule[]` | Haftalık program `{ id, day:0-6 (0=Pzt), type:'school'|'course', start, end, title, place }`. |
| `rewards[]`, `redemptions[]` | Ödül mağazası ve talepler (`status: pending/approved/rejected`, `cost` altın). |
| `badges{}` | `{ rozetId: 'YYYY-MM-DD' }` |
| `alarmsLast{}` | `{ examId: 'YYYY-MM-DD' }` aynı gün ikinci alarmı engeller. |
| `level10RewardClaimed` | Seviye 10 ödülü alındı mı. |
| `autoMissFrom` | ISO zaman; otomatik "Yapılmadı" yalnızca bundan sonra dolan görevlere uygulanır. |
| `vocab`, `vocabLog{}` | Günün kelime oyunu durumu ve geçmişi `{ tarih: { score, xp } }`. |
| `argoInbox{}` | Argo'dan gelen, onay bekleyen ödev/promemoria (betik yazar, veli siler). |
| `argoSeen{}` | Daha önce gelmiş Argo kayıt anahtarları (tekrar gelmesin). |
| `argoLastSync` | `{ at, ok, added, found, addedReminders, grades, reminderError?, gradeError?, error? }` |
| `argoGrades{}` | Argo notları (betik her çalışmada **tamamen** yeniden yazar). |
| `argoGradeIgnored{}` | Velinin "Yoksay" dediği not id'leri. |
| `settings` | `{ pinHash, pinDefault, notify, firebase }` |

**Görev (`task`) alanları:** `id, title, desc, subject, difficulty('normal'|'boss'), xp, gold,
createdAt, dueDate('YYYY-MM-DD'), status, activatedAt(ISO), submittedAt, completedAt, goldPaid,
missedAt, missedAuto, penaltyXp, source('argo'), argoId`.
Durum yaşam döngüsü:
`active` →(öğrenci "bitti")→ `pending` →(veli onay)→ `completed`
`active` →(süre doldu, `autoMissCheck`)→ `missed` →(veli: Yapıldı Say / Yeniden Aktif)→ …
`pending` →(veli reddet)→ `active`; `completed` →(veli Geri Al)→ `active`.

**Sınav (`exam`) alanları:** `id, title, subject, date, time('HH:MM', vars. 09:30), note,
alarmDays, boss(false değilse Boss), score(0-10, 2 ondalık), awardedXp, awardedAt,
source('argo'), argoId (promemoria'dan), argoGradeId (bağlı Argo notu)`.

**Dersler (`SUBJECTS`):** `mat` Matematik, `ita` İtalyanca, `sci` Fen Bilimleri, `sto` Tarih,
`geo` Coğrafya, `ing` İngilizce, `fra` Fransızca, `art` Görsel Sanatlar, `mus` Müzik,
`tec` Teknoloji, `rel` Din Kültürü, `gym` Beden Eğitimi. Her birinde `name`, `it` (İtalyanca
adı), `icon`. Renk/kısa ad: `SUBJECT_COLORS`, `SUBJECT_SHORT`.

**Diğer localStorage anahtarları:** `odevAvciUIV1` (rol/görünüm), `odevAvciGhTokenV1`
(yalnızca cihazda GitHub token).

---

## 5. Oyun Kuralları

- **Seviye:** `LEVEL_THRESHOLDS = [0,500,1200,2200,3500,5200,7500,10500,14500,20000]` (toplam
  XP); 10 seviye, unvanlar `LEVEL_TITLES` ("Çırak Avcı" … "Boss Termonatör").
- **Görev altını (`taskGold`):** `t.gold` sayıysa o; yoksa XP ≤50 → 0, Boss ya da XP ≥200 → 20,
  XP ≥150 → 10, diğer → 5. `goldForXp(xp) = max(1, round(xp/10))` (sınav/kelime ödülleri için).
- **Görev akışı:** Öğrenci "Görevi Tamamla" → `pending`. Veli onaylarsa XP + altın verilir;
  XP/seri **öğrencinin bitirdiği güne** yazılır (`submittedAt`). Altın bir görev için bir kez
  verilir (`goldPaid`).
- **Yapılmadı cezası:** Süresi geçen aktif görev otomatik `missed`; görevin XP'si kadar XP düşer
  (0'ın altına inmez), **altın asla silinmez**, seri sıfırlanır (`streakResetDay`). Veli sonradan:
  *Yapıldı Say* (ceza iade + normal XP/altın), *Yapılmadı* (elle), *Yeniden Aktif* (yeni tarih,
  ceza iade). Güncelleme öncesi eski görevler ve süresi geçmişken açılanlar cezalandırılmaz
  (`autoMissFrom`, `activatedAt`).
- **Sınav bonusu (`examBonus`):** not <7 → 0. Boss: 7→100, 8→200, 9→300, 10→500.
  Normal: 7→50, 8→100, 9→150, 10→250. Not değişirse fark eklenir/çıkarılır; not silinirse
  (`clearExamScore`) kazanılan XP/altın geri alınır.
- **Rozetler (`BADGES`):** İlk Ganimet, On Görev, Sınav Avcısı (8+), Tam İsabet (9+), Kusursuz
  Zafer (10), Boss Avcısı (Boss 8+), Boss Ustası (3 Boss 8+), 1000 XP, Ödül Avcısı.
  Koşul bozulursa `pruneBadges` rozeti kaldırır.
- **Boss alarmı:** sınavdan `alarmDays` gün önce (vars. 2) günde bir kez ses + bildirim + toast.
- **Kelime Avı:** Her gün 10 İtalyanca kelime (A2/B1), 4 şıklı, günde bir kez; aynı gün her
  cihazda aynı sorular (tohumlu karıştırma). **10/10 → +20 XP, 8–9 → +10 XP, ≤7 → 0.**
  Kullanıcı ileride okul kitabından fotoğraf gönderip kelimeleri oradan seçmek istiyor (§12).

---

## 6. Firebase Senkronu

### 6.1 Proje
- Proje: `odev-avcisi-35857`, Realtime DB:
  `https://odev-avcisi-35857-default-rtdb.us-central1.firebasedatabase.app`, kök düğüm **`odevAvci`**
  (tüm `state` burada). Config kodda `DEFAULT_FIREBASE_CONFIG`.
- Kimlik: **E-posta/şifre "aile hesabı"** (Firebase Auth). Veli ve öğrenci cihazları aynı aile
  hesabıyla giriş yapar (Ayarlar → Aile Hesabı). Konsolda Google sağlayıcısı da açılmıştı;
  uygulama onu kullanmıyor.

### 6.2 Nasıl çalışır
- `save()` → `fbPush()`: son bilinen bulut kopyası (`FB.base`) ile yerel durum karşılaştırılır
  (`fbDiff`, anahtar sırasından bağımsız `stableJSON`) ve **sadece değişen yollar**
  (`tasks/3`, `gold` …) `ref.update()` ile gönderilir. İki cihaz farklı şeyleri değiştirirse
  birbirini silmez.
- `fbOnValue`: buluttan gelen tüm veri `migrate()`'ten geçirilip `state` yapılır; çevrimdışı
  bekleyen değişiklikler (`applyPaths`) üstüne uygulanır ve yeniden gönderilir.
- Betiğin yazdığı alanlar (`argoInbox`, `argoGrades`, `argoLastSync`, `argoSeen`) uygulamaya
  bu yolla gelir. Uygulama `argoGrades`'i **değiştirmez** (yalnızca okur).

### 6.3 Kurallar
- Yayındaki kurallar (kullanıcı konsolda yayınladı): kök okuma/yazma kapalı; `odevAvci` yalnızca
  `auth != null && auth.uid === '<aile UID>'`. Depodaki `database.rules.json` şablondur.
- Geçmiş: Firebase "test modu kuralları X gün içinde bitiyor" e-postası geldi; kurallar aile
  UID'sine kilitlenerek çözüldü. Böyle bir e-posta tekrar gelirse kuralların yayında olduğunu
  kontrol ettir.

---

## 7. Argo DidUP Entegrasyonu

### 7.1 Amaç ve akış
Okulun Argo DidUP Famiglia sistemindeki **compiti assegnati** (ödevler), **promemoria**
(öğretmen hatırlatmaları) ve **voti** (notlar) çekilir → Firebase'e yazılır → uygulamada
**Panel → Argo'dan Gelenler** kartında veli onaylar.

### 7.2 GitHub Actions
- `.github/workflows/argo-sync.yml`: cron `7 5,12,15,18 * * *` (UTC; İtalya ~07/14/17/20) +
  `workflow_dispatch`. `concurrency: argo-sync`. Python 3.12.
- Bağımlılık: gayriresmi kütüphane **`didupwrapper`** (github.com/Rocciadura/didupAPI-wrapper),
  **commit `999b74bb90e219db3356dd00fb5c522fe424e258`'e sabit**. Sürüm yükseltirken
  `DiDUPClientSync`, `get_registro`, `get_promemoria`, `get_voti`, `didupwrapper.auth.ArgoConfig`
  arayüzünün aynı kaldığını kontrol et.
- Uygulamadaki **Ayarlar → Argo → Şimdi Senkronize Et** düğmesi, cihazdaki GitHub token'ıyla
  (fine-grained, Actions: Read and write) `workflow_dispatch` tetikler (`argoSyncNow`). Token
  yoksa Actions sayfasını açar. Sonuç `argoLastSync` değişince `argoSyncCheck` ile bildirilir.

### 7.3 `scripts/argo_sync.py` adım adım
1. Firebase'e REST ile giriş (`identitytoolkit … signInWithPassword`, `FB_EMAIL/FB_PASSWORD`).
2. `fetch_argo()` → `argo_attempts()` sırasıyla bağlanmayı dener (bkz. 7.4), `read_argo()`:
   - `get_registro()` → her dersin `compiti` listesi (metin, `data_consegna`) + öğretmen→ders
     haritası (`pk_docente`/`docente` → `materia`), promemoria'nın dersini bulmak için.
   - `get_promemoria()` (yalnızca `flg_visibile_famiglia`), `get_voti()`. Bu ikisi hata verirse
     `None` döner, ödevler yine yazılır.
3. `build_entries` (ödev): dünden eski teslim tarihli olanlar alınmaz; anahtar
   `task_key = sha1(materia|due|metin)[:16]`; `argoSeen ∪ argoInbox`'ta olan tekrar eklenmez.
   Ders `map_subject` (`SUBJECT_RULES` alt dize eşlemesi; "motori"/"fisica"→gym önce),
   ödül `guess_reward` (verifica/interrogazione/test → 300 XP boss; kısa "porta(re)" → 50;
   diğer 100), başlık `short_title` ("Ders: metnin başı…").
4. `build_promemoria_entries`: dünden eskiler alınmaz; anahtar `"p" + sha1("promemoria|gün|metin")[:15]`;
   `kind:"promemoria"`, `suggest:"exam"|"task"` (`EXAM_RE`: verific, interrogazi, compito in
   classe, test, prova, esame, simulazione), ders önce metinden, yoksa öğretmen **tek** derse
   eşleniyorsa o, belirsizse boş (veli seçer). `time` = `ora_inizio` (00:00 ise boş).
5. `build_grades`: yalnızca sayısal notlar (0–10), **son 150 gün**; anahtar
   `"g" + sha1(gün|pk_materia|prg_voto|kind)[:15]`; alanlar `date, subject, subjectIt, value
   (ör. "8-" → 7.75), code ("8-", "6½"), kind (S yazılı / N sözlü / P uygulama), desc, comment`.
6. Firebase'e yazar: `argoInbox` (patch), `argoSeen` (patch), `argoGrades` (**put**, tamamen),
   `argoLastSync` (put). Log: yalnızca sayılar ("Argo'da N ödev kaydı bulundu" …).
7. Hata: `describe_error` (HTML etiketleri temizlenir, URL sorguları atılır) → `argoLastSync.error`
   ve log. "consent" geçen hatada `describe_consent_page()` sayfanın yalnızca **yapısını** yazar.

### 7.4 Argo bağlantı geçmişi ve şu anki yol (ÖNEMLİ)
Argo'nun resmi API'si yok; kütüphane resmi mobil uygulamayı taklit eder. Argo iki kez değişti:

- **28 Ekim 2026 — onay ekranı (TRAS-1928):** OAuth zincirinde `/auth/sso/consent/` artık 302
  yerine **HTTP 200** sayfa dönüyor; içinde `data-auth-app-redirect` bağlantısı var (tarayıcı
  JS ile açıyor). Çözüm: `_capture_consent_pages()` `httpx.AsyncClient.send`'i sarar; consent
  yanıtında bu bağlantıyı bulursa (`consent_redirect_target`) yanıtı **302 + Location**'a
  çevirir (set-cookie korunur). Argo'nun genel hata sayfası: başlık "Oops!", `auth-error`,
  `id="collapseOne"` içinde OAuth hata detayı.
- **17 Kasım 2026 — uygulama API'si kapandı:** `https://www.portaleargo.it/appfamiglia/api/rest/`
  her isteğe **503** dönüyor (Argo bilinmeyen yollara da 503 verir). Aile web sitesi
  (`https://www.portaleargo.it/famiglia/`) **aynı API'yi** (POST `login`, POST
  `dashboard/dashboard` `{dataultimoaggiornamento, opzioni}`, yanıt `data.dati[0]`, alanlar
  `registro/promemoria/voti` aynı) yeni adreste kullanıyor:
  **`https://didattica.portaleargo.it/famiglia/api/`**. Başlıklar: `Authorization: Bearer
  <OIDC token>`, `x-auth-token`, `x-cod-min`, `argo-client-version: <web sürümü>`,
  **`os-type: WEB`**.
- **Şu anki bağlantı sırası (`argo_attempts`):**
  1. `web`: `WebConfig` (ArgoConfig alt sınıfı, `os-type: WEB` ekler), `api_base_url` =
     yeni adres, OIDC istemcisi **`8aef9dcb-e948-462a-a239-646a54a44ddb`**, redirect
     `https://www.portaleargo.it/famiglia/oidc-callback.html`, scope `openid profile`,
     sürüm `web_version()` (site JS'inden `="X.Y.Z",…={name:"Famiglia WEB"` okunur; bulunamazsa
     `4.3.0`). **24 Kasım 2026'dan beri bu yol çalışıyor.**
  2. `uygulama-yeni-adres`: mobil istemci (`72fd6dea-…`, redirect
     `it.argosoft.didup.famiglia.new://login-callback`) + yeni adres, sürüm App Store'dan.
  3. `uygulama-eski-adres`: eski adres (Argo geri açarsa diye).
  - Kullanıcı/şifre hatasında (`Login SSO fallito`, `credenziali`) **diğer yollar denenmez**
    (`is_credential_error`) — hesap kilitlenmesin.
  - Hangi yolun çalıştığı log'a yazılır: `Argo bağlantısı: web`.

### 7.5 Uygulama tarafı (Panel → "Argo'dan Gelenler" kartı)
- `argoInboxCard()`: üç sekme **Ödevler | Promemoria | Notlar** (`argoTab`, `setArgoTab`).
  Kart, bekleyen kayıt ya da not önerisi yoksa gizlenir.
- **Ödevler/Promemoria:** her kayıtta başlık, İtalyanca metin, ders seçimi (`argoSubChange`
  başlıktaki ders önekini günceller), tarih, XP. Promemoria'da tür seçimi
  **🎯 Sınav olarak ekle** (saat alanı; Boss, `alarmDays:2`) / **⚔️ Görev olarak ekle**
  (`argoKindOf`, `argoKindToggle`). `approveArgo` / `approveAllArgo(tab)` (sadece açık sekme) /
  `rejectArgo` ("Gerek Yok": `argoSeen`'de kaldığı için bir daha gelmez). Görevler
  `source:'argo', argoId` taşır.
- **Notlar (`argoGradeSuggestions`):** not ↔ sınav eşleme sırası: (0) `exam.argoGradeId` ile
  önceden bağlı not, (1) aynı ders + aynı gün, (2) aynı ders + sınavdan sonraki 7 gün (en erken;
  yazılı önce). Yoksayılan notlar eşlemeye girmez. Sınavın notu yoksa **Notu Uygula**, farklıysa
  **Notu Güncelle** (`applyArgoGrade` → `applyExamScore`), `applyAllArgoGrades`. Sınavı olmayan
  son **30 gün** notları: **Sınav Ekle** (`addExamFromGrade`; yazılı → Boss, sözlü/uygulama →
  normal; başlık "Ders Yazılı Sınav/Sözlü/Uygulama") ya da **Yoksay** (`ignoreArgoGrade`).
  Notlar **asla otomatik** uygulanmaz (eşleme tahmine dayalı ve XP'yi etkiler).
- Ayarlar → Argo kartı: `argoStatusHtml()` ("Son çalışma: tarih • N yeni ödev, M promemoria"
  ya da hata), token kaydet/sil, Şimdi Senkronize Et.

### 7.6 Senkron bozulduğunda teşhis rehberi
1. Çalışmaları listele: GitHub MCP `actions_list` (`list_workflow_runs`, `argo-sync.yml`) ya da
   `curl -sS "https://api.github.com/repos/serkanarslansoy-svg/OdevTakip/actions/workflows/argo-sync.yml/runs?per_page=10"`.
   İlk başarısız çalışmayı bul (ne zaman başladı?).
2. Kaydı oku: `get_job_logs` (`run_id`, `failed_only: true`). Hata satırı
   `Argo'dan ödevler alınamadı: …` — tüm denenen yollar `|` ile ayrılmış.
3. Hata türüne göre:
   - **AuthError … Login SSO fallito** → şifre değişmiş/yanlış: kullanıcıya GitHub Secrets'taki
     `ARGO_*` değerlerini güncellet (önce Argo web'e elle girebildiğini doğrulat).
   - **Catena OAuth interrotta … consent** → OAuth akışı değişmiş; `describe_consent_page` çıktısına
     bak; Argo'nun auth JS'i: `https://www.portaleargo.it/assets/auth/js/main.*.js`.
   - **503 / 404** → API adresi değişmiş olabilir. Kimlik bilgisi **olmadan** genel uçları dene
     (curl ile `POST …/login` 401/403 dönerse adres canlı, 503 ise yok). Web sitesinin JS'ini
     incele: `https://www.portaleargo.it/famiglia/` → `assets/main-*.js` içinde
     `backend:"https://…"`, `client_id:"…"`, sürüm `it="X.Y.Z"`, istek başlıkları
     (`interceptors.request`); veri çağrıları `assets/dashboard-*.js` (`getDashboard`).
   - **410** → `argo-client-version` eski.
4. Kütüphanenin yeni sürümüne bak (github.com/Rocciadura/didupAPI-wrapper, son commit'ler);
   düzeltme varsa commit'i sabitleyerek yükselt.
5. Düzeltmeyi sahte modülle yerelde test et (§8.2), push et, `workflow_dispatch` ile çalıştır,
   kayıtta `Argo bağlantısı: …` ve sayıları gör, kullanıcıya sade dille anlat.

---

## 8. Test ve Doğrulama Tarifleri

### 8.1 Tarayıcı testi (Playwright) — her arayüz değişikliğinden sonra
Bulut oturumunda Playwright hazır: `require('/opt/node-tools/node_modules/playwright')`,
`chromium.launch({ executablePath: '/opt/pw-browsers/chromium' })`. `playwright install` yapma.
```js
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } }); // telefon
  const errors = []; page.on('pageerror', e => errors.push(e.message));
  // Firebase'i kapat: test verisi buluta gitmesin
  await page.route(/gstatic\.com\/firebasejs|firebasedatabase|firebaseio|identitytoolkit/, r => r.abort());
  await page.goto('file:///<repo>/index.html');
  await page.waitForTimeout(1500);
  await page.evaluate(() => {
    state.tasks = [ /* örnek görevler */ ];
    ui.role = 'parent'; ui.view = 'panel'; renderAll();   // veli; öğrenci için 'student'/'home'
  });
  // tıkla: page.click('button[onclick="approveArgo(\'p1\')"]'); durumu oku: page.evaluate(() => state...)
  console.log('errors:', errors);   // boş olmalı
  await browser.close();
})();
```
- Hem **öğrenci** hem **veli** rolünü dene; veli düğmeleri öğrencide görünmemeli.
- Ekran görüntüsü al ve bak (`locator(...).screenshot`). "Firebase yüklenemedi" toast'ı testte
  normaldir.
- XP/altın etkileyen değişiklikte önce/sonra `state.totalXp`, `state.gold`, `state.history` kontrol et.

### 8.2 Senkron betiği testi (gerçek Argo'ya bağlanmadan)
- `python3 -m py_compile scripts/argo_sync.py`
- Ayrı bir venv'de `httpx requests` kur; `sys.modules["didupwrapper"]` ve
  `sys.modules["didupwrapper.auth"]` için **sahte modül** yaz (`DiDUPClientSync` taklidi:
  `__enter__`, `get_registro`, `get_promemoria`, `get_voti`; `ArgoConfig` dataclass taklidi).
  Sonra `import argo_sync as a` ve `a.fetch_argo(...)`, `a.build_entries(...)`,
  `a.build_promemoria_entries(...)`, `a.build_grades(...)` çağır.
- OAuth/consent değişikliklerini `httpx.MockTransport` ile test et.

### 8.3 Gerçek senkron denemesi
GitHub MCP `actions_run_trigger` (`run_workflow`, `argo-sync.yml`, `ref: main`) → çalışmayı
bekle → `get_job_logs` ile sayıları oku. (`gh` CLI yoksa MCP ya da genel API.)

### 8.4 Yayın doğrulaması
```bash
curl -sS "https://api.github.com/repos/serkanarslansoy-svg/OdevTakip/actions/runs?per_page=3"   # "pages build and deployment" completed/success
curl -sS "https://serkanarslansoy-svg.github.io/OdevTakip/?v=$(date +%s)" | grep -c "function yeniFonksiyonAdi"
```

---

## 9. Dağıtım

- **Web:** GitHub Pages, `main` dalının kökü. Push → otomatik "pages build and deployment".
- **Android:** `build-apk.yml` (Capacitor 7, Node 20, Java 21) debug APK üretir; uygulama
  `server.url` ile Pages adresini açtığından **HTML güncellemesi için APK yeniden kurulmaz**.
  APK yalnızca `package*.json` / `capacitor.config.js` / workflow değişince yeniden derlenir.
- **iPhone:** Safari → Ana Ekrana Ekle (PWA). Çentik için safe-area boşlukları var.
- Kullanıcı yeni sürümü görmek için uygulamayı kapatıp açmalı (önbellek ~10 dk).

---

## 10. Bilinen Tuzaklar ve Dersler

- **Freebuff olayı:** Eski bir yapay zekâ aracı (Freebuff) dosyanın **eski kopyasını** commit'leyip
  (3e87f65) birçok özelliği sildi; 3-yollu `git merge-file` ile kurtarıldı (120e59f). Ders:
  düzenlemeden önce `git pull`, büyük yeniden yazımlardan kaçın, `index.html`'i bütün olarak
  başka bir kopyayla değiştirme; değişiklikleri hedefli yap.
- **`.pyc` dosyası depoda izleniyor** → commit'lerde dışarıda bırak (§1.2).
- **Tarihler:** her zaman yerel `ymd()` / `todayStr()`; `toISOString().slice(0,10)` kullanma
  (UTC kayması). Görev süresi `taskDue` = gün sonu 23:59:59.
- **Türkçe büyük/küçük harf:** "I/ı/İ/i" sorunları (toplu ekleme ayrıştırıcısında yaşandı);
  `toLocaleLowerCase('tr-TR')` ve `trUpper` kullan.
- **Toplu ekleme ayrıştırıcısı (`bulkParse`):** "4-7" gibi alıştırma numaraları tarih sanılıyordu;
  düzeltildi. Değiştirirken örnek metinlerle test et. Desteklenen biçim örneği:
  ```
  6/11
  Storia: Pag 84-85
  Italiano: Ripassa …
  ```
- **PDF:** sayfa kaydırılmışken üstte boşluk/ikinci boş sayfa sorunu vardı → `scrollTo(0,0)`,
  html2canvas `scrollX/scrollY:0`, içerik yüksekliği ≤1100px.
- **`prompt()` zinciri kullanma:** mobilde kötü; düzenleme için `openDetail` formu kullan
  (`openTaskEditor`, `openExamEditor` örnek).
- **Render sonrası görünüm:** veli formu kaydedince `renderAll()` çağır (aktif görünümde kalır);
  `renderGorev()` gibi belirli bir ekranı çağırmak kullanıcıyı başka sayfaya atar.
- **`checkAlarms`:** `(e.alarmDays || 2)` — `alarmDays: 0` fiilen 2 gün sayılır (küçük tuhaflık;
  geçmiş sınavlarda `alarmsLast` bugüne ayarlandığından sorun çıkmıyor).
- **Firebase boş nesne saklamaz:** `{}` alanlar buluttan `undefined` gelir → `migrate()` varsayılan verir.
- **Argo kayıtları herkese açık:** log'a metin yazma; hata mesajında URL sorgularını temizle.
- **Actions uyarısı:** `actions/checkout@v4`, `setup-python@v5` Node 20 ile ilgili deprecation
  uyarısı veriyor (şimdilik zararsız; ileride sürüm yükselt).

---

## 11. Değişiklik Günlüğü (özet, eskiden yeniye)

**Ekim 2026**
- İnceleme sonrası iyileştirmeler: PIN hash'leme, Firebase diff senkronu, aile hesabı (e-posta/şifre)
  girişi, toplu ödev ekleme, Veli Paneline XP/altın kartı, Tamamlananlar panelden kaldırıldı.
- Veliye özel geriye dönük sınav + not girişi; haftalık takvim ızgarası (dokununca ayrıntı).
- Argo otomatik ödev senkronu (GitHub Actions + Firebase, veli onayı; ödev metni İtalyanca,
  ders eşlenir); Ayarlar'a "Şimdi Senkronize Et".
- Günlük İtalyanca Kelime Avı (10 soru, 10/10 +20 XP, 8–9 +10 XP).
- Dersler sekmeleri yeniden tasarlandı (Devam/Bitti/Yapılmadı/Tümü).
- Otomatik "Yapılmadı" sistemi (XP cezası, altın korunur, seri sıfırlanır; veli geri alabilir);
  yapılmayanlar kırmızı.
- Görev Ata'da ders açılır listesi; panelden "Yapılmayan Görevler" kaldırıldı.
- Tek sayfa PDF (yalnızca devam eden, yalnızca veli); görevlerden saat kaldırıldı.
- iPhone üst boşluk düzeltmesi; Hızlı Görev Şablonları kaldırıldı.
- Freebuff'ın sildiği özellikler geri getirildi.

**Kasım 2026**
- 04 Kas: Argo onay ekranı (TRAS-1928) otomatik geçiliyor → senkron yeniden çalıştı (64c9e91).
- 04 Kas: Promemoria onay kutusuna, Sınav/Görev olarak eklenebilir (f7dbe9d); Argo kartı
  Ödevler | Promemoria sekmeleri (b97582c).
- 04 Kas: Argo notları → Notlar sekmesi, sınavlarla eşleme, Notu Uygula/Güncelle, Sınav Ekle (d33002e).
- 16 Kas: Takvimde görev açıklaması + veli için görev düzenleme formu; Görev Ata'daki Düzenle de
  aynı form (1747e98).
- 16 Kas: Sınav düzenleme formu (Takvim + Planla; not/Boss değişince XP farkı) (c67c6b6).
- 24 Kas: Argo uygulama API'si kapandı (17 Kas'tan beri 503) → Famiglia web API'sine geçildi,
  yedek yollar + şifre hatasında dur (0c7f93c). İlk çalışmada 157 ödev, 33 promemoria, 31 not.
- 28 Kas: Bu `CLAUDE.md` eklendi (kullanıcının Claude hesabı değişeceği için kalıcı hafıza);
  İngilizce özet, "yeni oturuma başlarken" listesi, sözlük ve depo için `README.md` eklendi.

---

## 12. Açık İşler / Fikirler

- **Kelime Avı için okul kitabı kelimeleri:** kullanıcı kitap sayfalarının fotoğraflarını
  gönderecek; sayfadaki A2/B1 kelimeleri seç, `VOCAB` dizisine `italyanca=türkçe` biçiminde ekle
  (tekrarları ele, Türkçe karşılıklar doğru ve kısa olsun).
- **Bekleyen promemoria'yı takvimde göstermek** (ayrı renk, yalnızca veli takviminde) önerildi;
  kullanıcı henüz cevap vermedi.
- Senkron hata verdiğinde Panelde uyarı göstermek önerildi (şu an yalnızca Ayarlar'daki
  "Son çalışma" satırında görünüyor).
- `checkAlarms`'taki `alarmDays || 2` tuhaflığı (0 gün seçilebilsin istenirse düzelt).
- Actions sürümlerini Node 24 uyumlu sürümlere yükseltmek.
- `scripts/__pycache__`'i depodan çıkarıp `.gitignore`'a eklemek (kullanıcı onayıyla).

---

## 12.1 Claude Hesabı Değişirse (kullanıcı için kısa yol)

Kullanıcının Claude hesabı değişebilir; proje hafızası bu dosyada olduğu için kayıp olmaz.
Yeni hesapta:
1. claude.ai → Ayarlar → Bağlantılar'dan **GitHub hesabını bağla** ve Claude GitHub uygulamasının
   `serkanarslansoy-svg/OdevTakip` deposuna erişimi olduğundan emin ol.
2. Claude Code'da (web/telefon) yeni oturumu **OdevTakip deposunu seçerek** başlat.
3. İlk mesaj olarak şunu yazmak yeterli: *"CLAUDE.md'yi oku, projeye kaldığımız yerden devam edelim."*
- GitHub Secrets (Argo/Firebase), Firebase projesi, GitHub Pages ve otomatik senkron **Claude
  hesabından bağımsızdır**; hesap değişince hiçbiri durmaz.
- Uygulamadaki "Şimdi Senkronize Et" düğmesinin GitHub anahtarı da Claude'a bağlı değildir.

---

## 13. Bu Dosyayı Güncel Tutma

Her anlamlı değişiklikten sonra:
1. §11'e tarih + kısa açıklama + commit kısaltması ekle.
2. Yeni bir kural/karar varsa §1.4'e, yeni bir tuzak varsa §10'a yaz.
3. Veri modeli değiştiyse §4'ü, Argo akışı değiştiyse §7'yi güncelle.
4. Tamamlanan açık işleri §12'den sil, yenilerini ekle.
5. Gizli bilgi yazmadığından emin ol.
