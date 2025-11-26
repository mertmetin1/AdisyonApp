# Android APK Build Kılavuzu

## 📱 Genel Bakış

Bu kılavuz, AdisyonApp uygulamasının Android APK dosyasını oluşturmak için gerekli adımları detaylı şekilde açıklar.

## ⚠️ Önemli Notlar

- APK derleme işlemi **sadece Linux veya macOS** üzerinde yapılabilir
- Windows kullanıcıları WSL2 (Windows Subsystem for Linux) kullanabilir
- İlk derleme 1-2 saat sürebilir (bağımlılıklar indirilir)
- En az 10 GB boş disk alanı gereklidir

## 🛠️ Gereksinimler

### Sistem Gereksinimleri (Linux/macOS)

```bash
# Python 3.9 veya üzeri
python3 --version

# pip
pip3 --version

# Git
git --version

# Java JDK 8 veya 11
java -version

# Android SDK (buildozer otomatik indirir)
```

### Ubuntu/Debian için Ek Paketler

```bash
sudo apt update
sudo apt install -y \
    python3-pip \
    build-essential \
    git \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    libgstreamer1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    libgstreamer-plugins-base1.0-dev \
    zip \
    unzip \
    openjdk-11-jdk \
    autoconf \
    libtool \
    pkg-config
```

### macOS için Homebrew Paketleri

```bash
brew install \
    python3 \
    git \
    autoconf \
    automake \
    libtool \
    pkg-config \
    sdl2 \
    sdl2_image \
    sdl2_mixer \
    sdl2_ttf
```

## 📦 Buildozer Kurulumu

### 1. Buildozer'ı Yükleyin

```bash
pip3 install --upgrade buildozer
```

### 2. Cython'u Yükleyin

```bash
pip3 install --upgrade cython
```

### 3. Kurulumu Kontrol Edin

```bash
buildozer --version
```

## 🚀 APK Derleme Adımları

### Adım 1: Proje Dizinine Gidin

```bash
cd AdisyonApp
```

### Adım 2: buildozer.spec Dosyasını Kontrol Edin

`buildozer.spec` dosyası zaten yapılandırılmış durumda. İsteğe bağlı olarak şu ayarları değiştirebilirsiniz:

```ini
# Uygulama adı
title = AdisyonApp

# Paket adı (benzersiz olmalı)
package.name = adisyonapp
package.domain = org.adisyon

# Versiyon
version = 1.0.0

# İzinler
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,CAMERA

# Android API seviyeleri
android.api = 33
android.minapi = 21

# Mimari (ARM 64-bit ve 32-bit)
android.archs = arm64-v8a,armeabi-v7a
```

### Adım 3: İlk Derleme (Debug APK)

```bash
buildozer -v android debug
```

**Not:** 
- İlk derleme uzun sürecektir (1-2 saat)
- Android SDK, NDK ve bağımlılıklar indirilecek
- `-v` parametresi detaylı log verir

### Adım 4: APK Dosyasını Bulun

Derleme başarılı olursa APK dosyası şurada oluşur:

```
AdisyonApp/bin/adisyonapp-1.0.0-arm64-v8a-debug.apk
```

### Adım 5: APK'yı Telefona Yükleyin

#### USB ile:

```bash
# ADB yüklü olmalı
adb install bin/adisyonapp-1.0.0-arm64-v8a-debug.apk
```

#### Manuel Yükleme:

1. APK dosyasını telefona kopyalayın
2. Dosya yöneticisi ile APK'yı açın
3. "Bilinmeyen kaynaklardan yükleme"ye izin verin
4. Kurulumu tamamlayın

## 🔐 Release APK (Yayın Sürümü)

Release APK oluşturmak için keystore gereklidir.

### Adım 1: Keystore Oluşturun

```bash
keytool -genkey -v \
    -keystore adisyon-release.keystore \
    -alias adisyon \
    -keyalg RSA \
    -keysize 2048 \
    -validity 10000
```

Şu bilgiler sorulacak:
- Keystore şifresi
- Ad, organizasyon, şehir, ülke vb.

**ÖNEMLİ:** Keystore dosyasını ve şifresini güvenli saklayın!

### Adım 2: buildozer.spec'i Güncelleyin

buildozer.spec dosyasına ekleyin:

```ini
[app]
# ... mevcut ayarlar ...

# Release keystore
android.release_artifact = apk
android.keystore = adisyon-release.keystore
android.keystore_alias = adisyon
android.keystore_password = <ŞİFRENİZ>
android.key_alias_password = <ŞİFRENİZ>
```

### Adım 3: Release APK Derleyin

```bash
buildozer -v android release
```

Release APK:
```
bin/adisyonapp-1.0.0-arm64-v8a-release.apk
```

## 🐛 Sorun Giderme

### Hata: "Command failed"

```bash
# Buildozer'ı temizle
buildozer android clean

# Cache'i temizle
rm -rf .buildozer

# Tekrar deneyin
buildozer -v android debug
```

### Hata: "SDK/NDK not found"

```bash
# Android bileşenlerini yeniden indir
buildozer android clean
buildozer android update
```

### Hata: "Permission denied"

```bash
# buildozer.spec dosyasında izinleri kontrol edin
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
```

### Hata: "Out of memory"

```bash
# buildozer.spec'te heap size artırın
android.gradle_dependencies = 

# Veya daha az mimari için derleyin
android.archs = arm64-v8a  # Sadece 64-bit
```

### Derleme Çok Yavaş

```bash
# Paralel derleme aktif et
# buildozer.spec içine ekleyin:
android.ant_path = ~/.buildozer/android/platform/apache-ant-1.9.4
android.skip_update = False
```

## 📱 APK Boyutunu Küçültme

### 1. Tek Mimari için Derle

```ini
# buildozer.spec
android.archs = arm64-v8a  # Sadece 64-bit
```

### 2. ProGuard Kullanın

```ini
# buildozer.spec
android.release_artifact = aab  # Android App Bundle
```

### 3. Gereksiz Dosyaları Hariç Tutun

```ini
# buildozer.spec
source.exclude_exts = spec
source.exclude_dirs = tests, bin, venv, __pycache__
source.exclude_patterns = *.pyc, *.pyo, *.log
```

## 🚢 Google Play Store'a Yükleme

### 1. App Bundle (AAB) Oluşturun

```bash
buildozer android release
```

### 2. Play Console'a Gidin

1. https://play.google.com/console adresine gidin
2. "Uygulama oluştur" seçeneğine tıklayın
3. AAB dosyasını yükleyin

### 3. Store Listesi Hazırlayın

- Uygulama açıklaması
- Ekran görüntüleri
- Simge (512x512 PNG)
- Öne çıkan grafik (1024x500)
- Gizlilik politikası

## 📊 APK Analizi

### APK Boyutunu Kontrol Edin

```bash
ls -lh bin/adisyonapp-*.apk
```

### APK İçeriğini İnceleyin

```bash
unzip -l bin/adisyonapp-*.apk
```

### APK'yı Test Edin

```bash
# Emulator'da test
adb install bin/adisyonapp-*.apk
adb logcat | grep python
```

## 🔄 Güncelleme Süreci

### Versiyon Güncellemesi

```ini
# buildozer.spec
version = 1.0.1  # Versiyonu artırın
```

### Yeni APK Derleyin

```bash
buildozer android clean
buildozer -v android release
```

## 📝 Checklist (Yayın Öncesi)

- [ ] Tüm özellikler test edildi
- [ ] Veritabanı migration'ları çalışıyor
- [ ] Resimler ve assetler eklendi
- [ ] İzinler doğru yapılandırıldı
- [ ] Keystore güvenli saklandı
- [ ] Versiyon numarası güncellendi
- [ ] buildozer.spec kontrol edildi
- [ ] APK boyutu makul (<50 MB)
- [ ] Farklı cihazlarda test edildi
- [ ] Gizlilik politikası hazırlandı

## 🆘 Yardım

### Buildozer Dokümantasyonu
https://buildozer.readthedocs.io/

### Kivy Android Dokümantasyonu
https://kivy.org/doc/stable/guide/packaging-android.html

### Topluluk Desteği
https://github.com/kivy/buildozer/issues

---

## 💡 İpuçları

1. **İlk derleme uzun sürer**: Sabırlı olun, sonraki derlemeler daha hızlıdır.

2. **Cache kullanın**: `.buildozer` klasörünü silmeyin, tekrar derleme hızlanır.

3. **Logları inceleyin**: `-v` parametresi ile detaylı log alın.

4. **Temiz derleme**: Sorun yaşarsanız `clean` komutunu kullanın.

5. **WSL2 kullanın**: Windows'ta Linux ortamı için WSL2 ideal.

6. **Sanal makine**: VirtualBox veya VMware ile Ubuntu kullanabilirsiniz.

---

**Son Güncelleme:** 26 Kasım 2025
**Buildozer Versiyon:** 1.5.0
**Kivy Versiyon:** 2.3.0
