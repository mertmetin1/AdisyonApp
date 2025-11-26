"""
AdisyonApp Test Script
Tüm fonksiyonları test eder
"""

import sys
import time
from kivy.clock import Clock
from kivymd.app import MDApp

def test_navigation(app):
    """Navigasyon testleri"""
    print("\n=== NAVIGASYON TESTİ ===")
    screens = ["home", "products", "bills", "payments", "reports"]
    
    for screen in screens:
        try:
            app.change_screen(screen)
            print(f"✓ {screen} ekranı açıldı")
            time.sleep(0.5)
        except Exception as e:
            print(f"✗ {screen} ekranı HATA: {e}")
            return False
    
    return True

def test_drawer(app):
    """Drawer testi"""
    print("\n=== DRAWER TESTİ ===")
    try:
        app.root.ids.nav_drawer.set_state("open")
        print("✓ Drawer açıldı")
        time.sleep(0.5)
        
        app.root.ids.nav_drawer.set_state("close")
        print("✓ Drawer kapandı")
        return True
    except Exception as e:
        print(f"✗ Drawer HATA: {e}")
        return False

def test_database(app):
    """Database testi"""
    print("\n=== DATABASE TESTİ ===")
    try:
        if not app.db:
            print("✗ Database başlatılmadı")
            return False
        
        # Ürünleri kontrol et
        products = app.db.get_all_products()
        print(f"✓ {len(products)} ürün bulundu")
        
        # Adisyonları kontrol et
        bills = app.db.get_all_bills()
        print(f"✓ {len(bills)} adisyon bulundu")
        
        # Açık adisyonları kontrol et
        open_bills = app.db.get_open_bills()
        print(f"✓ {len(open_bills)} açık adisyon bulundu")
        
        return True
    except Exception as e:
        print(f"✗ Database HATA: {e}")
        return False

def test_screens_load(app):
    """Ekranların yüklenme testi"""
    print("\n=== EKRAN YÜKLEME TESTİ ===")
    
    screens_to_test = {
        "home": "HomeScreen",
        "products": "ProductsScreen",
        "bills": "BillsScreen",
        "payments": "PaymentsScreen",
        "reports": "ReportsScreen"
    }
    
    for screen_name, screen_class in screens_to_test.items():
        try:
            app.change_screen(screen_name)
            time.sleep(0.3)
            
            # Ekranın load metodlarını çalıştır
            screen = app.root.ids.screen_manager.get_screen(screen_name)
            
            if hasattr(screen, 'on_enter'):
                screen.on_enter()
                print(f"✓ {screen_class} on_enter çalıştı")
            
        except Exception as e:
            print(f"✗ {screen_class} HATA: {e}")
            return False
    
    return True

def run_tests():
    """Tüm testleri çalıştır"""
    print("\n" + "="*50)
    print("  AdisyonApp Test Başlıyor")
    print("="*50)
    
    # Uygulamayı başlat
    from main import AdisyonApp
    app = AdisyonApp()
    
    # Kısa bir bekleme - app başlasın
    def start_tests(dt):
        results = []
        
        # Testleri çalıştır
        results.append(("Database", test_database(app)))
        results.append(("Navigation", test_navigation(app)))
        results.append(("Drawer", test_drawer(app)))
        results.append(("Screen Load", test_screens_load(app)))
        
        # Sonuçları göster
        print("\n" + "="*50)
        print("  TEST SONUÇLARI")
        print("="*50)
        
        all_passed = True
        for test_name, passed in results:
            status = "✓ BAŞARILI" if passed else "✗ BAŞARISIZ"
            print(f"{test_name:20} : {status}")
            if not passed:
                all_passed = False
        
        print("="*50)
        if all_passed:
            print("  🎉 TÜM TESTLER BAŞARILI! 🎉")
        else:
            print("  ⚠️ BAZI TESTLER BAŞARISIZ")
        print("="*50 + "\n")
        
        # 2 saniye bekle ve kapat
        Clock.schedule_once(lambda dt: app.stop(), 2)
    
    # App başladıktan sonra testleri başlat
    Clock.schedule_once(start_tests, 2)
    
    app.run()

if __name__ == "__main__":
    run_tests()
