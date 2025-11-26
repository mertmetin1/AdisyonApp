"""
Ana uygulama dosyası
AdisyonApp - Kivy/KivyMD tabanlı adisyon yönetim sistemi
"""

import os
import sys
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.toolbar import MDTopAppBar

# Veritabanı modülünü import et
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from database import Database

# Ekranları import et
from screens.home_screen import HomeScreen
from screens.products_screen import ProductsScreen
from screens.bills_screen import BillsScreen
from screens.payments_screen import PaymentsScreen
from screens.reports_screen import ReportsScreen

# Pencere boyutunu ayarla (masaüstü için)
Window.size = (400, 700)


# KV dosyası (Material Design arayüz)
KV = """
#:import get_color_from_hex kivy.utils.get_color_from_hex

<ContentNavigationDrawer>:
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"

    MDTopAppBar:
        title: "AdisyonApp"
        elevation: 4
        md_bg_color: app.theme_cls.primary_color
        left_action_items: [["close", lambda x: nav_drawer.set_state("close")]]

    ScrollView:
        MDList:
            OneLineAvatarIconListItem:
                text: "Ana Sayfa"
                on_release: app.change_screen("home")
                IconLeftWidget:
                    icon: "home"

            OneLineAvatarIconListItem:
                text: "Ürünler"
                on_release: app.change_screen("products")
                IconLeftWidget:
                    icon: "food"

            OneLineAvatarIconListItem:
                text: "Adisyonlar"
                on_release: app.change_screen("bills")
                IconLeftWidget:
                    icon: "receipt"

            OneLineAvatarIconListItem:
                text: "Ödemeler"
                on_release: app.change_screen("payments")
                IconLeftWidget:
                    icon: "cash-multiple"

            OneLineAvatarIconListItem:
                text: "Raporlar"
                on_release: app.change_screen("reports")
                IconLeftWidget:
                    icon: "chart-bar"

MDScreen:
    MDNavigationLayout:
        ScreenManager:
            id: screen_manager

            HomeScreen:
                name: "home"

            ProductsScreen:
                name: "products"

            BillsScreen:
                name: "bills"

            PaymentsScreen:
                name: "payments"

            ReportsScreen:
                name: "reports"

        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)

            ContentNavigationDrawer:
                id: content_drawer
"""


class ContentNavigationDrawer(MDScreen):
    """Navigasyon drawer içeriği"""
    pass


class AdisyonApp(MDApp):
    """Ana uygulama sınıfı"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = None
    
    def build(self):
        """Uygulamayı oluştur"""
        # Temayı ayarla
        self.theme_cls.primary_palette = "Brown"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = "Light"
        
        # Veritabanını başlat
        self.db = Database()
        
        # KV dosyasını yükle
        return Builder.load_string(KV)
    
    def on_start(self):
        """Uygulama başladığında"""
        pass
    
    def change_screen(self, screen_name):
        """Ekranı değiştir ve drawer'ı kapat"""
        try:
            self.root.ids.screen_manager.current = screen_name
            self.root.ids.nav_drawer.set_state("close")
        except Exception as e:
            print(f"Error changing screen: {e}")
    
    def on_stop(self):
        """Uygulama kapandığında"""
        # Database artık her seferinde bağlantı açıp kapatıyor
        pass


if __name__ == "__main__":
    AdisyonApp().run()
