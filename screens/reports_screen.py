"""
Raporlama ve istatistik ekranı
"""

from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from datetime import datetime, timedelta

KV = """
<ReportsScreen>:
    name: "reports"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Raporlar"
            elevation: 4
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: "16dp"
                spacing: "16dp"
                adaptive_height: True

                MDLabel:
                    text: "Satış Raporları"
                    font_style: "H6"
                    size_hint_y: None
                    height: "48dp"

                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    size_hint_y: None
                    height: "180dp"
                    elevation: 3

                    MDLabel:
                        text: "Bugün"
                        font_style: "Subtitle1"
                        size_hint_y: None
                        height: "36dp"

                    MDGridLayout:
                        cols: 3
                        spacing: "8dp"

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                id: today_bills
                                text: "0"
                                font_style: "H4"
                                halign: "center"

                            MDLabel:
                                text: "Adisyon"
                                font_style: "Caption"
                                halign: "center"

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                id: today_sales
                                text: "₺0"
                                font_style: "H4"
                                halign: "center"

                            MDLabel:
                                text: "Satış"
                                font_style: "Caption"
                                halign: "center"

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                id: today_paid
                                text: "₺0"
                                font_style: "H4"
                                halign: "center"

                            MDLabel:
                                text: "Tahsilat"
                                font_style: "Caption"
                                halign: "center"

                    MDRaisedButton:
                        text: "Detaylı Rapor"
                        pos_hint: {"center_x": 0.5}
                        on_release: root.show_daily_report()

                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    size_hint_y: None
                    height: "180dp"
                    elevation: 3

                    MDLabel:
                        text: "Bu Ay"
                        font_style: "Subtitle1"
                        size_hint_y: None
                        height: "36dp"

                    MDGridLayout:
                        cols: 3
                        spacing: "8dp"

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                id: month_bills
                                text: "0"
                                font_style: "H4"
                                halign: "center"

                            MDLabel:
                                text: "Adisyon"
                                font_style: "Caption"
                                halign: "center"

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                id: month_sales
                                text: "₺0"
                                font_style: "H4"
                                halign: "center"

                            MDLabel:
                                text: "Satış"
                                font_style: "Caption"
                                halign: "center"

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                id: month_paid
                                text: "₺0"
                                font_style: "H4"
                                halign: "center"

                            MDLabel:
                                text: "Tahsilat"
                                font_style: "Caption"
                                halign: "center"

                    MDRaisedButton:
                        text: "Aylık Rapor"
                        pos_hint: {"center_x": 0.5}
                        on_release: root.show_monthly_report()

                MDLabel:
                    text: "Kar/Zarar Analizi"
                    font_style: "H6"
                    size_hint_y: None
                    height: "48dp"

                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    size_hint_y: None
                    height: "200dp"
                    elevation: 3

                    MDLabel:
                        text: "Son 7 Gün"
                        font_style: "Subtitle1"
                        size_hint_y: None
                        height: "36dp"

                    MDGridLayout:
                        cols: 2
                        spacing: "8dp"

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                id: week_revenue
                                text: "₺0"
                                font_style: "H5"
                                halign: "center"

                            MDLabel:
                                text: "Gelir"
                                font_style: "Caption"
                                halign: "center"

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                id: week_cost
                                text: "₺0"
                                font_style: "H5"
                                halign: "center"

                            MDLabel:
                                text: "Maliyet"
                                font_style: "Caption"
                                halign: "center"

                    MDSeparator:

                    MDBoxLayout:
                        orientation: "horizontal"
                        size_hint_y: None
                        height: "48dp"
                        padding: "8dp", "8dp"

                        MDLabel:
                            text: "Net Kar:"
                            font_style: "Subtitle1"

                        MDLabel:
                            id: week_profit
                            text: "₺0"
                            font_style: "H6"
                            halign: "right"

                    MDRaisedButton:
                        text: "Detaylı Kar/Zarar"
                        pos_hint: {"center_x": 0.5}
                        on_release: root.show_profit_loss_report()

                MDLabel:
                    text: "En Çok Satan Ürünler"
                    font_style: "H6"
                    size_hint_y: None
                    height: "48dp"

                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    size_hint_y: None
                    height: "250dp"
                    elevation: 3

                    ScrollView:
                        MDList:
                            id: top_products_list
"""


class ReportsScreen(MDScreen):
    """Raporlama ekranı"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
    
    def on_enter(self):
        """Ekran görüntülendiğinde"""
        self.load_today_stats()
        self.load_month_stats()
        self.load_week_profit_loss()
        self.load_top_products()
    
    def load_today_stats(self):
        """Bugünün istatistiklerini yükle"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            report = app.db.get_daily_report(today)
            
            if report and 'sales' in report:
                sales = report['sales']
                self.ids.today_bills.text = str(sales.get('total_bills', 0))
                self.ids.today_sales.text = f"₺{sales.get('total_sales', 0):.2f}"
                self.ids.today_paid.text = f"₺{sales.get('total_paid', 0):.2f}"
        except Exception as e:
            print(f"Error loading today stats: {e}")
    
    def load_month_stats(self):
        """Bu ayın istatistiklerini yükle"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        try:
            now = datetime.now()
            report = app.db.get_monthly_report(now.year, now.month)
            
            if report and 'sales' in report:
                sales = report['sales']
                self.ids.month_bills.text = str(sales.get('total_bills', 0))
                self.ids.month_sales.text = f"₺{sales.get('total_sales', 0):.2f}"
                self.ids.month_paid.text = f"₺{sales.get('total_paid', 0):.2f}"
        except Exception as e:
            print(f"Error loading month stats: {e}")
    
    def load_week_profit_loss(self):
        """Son 7 günün kar/zarar analizini yükle"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            
            report = app.db.get_profit_loss_report(
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )
            
            if report:
                self.ids.week_revenue.text = f"₺{report['total_revenue']:.2f}"
                self.ids.week_cost.text = f"₺{report['total_cost']:.2f}"
                self.ids.week_profit.text = f"₺{report['total_profit']:.2f}"
        except Exception as e:
            print(f"Error loading week profit/loss: {e}")
    
    def load_top_products(self):
        """En çok satan ürünleri yükle"""
        from kivymd.app import MDApp
        from kivymd.uix.list import TwoLineListItem
        
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            report = app.db.get_daily_report(today)
            
            self.ids.top_products_list.clear_widgets()
            
            if report and 'top_products' in report:
                for i, product in enumerate(report['top_products'][:5], 1):
                    item = TwoLineListItem(
                        text=f"{i}. {product['product_name']}",
                        secondary_text=f"{product['total_quantity']} adet | ₺{product['total_revenue']:.2f}"
                    )
                    self.ids.top_products_list.add_widget(item)
        except Exception as e:
            print(f"Error loading top products: {e}")
    
    def show_daily_report(self):
        """Detaylı günlük rapor göster"""
        from kivymd.app import MDApp
        from kivymd.uix.label import MDLabel
        
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        today = datetime.now().strftime("%Y-%m-%d")
        report = app.db.get_daily_report(today)
        
        content = MDBoxLayout(
            orientation="vertical",
            spacing="8dp",
            padding="8dp",
            size_hint_y=None,
            height="400dp"
        )
        
        if report:
            sales = report.get('sales', {})
            
            report_text = f"""
[b]Tarih:[/b] {datetime.now().strftime("%d %B %Y")}

[b]SATIŞLAR[/b]
Toplam Adisyon: {sales.get('total_bills', 0)}
Toplam Satış: ₺{sales.get('total_sales', 0):.2f}
Tahsilat: ₺{sales.get('total_paid', 0):.2f}

[b]ÖDEME YÖNTEMLERİ[/b]
            """
            
            for pm in report.get('payment_methods', []):
                pm_text = {
                    'cash': 'Nakit',
                    'card': 'Kart',
                    'transfer': 'Havale'
                }.get(pm['payment_method'], 'Diğer')
                report_text += f"{pm_text}: ₺{pm['total']:.2f} ({pm['count']} işlem)\n"
            
            report_text += "\n[b]EN ÇOK SATANLAR[/b]\n"
            for i, product in enumerate(report.get('top_products', [])[:10], 1):
                report_text += f"{i}. {product['product_name']}: {product['total_quantity']} adet\n"
            
            content.add_widget(MDLabel(text=report_text.strip(), markup=True))
        
        from kivy.uix.scrollview import ScrollView
        scroll = ScrollView()
        scroll.add_widget(content)
        
        self.dialog = MDDialog(
            title="Günlük Rapor",
            type="custom",
            content_cls=scroll,
            size_hint=(0.9, 0.8),
            buttons=[
                MDRaisedButton(
                    text="KAPAT",
                    on_release=lambda x: self.dialog.dismiss()
                ),
            ],
        )
        self.dialog.open()
    
    def show_monthly_report(self):
        """Aylık rapor göster"""
        from kivymd.app import MDApp
        from kivymd.uix.label import MDLabel
        
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        now = datetime.now()
        report = app.db.get_monthly_report(now.year, now.month)
        
        content = MDBoxLayout(
            orientation="vertical",
            spacing="8dp",
            padding="8dp",
            size_hint_y=None,
            height="400dp"
        )
        
        if report:
            sales = report.get('sales', {})
            
            month_names = {
                1: 'Ocak', 2: 'Şubat', 3: 'Mart', 4: 'Nisan',
                5: 'Mayıs', 6: 'Haziran', 7: 'Temmuz', 8: 'Ağustos',
                9: 'Eylül', 10: 'Ekim', 11: 'Kasım', 12: 'Aralık'
            }
            
            report_text = f"""
[b]Dönem:[/b] {month_names[now.month]} {now.year}

[b]ÖZET[/b]
Toplam Adisyon: {sales.get('total_bills', 0)}
Toplam Satış: ₺{sales.get('total_sales', 0):.2f}
Tahsilat: ₺{sales.get('total_paid', 0):.2f}

[b]GÜNLÜK DAĞILIM[/b]
            """
            
            for day in report.get('daily_breakdown', []):
                date_obj = datetime.fromisoformat(day['date'])
                report_text += f"{date_obj.strftime('%d.%m')}: ₺{day['daily_sales']:.2f} ({day['bills_count']} adisyon)\n"
            
            content.add_widget(MDLabel(text=report_text.strip(), markup=True))
        
        from kivy.uix.scrollview import ScrollView
        scroll = ScrollView()
        scroll.add_widget(content)
        
        self.dialog = MDDialog(
            title="Aylık Rapor",
            type="custom",
            content_cls=scroll,
            size_hint=(0.9, 0.8),
            buttons=[
                MDRaisedButton(
                    text="KAPAT",
                    on_release=lambda x: self.dialog.dismiss()
                ),
            ],
        )
        self.dialog.open()
    
    def show_profit_loss_report(self):
        """Kar/zarar raporu göster"""
        from kivymd.app import MDApp
        from kivymd.uix.label import MDLabel
        
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        report = app.db.get_profit_loss_report(
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )
        
        content = MDBoxLayout(
            orientation="vertical",
            spacing="8dp",
            padding="8dp",
            size_hint_y=None,
            height="450dp"
        )
        
        if report:
            report_text = f"""
[b]Dönem:[/b] {start_date.strftime("%d.%m.%Y")} - {end_date.strftime("%d.%m.%Y")}

[b]ÖZET[/b]
Toplam Gelir: ₺{report['total_revenue']:.2f}
Toplam Maliyet: ₺{report['total_cost']:.2f}
Net Kar: ₺{report['total_profit']:.2f}
Kar Marjı: %{report['profit_margin']:.2f}

[b]ÜRÜN BAZINDA[/b]
            """
            
            for product in report.get('products', [])[:10]:
                report_text += f"""
{product['product_name']}
  Satış: {product['total_quantity']} adet | ₺{product['total_revenue']:.2f}
  Maliyet: ₺{product['total_cost']:.2f}
  Kar: ₺{product['total_profit']:.2f}
---
"""
            
            content.add_widget(MDLabel(text=report_text.strip(), markup=True))
        
        from kivy.uix.scrollview import ScrollView
        scroll = ScrollView()
        scroll.add_widget(content)
        
        self.dialog = MDDialog(
            title="Kar/Zarar Raporu",
            type="custom",
            content_cls=scroll,
            size_hint=(0.9, 0.8),
            buttons=[
                MDRaisedButton(
                    text="KAPAT",
                    on_release=lambda x: self.dialog.dismiss()
                ),
            ],
        )
        self.dialog.open()


Builder.load_string(KV)
