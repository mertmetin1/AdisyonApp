# AdisyonApp - APK Oluşturma Kılavuzu

Bu dosya, AdisyonApp projesinden Android APK dosyası oluşturmak için gereken tüm adımları içerir.

---

## 📋 İçindekiler
1. [WSL ile APK Oluşturma (ÖNERİLEN)](#1-wsl-ile-apk-oluşturma-önerilen)
2. [Kali Linux ile APK Oluşturma](#2-kali-linux-ile-apk-oluşturma)
3. [GitHub Actions ile Otomatik Build](#3-github-actions-ile-otomatik-build)
4. [Google Colab ile APK Oluşturma](#4-google-colab-ile-apk-oluşturma)
5. [Sorun Giderme](#5-sorun-giderme)

---

## 1. WSL ile APK Oluşturma (ÖNERİLEN)

### Adım 1.1: WSL'i Başlat
```bash
# Windows PowerShell'de WSL'i başlat
wsl
```

### Adım 1.2: Proje Dizinine Git
```bash
cd /mnt/d/AdisyonApp
```

### Adım 1.3: Gerekli Paketleri Kur (İlk Seferlik)
```bash
sudo apt-get update
sudo apt-get install -y \
    git \
    zip \
    unzip \
    openjdk-17-jdk \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    cmake \
    libffi-dev \
    libssl-dev \
    python3 \
    python3-pip
```

### Adım 1.4: Buildozer Kur (İlk Seferlik)
```bash
pip3 install --upgrade pip
pip3 install buildozer cython
```

### Adım 1.5: APK Oluştur
```bash
# APK oluşturma (10-15 dakika sürer)
buildozer android debug

# İlerlemeyi izle - şunları göreceksin:
# - Android SDK indirme
# - Android NDK indirme
# - Python-for-Android derleme
# - APK paketleme
```

### Adım 1.6: APK'yı Bul
```bash
# APK'yı listele
ls -la bin/

# APK dosyası:
# bin/adisyonapp-1.0.0-arm64-v8a_armeabi-v7a-debug.apk
```

APK dosyası Windows'ta: `D:\AdisyonApp\bin\` klasöründe!

---

## 2. Kali Linux ile APK Oluşturma

### Adım 2.1: Projeyi Klonla
```bash
cd ~
git clone https://github.com/mertmetin1/AdisyonApp.git
cd AdisyonApp
```

### Adım 2.2: Gerekli Paketleri Kur
```bash
sudo apt-get update
sudo apt-get install -y \
    git \
    zip \
    unzip \
    openjdk-17-jdk \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    cmake \
    libffi-dev \
    libssl-dev \
    python3 \
    python3-pip
```

### Adım 2.3: Buildozer Kur
```bash
pip3 install --upgrade pip
pip3 install buildozer cython
```

### Adım 2.4: APK Oluştur
```bash
buildozer android debug
```

### Adım 2.5: APK'yı Bul
```bash
ls -la bin/
# APK: bin/adisyonapp-1.0.0-arm64-v8a_armeabi-v7a-debug.apk
```

---

## 3. GitHub Actions ile Otomatik Build

### Adım 3.1: Kod Değişikliklerini Push'la
```bash
# Windows PowerShell'de
cd D:\AdisyonApp
git add .
git commit -m "Update: [değişiklik açıklaması]"
git push
```

### Adım 3.2: GitHub Actions'ı Başlat
1. https://github.com/mertmetin1/AdisyonApp/actions adresine git
2. "Build Android APK" workflow'unu seç
3. "Run workflow" butonuna tıkla
4. "Run workflow" (yeşil buton) tıkla

### Adım 3.3: Build'i İzle
- Build çalışırken sarı ⚪ işareti göreceksin
- Tamamlanınca yeşil ✅ olacak
- Hata varsa kırmızı ❌ olacak
- **Süre:** ~10-15 dakika

### Adım 3.4: APK'yı İndir
1. Build tamamlanınca workflow'a tıkla
2. En altta "Artifacts" bölümünde `AdisyonApp-debug.apk` göreceksin
3. İndir (zip olarak gelir)
4. Zip'i aç, APK'yı çıkar

---

## 4. Google Colab ile APK Oluşturma

### Adım 4.1: Colab'ı Aç
1. https://colab.research.google.com adresine git
2. Yeni notebook oluştur

### Adım 4.2: Projeyi Zip'le
```powershell
# Windows PowerShell'de
cd D:\
Compress-Archive -Path D:\AdisyonApp\* -DestinationPath D:\AdisyonApp.zip -Force
```

### Adım 4.3: Colab'da Buildozer Kur
```python
!pip install buildozer cython
```

### Adım 4.4: Zip'i Yükle
```python
from google.colab import files
import zipfile

# Zip'i yükle
print("AdisyonApp.zip dosyasını yükle...")
uploaded = files.upload()

# Zip'i aç
!unzip -q AdisyonApp.zip -d /content/AdisyonApp
%cd /content/AdisyonApp
```

### Adım 4.5: Gerekli Paketleri Kur
```python
!apt-get update
!apt-get install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev cmake libffi-dev libssl-dev
```

### Adım 4.6: APK Oluştur
```python
!buildozer android debug
```

### Adım 4.7: APK'yı İndir
```python
!ls -la bin/
files.download('bin/adisyonapp-1.0.0-arm64-v8a_armeabi-v7a-debug.apk')
```

---

## 5. Sorun Giderme

### Hata: "Command failed: buildozer"
**Çözüm:** Buildozer kurulu değil
```bash
pip3 install --upgrade buildozer cython
```

### Hata: "Java not found"
**Çözüm:** JDK kurulu değil
```bash
sudo apt-get install -y openjdk-17-jdk
```

### Hata: "SDK License not accepted"
**Çözüm:** `buildozer.spec` dosyasında licenses otomatik kabul ediliyor, sorun olmamalı.

### Hata: "Permission denied"
**Çözüm:** Buildozer klasörünü temizle
```bash
rm -rf .buildozer
buildozer android debug
```

### Build Çok Uzun Sürüyor
**Normal:** İlk build 15-20 dakika sürebilir çünkü:
- Android SDK indiriyor (~500MB)
- Android NDK indiriyor (~1GB)
- Python-for-Android derliyor

**Sonraki build'ler:** 3-5 dakika sürer (cache kullanır)

### APK Çalışmıyor
**Kontrol Et:**
1. Android sürümü 7.0+ olmalı
2. "Bilinmeyen kaynaklardan yükleme" açık olmalı
3. STORAGE izni verilmeli (ayarlarda)

---

## 📱 APK'yı Telefona Yükleme

### Adım 1: APK'yı Telefona Kopyala
- USB ile kopyala
- WhatsApp/Telegram ile gönder
- Google Drive/Dropbox kullan

### Adım 2: APK'yı Yükle
1. Telefonda APK dosyasına dokun
2. "Bilinmeyen kaynaklardan yükleme" izni ver
3. "Yükle" butonuna bas
4. "Aç" butonuna bas

### Adım 3: İzinleri Ver
- STORAGE izni (veritabanı için)
- CAMERA izni (ürün fotoğrafı için)

---

## 🎯 Hızlı Başlangıç (ChatGPT için Talimatlar)

ChatGPT'ye şunu söyle:

```
"AdisyonApp projesinden APK oluştur. Proje: D:\AdisyonApp

WSL kullanarak:
1. cd /mnt/d/AdisyonApp
2. Gerekli paketleri kur (apt-get install...)
3. buildozer android debug çalıştır
4. bin/ klasöründeki APK'yı bul

Sorun çıkarsa APK_OLUSTURMA_KILAVUZU.md dosyasına bak."
```

---

## 📝 Notlar

- **İlk build:** 15-20 dakika
- **Sonraki build'ler:** 3-5 dakika
- **APK boyutu:** ~50-60 MB
- **Minimum Android:** 7.0 (API 24)
- **Hedef mimariler:** ARM64, ARMv7

---

## 🔗 Faydalı Linkler

- GitHub Repo: https://github.com/mertmetin1/AdisyonApp
- Buildozer Docs: https://buildozer.readthedocs.io
- Python-for-Android: https://python-for-android.readthedocs.io
- Kivy Docs: https://kivy.org/doc/stable/

---

**Son Güncelleme:** 26 Kasım 2025
**Proje Versiyonu:** 1.0.0
