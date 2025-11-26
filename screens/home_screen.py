"""
Ana sayfa ekranı
"""

from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from datetime import datetime

KV = """
<HomeScreen>:
    name: "home"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "AdisyonApp - Ana Sayfa"
            elevation: 4
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: "16dp"
                spacing: "16dp"
                adaptive_height: True

                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    size_hint_y: None
                    height: "120dp"
                    elevation: 3
                    md_bg_color: app.theme_cls.primary_color

                    MDLabel:
                        text: "Hoş Geldiniz!"
                        font_style: "H5"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        halign: "center"

                    MDLabel:
                        id: date_label
                        text: ""
                        font_style: "Body1"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 0.8
                        halign: "center"

                MDLabel:
                    text: "Hızlı Erişim"
                    font_style: "H6"
                    size_hint_y: None
                    height: "48dp"
                    padding: "8dp", "8dp"

                MDGridLayout:
                    cols: 2
                    spacing: "16dp"
                    size_hint_y: None
                    height: "300dp"

                    MDCard:
                        orientation: "vertical"
                        padding: "16dp"
                        elevation: 2

                        MDIconButton:
                            icon: "receipt-text"
                            pos_hint: {"center_x": 0.5}
                            user_font_size: "64sp"
                            on_release: app.change_screen("bills")

                        MDLabel:
                            text: "Yeni Adisyon"
                            halign: "center"
                            font_style: "Button"

                    MDCard:
                        orientation: "vertical"
                        padding: "16dp"
                        elevation: 2

                        MDIconButton:
                            icon: "food"
                            pos_hint: {"center_x": 0.5}
                            user_font_size: "64sp"
                            on_release: app.change_screen("products")

                        MDLabel:
                            text: "Ürünler"
                            halign: "center"
                            font_style: "Button"

                    MDCard:
                        orientation: "vertical"
                        padding: "16dp"
                        elevation: 2

                        MDIconButton:
                            icon: "cash-multiple"
                            pos_hint: {"center_x": 0.5}
                            user_font_size: "64sp"
                            on_release: app.change_screen("payments")

                        MDLabel:
                            text: "Ödemeler"
                            halign: "center"
                            font_style: "Button"

                    MDCard:
                        orientation: "vertical"
                        padding: "16dp"
                        elevation: 2

                        MDIconButton:
                            icon: "chart-bar"
                            pos_hint: {"center_x": 0.5}
                            user_font_size: "64sp"
                            on_release: app.change_screen("reports")

                        MDLabel:
                            text: "Raporlar"
                            halign: "center"
                            font_style: "Button"

                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    size_hint_y: None
                    height: "150dp"
                    elevation: 3

                    MDLabel:
                        text: "Bugünün Özeti"
                        font_style: "H6"
                        size_hint_y: None
                        height: "36dp"

                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: "8dp"

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                id: today_bills_label
                                text: "0"
                                font_style: "H4"
                                halign: "center"

                            MDLabel:
                                text: "Adisyon"
                                font_style: "Caption"
                                halign: "center"

                        MDSeparator:
                            orientation: "vertical"

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                id: today_sales_label
                                text: "₺0"
                                font_style: "H4"
                                halign: "center"

                            MDLabel:
                                text: "Satış"
                                font_style: "Caption"
                                halign: "center"

                        MDSeparator:
                            orientation: "vertical"

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                id: today_paid_label
                                text: "₺0"
                                font_style: "H4"
                                halign: "center"

                            MDLabel:
                                text: "Tahsilat"
                                font_style: "Caption"
                                halign: "center"
"""


class HomeScreen(MDScreen):
    """Ana sayfa ekranı"""
    
    def on_enter(self):
        """Ekran görüntülendiğinde"""
        # Tarihi güncelle
        today = datetime.now()
        try:
            self.ids.date_label.text = today.strftime("%d %B %Y, %A")
        except:
            pass  # ID henüz hazır değilse atla
        
        # Bugünün istatistiklerini yükle
        self.load_today_stats()
    
    def load_today_stats(self):
        """Bugünün istatistiklerini yükle"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        today = datetime.now().strftime("%Y-%m-%d")
        report = app.db.get_daily_report(today)
        
        if report and 'sales' in report:
            sales = report['sales']
            try:
                self.ids.today_bills_label.text = str(sales.get('total_bills', 0))
                self.ids.today_sales_label.text = f"₺{sales.get('total_sales', 0):.2f}"
                self.ids.today_paid_label.text = f"₺{sales.get('total_paid', 0):.2f}"
            except:
                pass  # ID'ler henüz hazır değilse atla


Builder.load_string(KV)
