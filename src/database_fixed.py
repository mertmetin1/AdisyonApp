"""
Veritabanı yönetimi modülü
SQLite ile ürünler, adisyonlar ve ödemeler yönetimi
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class Database:
    """Veritabanı işlemlerini yöneten sınıf"""
    
    def __init__(self, db_path: str = "database/adisyon.db"):
        """
        Veritabanı bağlantısını başlat
        
        Args:
            db_path: Veritabanı dosya yolu
        """
        # Veritabanı dizinini oluştur
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
        self.db_path = db_path
        self.create_tables()
    
    def connect(self):
        """Veritabanına yeni bağlantı aç ve döndür"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def create_tables(self):
        """Veritabanı tablolarını oluştur"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Ürünler tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                cost_price REAL NOT NULL DEFAULT 0,
                sale_price REAL NOT NULL,
                profit_margin REAL,
                image_path TEXT,
                category TEXT,
                stock_quantity INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Adisyonlar tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                table_number TEXT,
                total_amount REAL NOT NULL DEFAULT 0,
                paid_amount REAL NOT NULL DEFAULT 0,
                remaining_amount REAL NOT NULL DEFAULT 0,
                status TEXT DEFAULT 'open',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                closed_at TIMESTAMP
            )
        """)
        
        # Adisyon kalemleri tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bill_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 1,
                unit_price REAL NOT NULL,
                total_price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (bill_id) REFERENCES bills (id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        """)
        
        # Ödemeler tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                payment_method TEXT DEFAULT 'cash',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (bill_id) REFERENCES bills (id) ON DELETE CASCADE
            )
        """)
        
        conn.commit()
    
    conn.close()
    
    # ==================== ÜRÜN İŞLEMLERİ ====================
    
    def add_product(self, name: str, sale_price: float, cost_price: float = 0,
                   description: str = "", image_path: str = "", category: str = "",
                   stock_quantity: int = 0) -> int:
        """
        Yeni ürün ekle
        
        Args:
            name: Ürün adı
            sale_price: Satış fiyatı
            cost_price: Maliyet fiyatı
            description: Açıklama
            image_path: Resim yolu
            category: Kategori
            stock_quantity: Stok miktarı
            
        Returns:
            Eklenen ürünün ID'si
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        profit_margin = ((sale_price - cost_price) / sale_price * 100) if sale_price > 0 else 0
        
        cursor.execute("""
            INSERT INTO products (name, sale_price, cost_price, description, 
                                image_path, category, stock_quantity, profit_margin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, sale_price, cost_price, description, image_path, 
              category, stock_quantity, profit_margin))
        
        conn.commit()
        conn.close()
        product_id = cursor.lastrowid
        conn.close()
        return product_id
    
    def update_product(self, product_id: int, **kwargs) -> bool:
        """
        Ürün bilgilerini güncelle
        
        Args:
            product_id: Ürün ID
            **kwargs: Güncellenecek alanlar
            
        Returns:
            Başarılı ise True
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        # Kar marjını yeniden hesapla
        if 'sale_price' in kwargs or 'cost_price' in kwargs:
            cursor.execute("SELECT sale_price, cost_price FROM products WHERE id = ?", 
                         (product_id,))
            row = cursor.fetchone()
            if row:
                sale_price = kwargs.get('sale_price', row['sale_price'])
                cost_price = kwargs.get('cost_price', row['cost_price'])
                kwargs['profit_margin'] = ((sale_price - cost_price) / sale_price * 100) if sale_price > 0 else 0
        
        kwargs['updated_at'] = datetime.now()
        
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values()) + [product_id]
        
        cursor.execute(f"""
            UPDATE products 
            SET {set_clause}
            WHERE id = ?
        """, values)
        
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    def delete_product(self, product_id: int) -> bool:
        """
        Ürünü sil (soft delete)
        
        Args:
            product_id: Ürün ID
            
        Returns:
            Başarılı ise True
        """
        return self.update_product(product_id, is_active=0)
    
    def get_product(self, product_id: int) -> Optional[Dict]:
        """
        Tek bir ürün getir
        
        Args:
            product_id: Ürün ID
            
        Returns:
            Ürün bilgileri veya None
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()

        conn.close()
        
        return dict(row) if row else None
    
    def get_all_products(self, active_only: bool = True) -> List[Dict]:
        """
        Tüm ürünleri getir
        
        Args:
            active_only: Sadece aktif ürünleri getir
            
        Returns:
            Ürün listesi
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        query = "SELECT * FROM products"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY name"
        
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]
    
    def search_products(self, search_term: str) -> List[Dict]:
        """
        Ürün ara
        
        Args:
            search_term: Arama terimi
            
        Returns:
            Bulunan ürünler
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM products 
            WHERE is_active = 1 
            AND (name LIKE ? OR description LIKE ? OR category LIKE ?)
            ORDER BY name
        """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        
        return [dict(row) for row in cursor.fetchall()]
    
    # ==================== ADİSYON İŞLEMLERİ ====================
    
    def create_bill(self, customer_name: str, table_number: str = "", 
                   notes: str = "") -> int:
        """
        Yeni adisyon oluştur
        
        Args:
            customer_name: Müşteri adı
            table_number: Masa numarası
            notes: Notlar
            
        Returns:
            Oluşturulan adisyon ID'si
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO bills (customer_name, table_number, notes, status)
            VALUES (?, ?, ?, 'open')
        """, (customer_name, table_number, notes))
        
        conn.commit()
        conn.close()
        return cursor.lastrowid
    
    def add_bill_item(self, bill_id: int, product_id: int, quantity: int = 1) -> bool:
        """
        Adisyona ürün ekle
        
        Args:
            bill_id: Adisyon ID
            product_id: Ürün ID
            quantity: Miktar
            
        Returns:
            Başarılı ise True
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        # Ürün bilgilerini al
        product = self.get_product(product_id)
        if not product:
            return False
        
        unit_price = product['sale_price']
        total_price = unit_price * quantity
        
        # Ürünü adisyona ekle
        cursor.execute("""
            INSERT INTO bill_items (bill_id, product_id, product_name, quantity, 
                                   unit_price, total_price)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (bill_id, product_id, product['name'], quantity, unit_price, total_price))
        
        # Adisyon toplamını güncelle
        self._update_bill_total(bill_id)
        
        conn.commit()
        conn.close()
        return True
    
    def remove_bill_item(self, item_id: int) -> bool:
        """
        Adisyondan ürün çıkar
        
        Args:
            item_id: Kalem ID
            
        Returns:
            Başarılı ise True
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        # Bill ID'yi al
        cursor.execute("SELECT bill_id FROM bill_items WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        if not row:
            return False
        
        bill_id = row['bill_id']
        
        # Kalemi sil
        cursor.execute("DELETE FROM bill_items WHERE id = ?", (item_id,))
        
        # Adisyon toplamını güncelle
        self._update_bill_total(bill_id)
        
        conn.commit()
        conn.close()
        return True
    
    def update_bill_item_quantity(self, item_id: int, quantity: int) -> bool:
        """
        Adisyon kalemi miktarını güncelle
        
        Args:
            item_id: Kalem ID
            quantity: Yeni miktar
            
        Returns:
            Başarılı ise True
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT bill_id, unit_price FROM bill_items WHERE id = ?
        """, (item_id,))
        row = cursor.fetchone()
        
        if not row:
            return False
        
        bill_id = row['bill_id']
        unit_price = row['unit_price']
        total_price = unit_price * quantity
        
        cursor.execute("""
            UPDATE bill_items 
            SET quantity = ?, total_price = ?
            WHERE id = ?
        """, (quantity, total_price, item_id))
        
        # Adisyon toplamını güncelle
        self._update_bill_total(bill_id)
        
        conn.commit()
        conn.close()
        return True
    
    def _update_bill_total(self, bill_id: int):
        """Adisyon toplamını güncelle (internal)"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Toplam tutarı hesapla
        cursor.execute("""
            SELECT COALESCE(SUM(total_price), 0) as total 
            FROM bill_items 
            WHERE bill_id = ?
        """, (bill_id,))
        
        total = cursor.fetchone()['total']
        
        # Ödenen tutarı al
        cursor.execute("""
            SELECT paid_amount FROM bills WHERE id = ?
        """, (bill_id,))
        
        paid = cursor.fetchone()['paid_amount']
        remaining = total - paid
        
        # Adisyonu güncelle
        cursor.execute("""
            UPDATE bills 
            SET total_amount = ?, 
                remaining_amount = ?,
                updated_at = ?
            WHERE id = ?
        """, (total, remaining, datetime.now(), bill_id))
        
        conn.commit()
    
    conn.close()
    
    def get_bill(self, bill_id: int) -> Optional[Dict]:
        """
        Adisyon bilgilerini getir
        
        Args:
            bill_id: Adisyon ID
            
        Returns:
            Adisyon bilgileri
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM bills WHERE id = ?", (bill_id,))
        row = cursor.fetchone()
        
        if not row:
            return None
        
        bill = dict(row)
        
        # Adisyon kalemlerini getir
        cursor.execute("""
            SELECT * FROM bill_items WHERE bill_id = ? ORDER BY created_at
        """, (bill_id,))
        
        bill['items'] = [dict(item) for item in cursor.fetchall()]

        
        conn.close()
        
        return bill
    
    def get_all_bills(self, status: Optional[str] = None) -> List[Dict]:
        """
        Tüm adisyonları getir
        
        Args:
            status: Durum filtresi ('open', 'paid', 'partial')
            
        Returns:
            Adisyon listesi
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        query = "SELECT * FROM bills"
        params = []
        
        if status:
            query += " WHERE status = ?"
            params.append(status)
        
        query += " ORDER BY created_at DESC"
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_open_bills(self) -> List[Dict]:
        """Açık adisyonları getir"""
        return self.get_all_bills(status='open')
    
    # ==================== ÖDEME İŞLEMLERİ ====================
    
    def add_payment(self, bill_id: int, amount: float, 
                   payment_method: str = 'cash', notes: str = "") -> bool:
        """
        Ödeme ekle
        
        Args:
            bill_id: Adisyon ID
            amount: Ödeme tutarı
            payment_method: Ödeme yöntemi (cash, card, transfer)
            notes: Notlar
            
        Returns:
            Başarılı ise True
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        # Ödemeyi ekle
        cursor.execute("""
            INSERT INTO payments (bill_id, amount, payment_method, notes)
            VALUES (?, ?, ?, ?)
        """, (bill_id, amount, payment_method, notes))
        
        # Adisyon ödeme durumunu güncelle
        cursor.execute("""
            SELECT total_amount, paid_amount FROM bills WHERE id = ?
        """, (bill_id,))
        
        row = cursor.fetchone()
        if not row:
            return False
        
        total_amount = row['total_amount']
        paid_amount = row['paid_amount'] + amount
        remaining_amount = total_amount - paid_amount
        
        # Durumu belirle
        if remaining_amount <= 0:
            status = 'paid'
            closed_at = datetime.now()
        elif paid_amount > 0:
            status = 'partial'
            closed_at = None
        else:
            status = 'open'
            closed_at = None
        
        # Adisyonu güncelle
        cursor.execute("""
            UPDATE bills 
            SET paid_amount = ?, 
                remaining_amount = ?,
                status = ?,
                closed_at = ?,
                updated_at = ?
            WHERE id = ?
        """, (paid_amount, remaining_amount, status, closed_at, datetime.now(), bill_id))
        
        conn.commit()
        conn.close()
        return True
    
    def get_bill_payments(self, bill_id: int) -> List[Dict]:
        """
        Adisyon ödemelerini getir
        
        Args:
            bill_id: Adisyon ID
            
        Returns:
            Ödeme listesi
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM payments 
            WHERE bill_id = ? 
            ORDER BY created_at DESC
        """, (bill_id,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    # ==================== RAPORLAMA ====================
    
    def get_daily_report(self, date: str = None) -> Dict:
        """
        Günlük rapor
        
        Args:
            date: Tarih (YYYY-MM-DD formatında, None ise bugün)
            
        Returns:
            Rapor verileri
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        conn = self.connect()
        cursor = conn.cursor()
        
        # Toplam satış
        cursor.execute("""
            SELECT 
                COUNT(*) as total_bills,
                COALESCE(SUM(total_amount), 0) as total_sales,
                COALESCE(SUM(paid_amount), 0) as total_paid
            FROM bills
            WHERE DATE(created_at) = ?
        """, (date,))
        
        sales_data = dict(cursor.fetchone())
        
        # Ödeme yöntemleri
        cursor.execute("""
            SELECT 
                payment_method,
                COUNT(*) as count,
                SUM(amount) as total
            FROM payments
            WHERE DATE(created_at) = ?
            GROUP BY payment_method
        """, (date,))
        
        payment_methods = [dict(row) for row in cursor.fetchall()]
        
        # En çok satan ürünler
        cursor.execute("""
            SELECT 
                bi.product_name,
                SUM(bi.quantity) as total_quantity,
                SUM(bi.total_price) as total_revenue
            FROM bill_items bi
            JOIN bills b ON bi.bill_id = b.id
            WHERE DATE(b.created_at) = ?
            GROUP BY bi.product_name
            ORDER BY total_quantity DESC
            LIMIT 10
        """, (date,))
        
        top_products = [dict(row) for row in cursor.fetchall()]

        
        conn.close()
        
        return {
            'date': date,
            'sales': sales_data,
            'payment_methods': payment_methods,
            'top_products': top_products
        }
    
    def get_monthly_report(self, year: int, month: int) -> Dict:
        """
        Aylık rapor
        
        Args:
            year: Yıl
            month: Ay
            
        Returns:
            Rapor verileri
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        # Toplam satış
        cursor.execute("""
            SELECT 
                COUNT(*) as total_bills,
                COALESCE(SUM(total_amount), 0) as total_sales,
                COALESCE(SUM(paid_amount), 0) as total_paid
            FROM bills
            WHERE strftime('%Y', created_at) = ? 
            AND strftime('%m', created_at) = ?
        """, (str(year), f"{month:02d}"))
        
        sales_data = dict(cursor.fetchone())
        
        # Günlük dağılım
        cursor.execute("""
            SELECT 
                DATE(created_at) as date,
                COUNT(*) as bills_count,
                SUM(total_amount) as daily_sales
            FROM bills
            WHERE strftime('%Y', created_at) = ? 
            AND strftime('%m', created_at) = ?
            GROUP BY DATE(created_at)
            ORDER BY date
        """, (str(year), f"{month:02d}"))
        
        daily_breakdown = [dict(row) for row in cursor.fetchall()]

        
        conn.close()
        
        return {
            'year': year,
            'month': month,
            'sales': sales_data,
            'daily_breakdown': daily_breakdown
        }
    
    def get_profit_loss_report(self, start_date: str, end_date: str) -> Dict:
        """
        Kar/zarar raporu
        
        Args:
            start_date: Başlangıç tarihi (YYYY-MM-DD)
            end_date: Bitiş tarihi (YYYY-MM-DD)
            
        Returns:
            Kar/zarar verileri
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                bi.product_name,
                p.cost_price,
                bi.unit_price as sale_price,
                SUM(bi.quantity) as total_quantity,
                SUM(bi.total_price) as total_revenue,
                SUM(bi.quantity * p.cost_price) as total_cost,
                SUM(bi.total_price - (bi.quantity * p.cost_price)) as total_profit
            FROM bill_items bi
            JOIN bills b ON bi.bill_id = b.id
            JOIN products p ON bi.product_id = p.id
            WHERE DATE(b.created_at) BETWEEN ? AND ?
            GROUP BY bi.product_name, p.cost_price, bi.unit_price
            ORDER BY total_profit DESC
        """, (start_date, end_date))
        
        products = [dict(row) for row in cursor.fetchall()]
        
        # Toplamları hesapla
        total_revenue = sum(p['total_revenue'] for p in products)
        total_cost = sum(p['total_cost'] for p in products)
        total_profit = total_revenue - total_cost
        profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        return {
            'start_date': start_date,
            'end_date': end_date,
            'total_revenue': total_revenue,
            'total_cost': total_cost,
            'total_profit': total_profit,
            'profit_margin': profit_margin,
            'products': products
        }
