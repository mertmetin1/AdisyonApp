"""
Test scripti ve örnek veri ekleme
Uygulamayı ilk kullanımda test etmek için örnek veriler ekler
"""

import sys
import os

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.database import Database


def add_sample_data():
    """Örnek test verileri ekle"""
    
    print("🔄 Veritabanı başlatılıyor...")
    db = Database()
    
    print("\n✅ Veritabanı bağlantısı başarılı!")
    
    # Örnek ürünler ekle
    print("\n📦 Örnek ürünler ekleniyor...")
    
    products = [
        {
            'name': 'Türk Kahvesi',
            'sale_price': 25.00,
            'cost_price': 8.00,
            'description': 'Geleneksel Türk kahvesi',
            'category': 'Sıcak İçecekler',
            'stock_quantity': 100
        },
        {
            'name': 'Filtre Kahve',
            'sale_price': 30.00,
            'cost_price': 10.00,
            'description': 'El yapımı filtre kahve',
            'category': 'Sıcak İçecekler',
            'stock_quantity': 80
        },
        {
            'name': 'Cappuccino',
            'sale_price': 35.00,
            'cost_price': 12.00,
            'description': 'İtalyan usulü cappuccino',
            'category': 'Sıcak İçecekler',
            'stock_quantity': 90
        },
        {
            'name': 'Latte',
            'sale_price': 35.00,
            'cost_price': 12.00,
            'description': 'Kremalı latte',
            'category': 'Sıcak İçecekler',
            'stock_quantity': 90
        },
        {
            'name': 'Espresso',
            'sale_price': 20.00,
            'cost_price': 7.00,
            'description': 'Yoğun espresso',
            'category': 'Sıcak İçecekler',
            'stock_quantity': 120
        },
        {
            'name': 'Americano',
            'sale_price': 28.00,
            'cost_price': 9.00,
            'description': 'Sulandırılmış espresso',
            'category': 'Sıcak İçecekler',
            'stock_quantity': 100
        },
        {
            'name': 'Mocha',
            'sale_price': 38.00,
            'cost_price': 14.00,
            'description': 'Çikolatalı kahve',
            'category': 'Sıcak İçecekler',
            'stock_quantity': 75
        },
        {
            'name': 'Ice Latte',
            'sale_price': 38.00,
            'cost_price': 13.00,
            'description': 'Buzlu latte',
            'category': 'Soğuk İçecekler',
            'stock_quantity': 85
        },
        {
            'name': 'Cold Brew',
            'sale_price': 40.00,
            'cost_price': 15.00,
            'description': 'Soğuk demleme kahve',
            'category': 'Soğuk İçecekler',
            'stock_quantity': 60
        },
        {
            'name': 'Filtre Çay',
            'sale_price': 15.00,
            'cost_price': 4.00,
            'description': 'Özel çay karışımı',
            'category': 'Sıcak İçecekler',
            'stock_quantity': 150
        },
        {
            'name': 'Limonata',
            'sale_price': 25.00,
            'cost_price': 8.00,
            'description': 'Taze sıkılmış limonata',
            'category': 'Soğuk İçecekler',
            'stock_quantity': 70
        },
        {
            'name': 'Croissant',
            'sale_price': 20.00,
            'cost_price': 7.00,
            'description': 'Tereyağlı kruvasan',
            'category': 'Atıştırmalık',
            'stock_quantity': 40
        },
        {
            'name': 'Cheesecake',
            'sale_price': 45.00,
            'cost_price': 18.00,
            'description': 'Ev yapımı cheesecake',
            'category': 'Tatlı',
            'stock_quantity': 30
        },
        {
            'name': 'Brownie',
            'sale_price': 35.00,
            'cost_price': 12.00,
            'description': 'Çikolatalı brownie',
            'category': 'Tatlı',
            'stock_quantity': 35
        },
        {
            'name': 'Su',
            'sale_price': 5.00,
            'cost_price': 1.50,
            'description': 'Şişe su 500ml',
            'category': 'Soğuk İçecekler',
            'stock_quantity': 200
        }
    ]
    
    product_ids = []
    for product in products:
        product_id = db.add_product(**product)
        product_ids.append(product_id)
        print(f"  ✓ {product['name']} eklendi (ID: {product_id})")
    
    # Örnek adisyonlar oluştur
    print("\n📋 Örnek adisyonlar oluşturuluyor...")
    
    # Adisyon 1 - Açık
    bill1_id = db.create_bill("Ahmet Yılmaz", "Masa 1", "Pencere kenarı")
    db.add_bill_item(bill1_id, product_ids[0], 2)  # 2x Türk Kahvesi
    db.add_bill_item(bill1_id, product_ids[11], 1)  # 1x Croissant
    print(f"  ✓ Ahmet Yılmaz için adisyon oluşturuldu (ID: {bill1_id}) - Açık")
    
    # Adisyon 2 - Kısmi ödeme
    bill2_id = db.create_bill("Ayşe Demir", "Masa 3")
    db.add_bill_item(bill2_id, product_ids[2], 1)  # 1x Cappuccino
    db.add_bill_item(bill2_id, product_ids[3], 1)  # 1x Latte
    db.add_bill_item(bill2_id, product_ids[13], 2)  # 2x Brownie
    db.add_payment(bill2_id, 50.00, 'cash', 'İlk ödeme')
    print(f"  ✓ Ayşe Demir için adisyon oluşturuldu (ID: {bill2_id}) - Kısmi Ödeme")
    
    # Adisyon 3 - Ödendi
    bill3_id = db.create_bill("Mehmet Kaya", "Masa 5")
    db.add_bill_item(bill3_id, product_ids[1], 2)  # 2x Filtre Kahve
    db.add_bill_item(bill3_id, product_ids[12], 1)  # 1x Cheesecake
    db.add_payment(bill3_id, 105.00, 'card', 'Kredi kartı ile ödendi')
    print(f"  ✓ Mehmet Kaya için adisyon oluşturuldu (ID: {bill3_id}) - Ödendi")
    
    # Adisyon 4 - Açık
    bill4_id = db.create_bill("Zeynep Arslan", "Masa 2")
    db.add_bill_item(bill4_id, product_ids[7], 1)  # 1x Ice Latte
    db.add_bill_item(bill4_id, product_ids[10], 1)  # 1x Limonata
    print(f"  ✓ Zeynep Arslan için adisyon oluşturuldu (ID: {bill4_id}) - Açık")
    
    # Adisyon 5 - Ödendi
    bill5_id = db.create_bill("Can Öztürk", "Paket")
    db.add_bill_item(bill5_id, product_ids[4], 3)  # 3x Espresso
    db.add_bill_item(bill5_id, product_ids[14], 3)  # 3x Su
    db.add_payment(bill5_id, 75.00, 'cash', 'Nakit ödendi')
    print(f"  ✓ Can Öztürk için adisyon oluşturuldu (ID: {bill5_id}) - Ödendi")
    
    print("\n✅ Tüm örnek veriler başarıyla eklendi!")
    print("\n📊 Veritabanı İstatistikleri:")
    print(f"  • Toplam Ürün: {len(db.get_all_products())}")
    print(f"  • Toplam Adisyon: {len(db.get_all_bills())}")
    print(f"  • Açık Adisyon: {len(db.get_open_bills())}")
    
    # Bugünün raporunu göster
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    report = db.get_daily_report(today)
    
    print(f"\n📈 Günlük Rapor ({today}):")
    if report and 'sales' in report:
        sales = report['sales']
        print(f"  • Toplam Satış: ₺{sales.get('total_sales', 0):.2f}")
        print(f"  • Tahsilat: ₺{sales.get('total_paid', 0):.2f}")
    
    db.close()
    print("\n🎉 Test verisi hazırlama tamamlandı! Uygulamayı çalıştırabilirsiniz.")


def clear_database():
    """Veritabanını temizle"""
    import os
    db_path = "database/adisyon.db"
    
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✅ Veritabanı temizlendi: {db_path}")
    else:
        print("⚠️  Veritabanı dosyası bulunamadı.")


if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("AdisyonApp - Test Veri Yönetimi")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        print("\n⚠️  Veritabanı temizleniyor...")
        clear_database()
        print("\n✅ Veritabanı temizlendi. Yeni veri eklemek için tekrar çalıştırın.")
    else:
        print("\nℹ️  Örnek veriler ekleniyor...")
        print("   (Veritabanını temizlemek için: python test_data.py clear)\n")
        add_sample_data()
