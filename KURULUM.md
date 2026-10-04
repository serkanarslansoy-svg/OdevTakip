# 🏹 Ödev Avcısı — Kurulum & Kullanım Rehberi

Rüzgar için hazırlanmış oyunlaştırılmış ödev, sınav ve çalışma takip uygulaması.
Tek dosyadır (`index.html`), kurulum gerektirmez, telefonda ve bilgisayarda çalışır.

---

## ⚡ Hızlı Başlangıç (2 dakika)

### Telefonda / tablette açma
1. `index.html` dosyasını telefonuna gönder (WhatsApp, e-posta, USB…).
2. Dosyayı **Chrome** veya **Safari** ile aç.
3. Tarayıcı menüsünden **"Ana ekrana ekle" / "Add to Home Screen"** seç.
4. Artık uygulama gibi tam ekran açılır. 🎉

> Not: Uygulama internet olmadan da çalışır (veriler cihazda saklanır).
> İnternete çıktığında Firebase senkronunu açarsan iki cihaz aynı veriyi görür.

---

## 🎮 İki Mod

| Mod | Kim kullanır? | Giriş |
|---|---|---|
| 🚀 **Ruz (Öğrenci)** | Oğlun | PIN gerekmez |
| 🛡️ **Veli (Komutan)** | Sen | 4 haneli PIN (ilk girişten sonra **Ayarlar**'dan değiştir; varsayılan değiştirilene kadar panelde uyarı çıkar) |

Sağ üstteki **Ruz / Veli** düğmeleriyle geçiş yapılır.

### 🚀 Öğrenci ekranları
- **Görevler:** Ana ekran — XP/seviye göstergesi, gün serisi 🔥, acil sınav alarmı, bugünün görevleri
- **Dersler:** Tüm görevler; ders filtreleri, arama, devam eden / tamamlanan sekmeleri
- **Program:** Haftalık takvim görünümü (derse dokununca saat, yer, o gün teslim edilecek ödevler ve sınavlar açılır) veya günlük liste, "ŞU AN" canlı göstergesi
- **Sınavlar:** Boss savaşı geri sayımları, yaklaşan / geçmiş sınavlar, girilmiş sınav notları, bildirim izni
- **Ödüller:** Karakter vitrini, rozet koleksiyonu, **Ganimet Mağazası** (XP'yi ödüle takas)

### 🛡️ Veli ekranları (PIN ile)
- **Panel:** Ruz'un seviyesi, toplam XP, altın bakiyesi ve haftalık kazancı; onay bekleyen görevler/takaslar, hızlı görev şablonları, son 7 gün grafiği
- **Görev Ata:** Görev oluştur; **Toplu Ödev Ekle** ile öğretmen mesajını/Classroom listesini yapıştırıp tek seferde çok görev ekle (ders, zorluk BOSS/NORMAL, XP, son tarih) → anında Ruz'un ekranına düşer
- **Planla:** Sınav tanımla ya da geçmiş tarihli sınavı notuyla birlikte gir (not girişi yalnızca velide) (Boss seçimi ve alarm günü ayarlanır), geçmiş sınavın notunu gir/düzenle + haftalık ders programını yönet
- **Ödül:** Mağazaya ödül ekle, takas taleplerini onayla/reddet
- **Ayarlar:** PIN değiştir, bildirim izni, **Firebase senkron**, **Aile Hesabı** girişi, yedek al/geri yükle, sıfırla

---

## 🔁 Temel Akış

```
Sen görev ata (XP belirle)
   ↓
Ruz görevi görür, çalışır, "Tamamla" der
   ↓
Görev ONAY BEKLİYOR durumuna geçer (XP henüz verilmez)
   ↓
Sen veli panelinden Onayla → Ruz'a +XP geçer, seri/rozetler işler
        veya Reddet → görev tekrar aktif olur
```

Ödül tarafı:
```
Ruz mağazadan takas eder → XP'si düşer, talep onaya gider
   ↓
Sen onaylarsan: 🎁 ödül kazanıldı
Sen reddedersen: XP otomatik iade edilir
```

---

## ☁️ İki Cihaz Senkronu (Firebase, ~3 dk)

Sadece **senin cihazında** kullanacaksan bu adımı atla.
Ruz kendi telefonundan kullanacaksa ve ikinizin **aynı veriyi** görmesini istiyorsan:

1. **console.firebase.google.com** → yeni proje oluştur (Analytics'i kapatabilirsin).
2. Sol menü → **Build → Realtime Database** (⚠️ Firestore değil!) → *Create Database* → **Test mode** → *Enable*.
3. Proje ayarları (⚙️) → **Web uygulaması ekle** (`</>` simgesi) → verilen `firebaseConfig` nesnesini kopyala.
4. Uygulamada: **Veli modu → Ayarlar → Bulut Senkronu** → yapılandırmayı kutuya yapıştır → **Bağlan**.
5. İkinci cihazda (Ruz'un telefonu) aynı `index.html` dosyasını açıp **aynı config** ile bağlan.

Bağlanınca:
- Bulutta veri varsa otomatik çekilir; yoksa cihazdaki veriler yüklenir.
- Her değişiklik ~1 saniye içinde diğer cihaza yansır (header'da 🟢 **BULUT** rozeti).
- Senkronu kapatmak istersen aynı ekrandan **Kes** düğmesine bas (veriler cihazda kalır).

Senkron yalnızca değişen alanları gönderir (ör. tek bir görevin durumu). İki cihazda aynı anda
farklı işlemler yapılsa da biri diğerini silmez; çevrimdışıyken yapılan değişiklikler bağlantı
gelince buluttaki verinin üstüne eklenir.

### 🔒 Veriyi yalnızca ailene aç (önemli!)

"Test mode" kuralları veritabanını adresi bilen **herkese** açar ve 30 gün sonra kapanır.
Uygulama herkese açık bir sitede yayınlandığı için veritabanı adresi de görülebilir.
Erişimi aile hesabıyla sınırla:

1. Firebase Console → **Authentication** → *Get started* → *Sign-in method* → **Email/Password** → *Enable*.
2. **Users** sekmesi → *Add user*: bir aile e-postası ve güçlü bir şifre.
3. Uygulamada **Veli → Ayarlar → Aile Hesabı** → bu hesapla giriş yap.
   **Hem kendi cihazında hem Ruz'un cihazında** giriş yap.
4. Aynı ekranda görünen **UID**'yi kopyala.
5. Realtime Database → **Rules** sekmesi → bu depodaki `database.rules.json` içeriğini yapıştır,
   `AILE_UID` yerine kopyaladığın UID'yi yaz → **Publish**.

Bundan sonra veriyi yalnızca bu hesapla giriş yapmış cihazlar okuyup yazabilir. Giriş yapmamış
bir cihaz "Bulut erişimi reddedildi" uyarısı verir ve verileri yalnızca kendinde tutar.
Sırayla yap: önce iki cihazda giriş, sonra kuralları yayınla.

---

## 📥 Argo'dan Otomatik Ödev

Okulun Argo DidUP sistemindeki "Compiti assegnati" listesi **günde 4 kez** (İtalya saatiyle
yaklaşık 07:00, 14:00, 17:00, 20:00) otomatik çekilir. Ödev metni **İtalyanca** kalır, dersi
uygulamadaki derse eşlenir (MATEMATICA → Matematik gibi) ve **Veli → Panel → Argo'dan Gelenler**
listesine düşer. Ruz'un ekranına sen
onayladıktan sonra geçer. Onaylarken başlığı, açıklamayı, dersi, tarihi ve XP'yi düzeltebilirsin;
"Gerek Yok" dediğin ödev bir daha gelmez.

**Kurulum (bir kez):**
1. Önce yukarıdaki **Aile Hesabı** adımlarını tamamla (Firebase'de e-posta/şifre kullanıcısı).
2. GitHub'da depo → **Settings** → **Secrets and variables** → **Actions** →
   **New repository secret** ile şu 5 sırrı ekle:

   | Ad | Değer |
   |---|---|
   | `ARGO_SCUOLA` | Okul kodu (Argo girişindeki, ör. `SC12345`) |
   | `ARGO_USERNAME` | Argo veli kullanıcı adı |
   | `ARGO_PASSWORD` | Argo veli şifresi |
   | `FB_EMAIL` | Firebase aile hesabı e-postası |
   | `FB_PASSWORD` | Firebase aile hesabı şifresi |

3. Depoda **Actions** sekmesi → **Argo ödev senkronu** → **Run workflow** ile ilk kez elle çalıştır.
4. Yeşil tik çıkarsa uygulamada **Ayarlar → Argo Otomatik Ödev → Son çalışma** güncellenir.

**Elle senkron:** Uygulamada **Ayarlar → Argo Otomatik Ödev → Şimdi Senkronize Et**. Anahtar
eklenmemişse düğme GitHub'daki sayfayı açar (orada **Run workflow**). Tek dokunuşla çalışması için
GitHub → Settings → Developer settings → Personal access tokens → **Fine-grained tokens** → yalnızca
**OdevTakip** deposu, izin olarak sadece **Actions: Read and write** verilmiş bir anahtar oluşturup aynı
ekrana yapıştır. Anahtar yalnızca o cihazda saklanır, buluta gitmez.

**Notlar:**
- Şifreler GitHub Secrets'ta şifreli durur; kayıtlarda (log) görünmez. Betik kayıtlara ödev
  metni yazmaz, sadece kaç ödev bulunduğunu yazar.
- Argo'nun resmi bir API'si yok; gayriresmi [didupAPI-wrapper](https://github.com/Rocciadura/didupAPI-wrapper)
  kütüphanesi kullanılır. Argo giriş yöntemini değiştirirse çekme durabilir; uygulama
  çalışmaya devam eder, "Son çalışma" satırında hata görünür.
- GitHub, depoda 60 gün hiç değişiklik olmazsa zamanlanmış görevleri durdurur. Öyle olursa
  Actions sekmesinden tekrar etkinleştir.

---

## 🔔 Sınav Boss Alarmları

- Sınavları veli panelinden tanımlarken **"alarm kaç gün önce?"** ayarını seç (varsayılan 2 gün).
- Alarm günü geldiğinde uygulama açıksa: 🚨 sesli uyarı + ekranda alarm kartı + toast.
- **Bildirim izni** verilmişse uygulama kapalıyken de cihaz bildirimi düşer.
- Öğrenci ekranında sınav yaklaşırken kart **turuncu neon pulse** efektine bürünür ve
  canlı geri sayım (gün/saat/dakika/saniye) işler.

---

## 🏅 Oyunlaştırma Sistemi

| Öğe | Nasıl işler |
|---|---|
| **XP** | Görev zorluğuna göre veli belirler (NORMAL 50–250, BOSS 300+) |
| **Seviye** | Her 500 XP'de 1 seviye + yeni rütbe adı (Çırak Avcı → Boss Termonatör) |
| **Seri 🔥** | Her onaylanan görev günü seriyi uzatır; gün atlanırsa sıfırlanır |
| **Sınav notu** | Veli geçmiş sınava 0–10 not girer. Boss sınavında 7+: 100, 8+: 300, 9+: 450, 10: 600 XP; normal sınavda 8+: 150, 9+: 225, 10: 300 XP. Not düzeltilirse XP farkı güncellenir. |
| **Kelime Avı** | Öğrenci ana ekranında günde bir kez 10 İngilizce kelime (A2/B1), 4 şıktan Türkçesi seçilir. 10/10: +20 XP, 8-9: +10 XP, 7 ve altı: XP yok. Yarıda kalırsa kaldığı yerden devam eder, tekrar oynanamaz. |
| **Rozetler** | 8+, 9+, 10 sınav notları; Boss sınavından 8+ ve üç Boss sınavından 8+; görev/XP/ödül rozetleri. Çalışma serisi ve sadece sınava girme rozet kazandırmaz. |
| **Ödüller** | Veli tanımlar; Ruz XP'sini gerçek ödüllere takas eder, sen onaylarsın |

---

## 💾 Veri & Yedek

- Veriler cihazda `localStorage`'da saklanır; Firebase açılırsa buluta yansır.
- **Ayarlar → Dışa Aktar**: tüm verileri JSON olarak indirir (yedek).
- **Ayarlar → İçe Aktar**: JSON yedeği geri yükler.
- **Tüm Verileri Sıfırla**: her şeyi örnek verilere döndürür (geri alınamaz!).

---

## ❓ SSS

**PIN'i unuttum ne yapayım?**
PIN artık düz metin değil, özet (hash) olarak saklanır; geri okunamaz. Bilgisayarda uygulamayı
açıp tarayıcı konsoluna `state.settings.pinHash = hashPin('YENİPIN'); save();` yazarak yeni PIN
belirleyebilirsin (bulut bağlıysa diğer cihaza da geçer).

**Toplu ödev eklemede ne tanınıyor?**
Tarih satırları (`5 Ekim`, `05/10`, `7 Ottobre`, `Pazartesi`/`Lunedì`) ve Türkçe/İtalyanca ders
adları (`Matematik`/`Matematica`, `Tarih`/`Storia`…). Tarih ya da ders adı tek başına bir satırdaysa
altındaki satırlara uygulanır. "sınav/verifica" geçen satırlar BOSS (300 XP), "getir/portare" geçenler
50 XP önerilir. Eklemeden önce her satırın dersini, tarihini ve XP'sini düzeltebilirsin.

**Telefonda bildirim gelmiyor?**
Sınavlar ekranından veya Ayarlar'dan **Bildirim İznini Aç** düğmesine bas; iOS'ta
uygulamanın ana ekrana eklenmiş olması gerekir.

**Firebase bağlanamıyor?**
`databaseURL` alanının config'de olduğundan emin ol (Realtime Database oluştur
meden alınan config'lerde bu alan olmayabilir). Ayrıca URL'nin `https://` ile
başladığını ve veritabanının oluşturulduğunu kontrol et.

---

*Ödev Avcısı v1.0 — iyi çalışmalar! 🏹*
