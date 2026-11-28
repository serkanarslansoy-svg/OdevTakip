# 🏹 Ödev Avcısı

Ortaokula giden bir öğrenci için oyunlaştırılmış **ödev ve sınav takip** uygulaması.
Öğrenci görevleri tamamlayıp XP ve altın kazanır, veli ("Komutan") onaylar, ödevleri atar ve
sınavları planlar. Okulun **Argo DidUP** sistemindeki ödevler, öğretmen hatırlatmaları
(promemoria) ve notlar otomatik olarak çekilip veli onayına düşer.

**Uygulama:** https://serkanarslansoy-svg.github.io/OdevTakip/

## Belgeler

| Dosya | Kimin için | İçerik |
|---|---|---|
| [`KURULUM.md`](KURULUM.md) | Kullanıcı (veli) | Kurulum, kullanım, Firebase ve Argo ayarları, SSS |
| [`CLAUDE.md`](CLAUDE.md) | Geliştirici / yapay zekâ asistanı | Projenin tam hafızası: kurallar, mimari, veri modeli, Argo entegrasyonu, test, geçmiş |

## Kısaca teknik yapı

- `index.html`: uygulamanın tamamı (tek dosya, derleme yok; Tailwind CDN, Firebase Realtime DB).
- `scripts/argo_sync.py` + `.github/workflows/argo-sync.yml`: Argo → Firebase senkronu
  (GitHub Actions, günde 4 kez + elle).
- `capacitor.config.js`, `.github/workflows/build-apk.yml`: siteyi açan Android sarmalayıcı.
- Yayın: `main` dalı → GitHub Pages.

Gizli bilgiler (Argo ve Firebase giriş bilgileri) yalnızca GitHub Secrets'tadır; depoda bulunmaz.
