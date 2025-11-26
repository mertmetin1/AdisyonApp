# AdisyonApp - Hızlı Başlangıç 🚀

## 5 Dakikada Başlayın!

### 1️⃣ Gereksinimleri Yükleyin (1 dakika)

```bash
pip install -r requirements.txt
```

### 2️⃣ Örnek Verileri Yükleyin (30 saniye)

```bash
python test_data.py
```

Bu komut şunları oluşturur:
- ✅ 15 örnek ürün (kahveler, tatlılar, içecekler)
- ✅ 5 örnek adisyon (açık, kısmi ödemeli, kapalı)
- ✅ Çalışan bir veritabanı

### 3️⃣ Uygulamayı Başlatın (5 saniye)

```bash
python start.py
```

veya

```bash
python main.py
```

## 🎯 İlk Adımlar

### ✨ Ana Sayfadan Başlayın
Uygulama açılır açılmaz **Ana Sayfa** görünür:
- Bugünün istatistiklerini görün
- Hızlı erişim kartlarını kullanın

### 📦 Ürün Ekleyin
1. Sol menüden **"Ürünler"** seçin
2. Sağ üst köşedeki **+** butonuna tıklayın
3. Bilgileri doldurun ve **EKLE**

### 📝 Adisyon Oluşturun
1. Sol menüden **"Adisyonlar"** seçin
2. **+** butonuyla yeni adisyon
3. Müşteri adını girin
4. **ÜRÜN EKLE** ile ürünleri seçin

### 💰 Ödeme Alın
1. Adisyon listesinde **💰** ikonuna tıklayın
2. Tutarı girin (varsayılan: kalan tutar)
3. **ÖDEME AL** butonuna basın

### 📊 Raporları Görün
1. Sol menüden **"Raporlar"**
2. Günlük/Aylık/Kar-Zarar raporlarını inceleyin

## 🎨 Özellikler Bir Bakışta

| Özellik | Açıklama |
|---------|----------|
| 🍵 **Ürün Yönetimi** | Ekle, düzenle, sil, resim ekle |
| 📝 **Adisyon** | Müşteri bazlı sipariş takibi |
| 💰 **Ödeme** | Nakit/Kart, kısmi ödeme |
| 📊 **Raporlar** | Satış, kar/zarar analizi |
| 🎯 **Kar Marjı** | Otomatik hesaplama |
| 📱 **Cross-Platform** | Masaüstü + Android APK |

## 📱 Android APK Derlemek İçin

**Not:** Sadece Linux/macOS üzerinde yapılabilir

```bash
# Buildozer'ı yükleyin
pip install buildozer

# APK derleyin (ilk seferde 1-2 saat sürer)
buildozer -v android debug

# APK dosyası bin/ klasöründe oluşur
```

Detaylar için: [APK_BUILD.md](APK_BUILD.md)

## 📚 Dokümantasyon

- 📖 **[README.md](README.md)** - Genel bilgiler ve kurulum
- 📘 **[KULLANIM_KILAVUZU.md](KULLANIM_KILAVUZU.md)** - Detaylı kullanım talimatları
- 📗 **[APK_BUILD.md](APK_BUILD.md)** - Android APK derleme rehberi

## 🐛 Sorun mu Yaşıyorsunuz?

### Kivy yüklenemiyor?
```bash
pip install --upgrade pip
pip install kivy==2.3.0 kivymd==1.2.0
```

### Veritabanı hatası?
```bash
python test_data.py clear  # Veritabanını temizle
python test_data.py        # Yeniden oluştur
```

### Uygulama açılmıyor?
```bash
python start.py  # Bu kontrollü başlatma yapar
```

## 💡 Örnekler

### Kahve Dükkanı Senaryosu

1. **Sabah Hazırlığı:**
   ```bash
   python main.py
   ```
   - Ürünleri kontrol et
   - Stokları gözden geçir

2. **Müşteri Geldi:**
   - "Adisyonlar" → + → "Ahmet Bey"
   - Ürün ekle: 2x Türk Kahvesi, 1x Croissant
   - Toplam: ₺70

3. **Ödeme Al:**
   - 💰 ikonu → ₺70 → ÖDEME AL
   - Adisyon otomatik kapanır

4. **Gün Sonu:**
   - "Raporlar" → Günlük rapor
   - Kar/zarar analizi

## 🎓 İpuçları

✅ **Kategoriler kullanın** - Ürünleri gruplandırın
✅ **Maliyet girin** - Kar marjını hesaplayın
✅ **Notlar ekleyin** - Özel istekleri kaydedin
✅ **Düzenli yedekleyin** - `database/adisyon.db` dosyasını

## 🚀 Sonraki Adımlar

1. ✨ Kendi ürünlerinizi ekleyin
2. 🎨 Tema renklerini değiştirin (main.py)
3. 📱 Android APK derleyin
4. 🌟 Uygulamayı özelleştirin

## 💬 Yardım

- 📧 Issue açın (GitHub)
- 📖 KULLANIM_KILAVUZU.md'yi okuyun
- 🔍 README.md'de arayın

---

**Başarılar!** ☕️

**Not:** İlk kullanımda `python test_data.py` komutunu çalıştırmayı unutmayın!
