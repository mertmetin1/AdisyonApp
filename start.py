"""
Uygulamayı başlatma scripti
Gerekli kontrolleri yapıp uygulamayı çalıştırır
"""

import os
import sys


def check_requirements():
    """Gereksinimleri kontrol et"""
    print("🔍 Gereksinimler kontrol ediliyor...")
    
    required_modules = ['kivy', 'kivymd', 'PIL']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✓ {module} bulundu")
        except ImportError:
            missing_modules.append(module)
            print(f"  ✗ {module} bulunamadı")
    
    if missing_modules:
        print("\n❌ Eksik modüller bulundu!")
        print("Lütfen şu komutu çalıştırın:")
        print("  pip install -r requirements.txt")
        return False
    
    print("✅ Tüm gereksinimler karşılandı!\n")
    return True


def check_database():
    """Veritabanı dosyasını kontrol et"""
    db_path = "database/adisyon.db"
    
    if not os.path.exists(db_path):
        print("ℹ️  Veritabanı bulunamadı, otomatik oluşturulacak...")
        
        # Örnek veri eklemek ister misiniz?
        response = input("Örnek test verileri eklemek ister misiniz? (E/H): ").strip().upper()
        
        if response == 'E':
            print("\n📦 Örnek veriler ekleniyor...")
            try:
                import test_data
                test_data.add_sample_data()
                print("✅ Örnek veriler eklendi!\n")
            except Exception as e:
                print(f"⚠️  Örnek veri eklenirken hata: {e}\n")
        else:
            print("ℹ️  Boş veritabanı oluşturulacak...\n")
    else:
        print("✅ Veritabanı bulundu!\n")


def start_app():
    """Uygulamayı başlat"""
    print("=" * 60)
    print("AdisyonApp - Kahve Dükkanı Adisyon Sistemi")
    print("=" * 60)
    print()
    
    # Gereksinimleri kontrol et
    if not check_requirements():
        sys.exit(1)
    
    # Veritabanını kontrol et
    check_database()
    
    # Uygulamayı başlat
    print("🚀 Uygulama başlatılıyor...\n")
    
    try:
        import main
        main.AdisyonApp().run()
    except KeyboardInterrupt:
        print("\n\n👋 Uygulama kapatılıyor...")
    except Exception as e:
        print(f"\n❌ Hata oluştu: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    start_app()
