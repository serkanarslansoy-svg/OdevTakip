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
| 🛡️ **Veli (Komutan)** | Sen | **PIN: `1234`** (değiştir!) |

Sağ üstteki **Ruz / Veli** düğmeleriyle geçiş yapılır.

### 🚀 Öğrenci ekranları
- **Görevler:** Ana ekran — XP/seviye göstergesi, gün serisi 🔥, acil sınav alarmı, bugünün görevleri
- **Dersler:** Tüm görevler; ders filtreleri, arama, devam eden / tamamlanan sekmeleri
- **Program:** Haftalık okul + kurs çizelgesi, "ŞU AN" canlı göstergesi
- **Sınavlar:** Boss savaşı geri sayımları, yaklaşan / geçmiş sınavlar, girilmiş sınav notları, bildirim izni
- **Ödüller:** Karakter vitrini, rozet koleksiyonu, **Ganimet Mağazası** (XP'yi ödüle takas)

### 🛡️ Veli ekranları (PIN ile)
- **Panel:** Onay bekleyen görevler/takaslar, hızlı görev şablonları, son 7 gün grafiği
- **Görev Ata:** Görev oluştur (ders, zorluk BOSS/NORMAL, XP, son tarih) → anında Ruz'un ekranına düşer
- **Planla:** Sınav tanımla (Boss seçimi ve alarm günü ayarlanır), geçmiş sınavın notunu gir/düzenle + haftalık ders programını yönet
- **Ödül:** Mağazaya ödül ekle, takas taleplerini onayla/reddet
- **Ayarlar:** PIN değiştir, bildirim izni, **Firebase senkron**, yedek al/geri yükle, sıfırla

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

> ⚠️ Güvenlik notu: "Test mode" kuralları 30 gün sonra kapanır ve veri erişimi durur.
> Uzun vadeli kullanım için Firebase konsolunda kuralları okuma/yazma olarak güncelleyip
> tarih uzatman ya da basit kimlik doğrulama eklemen önerilir.

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
Cihazda `localStorage` temizlenirse PIN örnek değere (`1234`) döner; ya da Konsol'dan
`JSON.parse(localStorage.odevAvciStateV1).settings.pin` ile mevcut PIN'i görebilirsin.

**Telefonda bildirim gelmiyor?**
Sınavlar ekranından veya Ayarlar'dan **Bildirim İznini Aç** düğmesine bas; iOS'ta
uygulamanın ana ekrana eklenmiş olması gerekir.

**Firebase bağlanamıyor?**
`databaseURL` alanının config'de olduğundan emin ol (Realtime Database oluştur
meden alınan config'lerde bu alan olmayabilir). Ayrıca URL'nin `https://` ile
başladığını ve veritabanının oluşturulduğunu kontrol et.

---

*Ödev Avcısı v1.0 — iyi çalışmalar! 🏹*
