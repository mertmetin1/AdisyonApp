# AdisyonApp APK Build - Google Colab
# Colab'da çalıştır: https://colab.research.google.com

# 1. Bu hücreyi çalıştır
!pip install buildozer cython

# 2. Dosyalarını yükle
from google.colab import files
import zipfile
import os

# Proje klasörünü zip'le ve yükle
# Windows'ta: Compress-Archive -Path D:\AdisyonApp\* -DestinationPath D:\AdisyonApp.zip
print("AdisyonApp.zip dosyasını yükle...")
uploaded = files.upload()

# Zip'i aç
!unzip AdisyonApp.zip -d /content/AdisyonApp
%cd /content/AdisyonApp

# 3. Gerekli paketleri yükle
!apt-get update
!apt-get install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 4. APK oluştur
!buildozer android debug

# 5. APK'yı indir
!ls -la bin/
files.download('bin/adisyonapp-0.1-arm64-v8a-debug.apk')
