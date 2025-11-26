"""
Ödeme yönetimi ekranı
"""

from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget
from datetime import datetime

KV = """
<PaymentsScreen>:
    name: "payments"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Ödeme Geçmişi"
            elevation: 4
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]

        MDBoxLayout:
            orientation: "vertical"
            padding: "8dp"
            spacing: "8dp"

            MDCard:
                orientation: "vertical"
                padding: "16dp"
                size_hint_y: None
                height: "100dp"
                elevation: 3

                MDLabel:
                    text: "Bugün"
                    font_style: "H6"
                    size_hint_y: None
                    height: "36dp"

                MDBoxLayout:
                    orientation: "horizontal"
                    spacing: "8dp"

                    MDBoxLayout:
                        orientation: "vertical"

                        MDLabel:
                            id: today_payments_count
                            text: "0"
                            font_style: "H4"
                            halign: "center"

                        MDLabel:
                            text: "Ödeme"
                            font_style: "Caption"
                            halign: "center"

                    MDSeparator:
                        orientation: "vertical"

                    MDBoxLayout:
                        orientation: "vertical"

                        MDLabel:
                            id: today_payments_amount
                            text: "₺0"
                            font_style: "H4"
                            halign: "center"

                        MDLabel:
                            text: "Toplam"
                            font_style: "Caption"
                            halign: "center"

            ScrollView:
                MDList:
                    id: payments_list
"""


class PaymentsScreen(MDScreen):
    """Ödeme yönetimi ekranı"""
    
    def on_enter(self):
        """Ekran görüntülendiğinde"""
        self.load_payments()
        self.load_today_stats()
    
    def load_payments(self):
        """Ödemeleri yükle"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        try:
            # Tüm adisyonları al
            bills = app.db.get_all_bills()
            
            self.ids.payments_list.clear_widgets()
            
            # Her adisyon için ödemeleri göster
            for bill in bills:
                payments = app.db.get_bill_payments(bill['id'])
                
                for payment in payments:
                    payment_method_icons = {
                        'cash': 'cash',
                        'card': 'credit-card',
                        'transfer': 'bank-transfer'
                    }
                    
                    payment_method_texts = {
                        'cash': 'Nakit',
                        'card': 'Kart',
                        'transfer': 'Havale'
                    }
                    
                    # Tarih formatla
                    payment_date = datetime.fromisoformat(payment['created_at'])
                    date_str = payment_date.strftime("%d.%m.%Y %H:%M")
                    
                    item = TwoLineAvatarIconListItem(
                        text=f"{bill['customer_name']} - ₺{payment['amount']:.2f}",
                        secondary_text=f"{payment_method_texts.get(payment['payment_method'], 'Diğer')} | {date_str}"
                    )
                    
                    icon = payment_method_icons.get(payment['payment_method'], 'cash')
                    item.add_widget(IconLeftWidget(icon=icon))
                    
                    self.ids.payments_list.add_widget(item)
        except Exception as e:
            print(f"Error loading payments: {e}")
    
    def load_today_stats(self):
        """Bugünün istatistiklerini yükle"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Bugünün ödemelerini say
            conn = app.db.connect()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT COUNT(*) as count, COALESCE(SUM(amount), 0) as total
                FROM payments
                WHERE DATE(created_at) = ?
            """, (today,))
            
            result = cursor.fetchone()
            
            if result:
                self.ids.today_payments_count.text = str(result['count'])
                self.ids.today_payments_amount.text = f"₺{result['total']:.2f}"
            
            conn.close()
        except Exception as e:
            print(f"Error loading today stats: {e}")


Builder.load_string(KV)
