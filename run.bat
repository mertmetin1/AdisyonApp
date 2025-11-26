@echo off
chcp 65001 > nul
cls

echo ====================================
echo     AdisyonApp Başlatıcı
echo ====================================
echo.

REM Python kontrolü
python --version > nul 2>&1
if errorlevel 1 (
    echo [HATA] Python bulunamadı!
    echo Lütfen Python 3.9 veya üzeri yükleyin: https://python.org
    pause
    exit /b 1
)

echo [✓] Python bulundu
echo.

REM Sanal ortam kontrolü
if not exist "venv" (
    echo [i] Sanal ortam bulunamadı, oluşturuluyor...
    python -m venv venv
    if errorlevel 1 (
        echo [HATA] Sanal ortam oluşturulamadı!
        pause
        exit /b 1
    )
    echo [✓] Sanal ortam oluşturuldu
    echo.
)

REM Sanal ortamı aktifleştir
call venv\Scripts\activate.bat

REM Gereksinimleri kontrol et
pip show kivy > nul 2>&1
if errorlevel 1 (
    echo [i] Gereksinimler yüklenecek (biraz zaman alabilir)...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [HATA] Gereksinimler yüklenemedi!
        pause
        exit /b 1
    )
    echo.
    echo [✓] Gereksinimler yüklendi
    echo.
)

REM Veritabanı kontrolü
if not exist "database\adisyon.db" (
    echo [i] Veritabanı bulunamadı!
    echo.
    set /p response="Örnek veriler eklensin mi? (E/H): "
    if /i "%response%"=="E" (
        echo.
        echo [i] Örnek veriler ekleniyor...
        python test_data.py
        echo.
    )
)

REM Uygulamayı başlat
echo [i] Uygulama başlatılıyor...
echo.
python main.py

REM Hata durumunda bekle
if errorlevel 1 (
    echo.
    echo [HATA] Uygulama beklenmedik şekilde kapandı!
    pause
)

deactivate
