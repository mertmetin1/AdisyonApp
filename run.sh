#!/bin/bash

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "===================================="
echo "     AdisyonApp Başlatıcı"
echo "===================================="
echo ""

# Python kontrolü
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[HATA] Python3 bulunamadı!${NC}"
    echo "Lütfen Python 3.9 veya üzeri yükleyin"
    exit 1
fi

echo -e "${GREEN}[✓] Python bulundu${NC}"
echo ""

# Sanal ortam kontrolü
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}[i] Sanal ortam oluşturuluyor...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}[HATA] Sanal ortam oluşturulamadı!${NC}"
        exit 1
    fi
    echo -e "${GREEN}[✓] Sanal ortam oluşturuldu${NC}"
    echo ""
fi

# Sanal ortamı aktifleştir
source venv/bin/activate

# Gereksinimleri kontrol et
if ! pip show kivy &> /dev/null; then
    echo -e "${YELLOW}[i] Gereksinimler yükleniyor...${NC}"
    echo ""
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}[HATA] Gereksinimler yüklenemedi!${NC}"
        exit 1
    fi
    echo ""
    echo -e "${GREEN}[✓] Gereksinimler yüklendi${NC}"
    echo ""
fi

# Veritabanı kontrolü
if [ ! -f "database/adisyon.db" ]; then
    echo -e "${YELLOW}[i] Veritabanı bulunamadı!${NC}"
    echo ""
    read -p "Örnek veriler eklensin mi? (E/H): " response
    if [[ "$response" =~ ^[Ee]$ ]]; then
        echo ""
        echo -e "${YELLOW}[i] Örnek veriler ekleniyor...${NC}"
        python3 test_data.py
        echo ""
    fi
fi

# Uygulamayı başlat
echo -e "${GREEN}[i] Uygulama başlatılıyor...${NC}"
echo ""
python3 main.py

# Hata kontrolü
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}[HATA] Uygulama beklenmedik şekilde kapandı!${NC}"
    read -p "Devam etmek için Enter'a basın..."
fi

deactivate
