# AdisyonApp - Kahve Dükkanı Adisyon Yönetim Sistemi

## 📱 Açıklama

**AdisyonApp**, butik kahve dükkanları için geliştirilmiş, modern ve kullanımı kolay bir adisyon yönetim sistemidir. Python ve Kivy/KivyMD ile geliştirilmiş olup hem masaüstü hem de mobil (Android) platformlarda çalışır.

## ✨ Özellikler

### 🍵 Ürün Yönetimi
- Ürün ekleme, düzenleme ve silme
- Ürün resimleri ekleme
- Maliyet fiyatı ve satış fiyatı takibi
- Otomatik kar marjı hesaplama
- Kategori ve stok yönetimi
- Ürün arama ve filtreleme

### 📝 Adisyon Yönetimi
- Müşteri adına adisyon açma
- Masa numarası takibi
- Adisyona ürün ekleme/çıkarma
- Açık ve kapalı adisyon listesi
- Adisyon detay görüntüleme
- Adisyon notları

### 💰 Ödeme Takibi
- Nakit, kart ve havale ödeme yöntemleri
- Kısmi ödeme desteği
- Ödeme geçmişi
- Kalan bakiye hesaplama
- Otomatik adisyon kapatma

### 📊 Raporlama ve Analiz
- Günlük satış raporları
- Aylık satış raporları
- Kar/zarar analizi (7 günlük)
- En çok satan ürünler
- Ödeme yöntemi dağılımı
- Detaylı istatistikler

## 🛠️ Teknoloji Stack

- **Python 3.9+**: Ana programlama dili
- **Kivy 2.3.0**: Cross-platform UI framework
- **KivyMD 1.2.0**: Material Design bileşenleri
- **SQLite**: Yerel veritabanı
- **Pillow**: Resim işleme
- **Buildozer**: APK derleme aracı

## 📦 Kurulum

### Masaüstü için (Windows/Linux/Mac)

1. **Repoyu klonlayın:**
```bash
git clone <repo-url>
cd AdisyonApp
```

2. **Sanal ortam oluşturun (önerilir):**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

3. **Gereksinimleri yükleyin:**
```bash
pip install -r requirements.txt
```

4. **Uygulamayı çalıştırın:**
```bash
python main.py
```

### Android APK Derleme (Linux/Mac)

1. **Buildozer'ı yükleyin:**
```bash
pip install buildozer
```

2. **Android gereksinimlerini yükleyin:**
```bash
buildozer android debug
```

3. **APK dosyasını derleyin:**
```bash
buildozer -v android debug
```

APK dosyası `bin/` klasöründe oluşturulacaktır.

## 📁 Proje Yapısı

```
AdisyonApp/
├── main.py                 # Ana uygulama dosyası
├── requirements.txt        # Python bağımlılıkları
├── buildozer.spec         # Android build konfigürasyonu
│
├── src/
│   └── database.py        # Veritabanı yönetimi
│
├── screens/
│   ├── home_screen.py     # Ana sayfa
│   ├── products_screen.py # Ürün yönetimi
│   ├── bills_screen.py    # Adisyon yönetimi
│   ├── payments_screen.py # Ödeme takibi
│   └── reports_screen.py  # Raporlama
│
├── assets/
│   ├── images/            # Ürün resimleri
│   └── icons/             # Uygulama ikonları
│
└── database/
    └── adisyon.db         # SQLite veritabanı
```

## 🎯 Kullanım

### İlk Kurulum
1. Uygulamayı ilk çalıştırdığınızda veritabanı otomatik oluşturulur
2. Ana sayfadan hızlı erişim menüsünü kullanabilirsiniz

### Ürün Ekleme
1. "Ürünler" menüsüne gidin
2. Sağ üst köşedeki "+" butonuna tıklayın
3. Ürün bilgilerini girin (ad, fiyat, maliyet, vb.)
4. İsteğe bağlı olarak ürün resmi ekleyin
5. "EKLE" butonuna tıklayın

### Adisyon Oluşturma
1. "Adisyonlar" menüsüne gidin
2. Sağ üst köşedeki "+" butonuna tıklayın
3. Müşteri adını ve masa numarasını girin
4. Adisyona tıklayarak detaylara gidin
5. "ÜRÜN EKLE" butonu ile ürün ekleyin

### Ödeme Alma
1. Adisyon listesinden ödeme alınacak adisyonu seçin
2. Sağdaki "💰" ikonuna veya "ÖDEME AL" butonuna tıklayın
3. Ödeme tutarını girin (varsayılan: kalan tutar)
4. Ödeme yöntemini seçin
5. "ÖDEME AL" butonuna tıklayın

### Raporları Görüntüleme
1. "Raporlar" menüsüne gidin
2. Günlük, aylık veya kar/zarar raporlarını görüntüleyin
3. Detaylı raporlar için ilgili butona tıklayın

## 🔧 Yapılandırma

### Veritabanı Yolu
`src/database.py` dosyasındaki `Database` sınıfında varsayılan yol:
```python
db_path = "database/adisyon.db"
```

### Pencere Boyutu (Masaüstü)
`main.py` dosyasında:
```python
Window.size = (400, 700)  # Mobil boyut simülasyonu
```

### Tema Renkleri
`main.py` içinde tema ayarları:
```python
self.theme_cls.primary_palette = "Brown"
self.theme_cls.accent_palette = "Amber"
```

## 📱 Android İzinleri

buildozer.spec dosyasında tanımlı izinler:
- `WRITE_EXTERNAL_STORAGE`: Ürün resimlerini kaydetmek için
- `READ_EXTERNAL_STORAGE`: Ürün resimlerini okumak için
- `CAMERA`: Kamera ile resim çekmek için (opsiyonel)

## 🐛 Bilinen Sorunlar ve Çözümler

### Kivy/KivyMD Import Hataları
Bu hatalar geliştirme ortamında normaldir. Uygulama çalışır durumda olduğunda sorun olmayacaktır.

### Android'de Veritabanı Yolu
Android'de veritabanı internal storage'da saklanır. Uygulama kaldırıldığında veriler silinir.

### Resim Yükleme
- Desteklenen formatlar: PNG, JPG, JPEG
- Önerilen boyut: 512x512 piksel
- Android'de galeriden veya kameradan resim seçilebilir

## 🚀 Performans İpuçları

1. **Ürün Sayısı**: 1000'den fazla ürün için sayfalama ekleyin
2. **Resim Boyutu**: Resimleri optimize edin (max 1MB)
3. **Veritabanı**: Düzenli olarak VACUUM işlemi yapın
4. **Eski Kayıtlar**: 1 yıldan eski kayıtları arşivleyin

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👨‍💻 Geliştirici

AdisyonApp - Butik kahve dükkanları için modern adisyon sistemi

## 🤝 Katkıda Bulunma

1. Bu repoyu fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📞 Destek

Sorularınız veya sorunlarınız için issue açabilirsiniz.

---

**Not:** Bu uygulama butik kahve dükkanları için özelleştirilmiş olup, ihtiyaçlarınıza göre özelleştirilebilir.
