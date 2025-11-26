#!/bin/bash
# AdisyonApp APK Build Script for WSL/Linux

echo "🔧 AdisyonApp APK Build Başlıyor..."

# Sistem güncellemesi
sudo apt-get update
sudo apt-get upgrade -y

# Java ve build araçlarını yükle
sudo apt-get install -y \
    git zip unzip openjdk-17-jdk \
    autoconf libtool pkg-config \
    zlib1g-dev libncurses5-dev libncursesw5-dev \
    libtinfo5 cmake libffi-dev libssl-dev \
    python3 python3-pip

# Buildozer ve Cython yükle
pip3 install --upgrade pip
pip3 install buildozer cython

# Buildozer ile APK oluştur
echo "📦 APK oluşturuluyor..."
buildozer android debug

# Sonuç
if [ -f "bin/*.apk" ]; then
    echo "✅ APK başarıyla oluşturuldu!"
    ls -lh bin/*.apk
else
    echo "❌ APK oluşturulamadı, hataları kontrol et"
fi
