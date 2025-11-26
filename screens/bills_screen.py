"""
Adisyon yönetimi ekranı
"""

from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineAvatarIconListItem, ThreeLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp

KV = """
<BillsScreen>:
    name: "bills"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Adisyon Yönetimi"
            elevation: 4
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]
            right_action_items: [["plus", lambda x: root.show_new_bill_dialog()]]

        MDBoxLayout:
            orientation: "vertical"
            padding: "8dp"
            spacing: "8dp"

            MDBoxLayout:
                size_hint_y: None
                height: "48dp"
                spacing: "8dp"

                MDRaisedButton:
                    id: btn_open
                    text: "Açık Adisyonlar"
                    on_release: root.show_open_bills()
                    md_bg_color: app.theme_cls.primary_color

                MDRaisedButton:
                    id: btn_all
                    text: "Tüm Adisyonlar"
                    on_release: root.show_all_bills()

            ScrollView:
                id: scroll_view

                MDList:
                    id: bills_list
"""


class BillsScreen(MDScreen):
    """Adisyon yönetimi ekranı"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.current_bill_id = None
        self.product_menu = None
        self.current_view = "open"
    
    def on_enter(self):
        """Ekran görüntülendiğinde"""
        self.load_open_bills()
    
    def show_open_bills(self):
        """Açık adisyonlar görünümüne geç"""
        self.current_view = "open"
        try:
            from kivymd.app import MDApp
            app = MDApp.get_running_app()
            self.ids.btn_open.md_bg_color = app.theme_cls.primary_color
            self.ids.btn_all.md_bg_color = app.theme_cls.disabled_hint_text_color
        except:
            pass
        self.load_open_bills()
    
    def show_all_bills(self):
        """Tüm adisyonlar görünümüne geç"""
        self.current_view = "all"
        try:
            from kivymd.app import MDApp
            app = MDApp.get_running_app()
            self.ids.btn_all.md_bg_color = app.theme_cls.primary_color
            self.ids.btn_open.md_bg_color = app.theme_cls.disabled_hint_text_color
        except:
            pass
        self.load_all_bills()
    
    def load_open_bills(self):
        """Açık adisyonları yükle"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        try:
            bills = app.db.get_open_bills()
            
            self.ids.bills_list.clear_widgets()
            
            for bill in bills:
                status_icon = "clock-outline" if bill['status'] == 'open' else "clock-check-outline"
                status_text = "Açık" if bill['status'] == 'open' else "Kısmi Ödeme"
                
                item = ThreeLineAvatarIconListItem(
                    text=bill['customer_name'],
                    secondary_text=f"Toplam: ₺{bill['total_amount']:.2f} | Ödenen: ₺{bill['paid_amount']:.2f}",
                    tertiary_text=f"Kalan: ₺{bill['remaining_amount']:.2f} | {status_text}",
                    on_release=lambda x, b=bill: self.show_bill_detail(b['id'])
                )
                
                item.add_widget(IconLeftWidget(icon=status_icon))
                
                # Ödeme butonu
                pay_icon = IconRightWidget(
                    icon="cash",
                    on_release=lambda x, b=bill: self.show_payment_dialog(b['id'])
                )
                item.add_widget(pay_icon)
                
                self.ids.bills_list.add_widget(item)
        except Exception as e:
            print(f"Error loading open bills: {e}")
            toast(f"Adisyonlar yüklenirken hata: {str(e)}")
    
    def load_all_bills(self):
        """Tüm adisyonları yükle"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        try:
            bills = app.db.get_all_bills()
            
            self.ids.bills_list.clear_widgets()
            
            for bill in bills:
                status_icons = {
                    'open': 'clock-outline',
                    'partial': 'clock-check-outline',
                    'paid': 'check-circle'
                }
                status_texts = {
                    'open': 'Açık',
                    'partial': 'Kısmi Ödeme',
                    'paid': 'Ödendi'
                }
                
                item = ThreeLineAvatarIconListItem(
                    text=bill['customer_name'],
                    secondary_text=f"Toplam: ₺{bill['total_amount']:.2f} | Ödenen: ₺{bill['paid_amount']:.2f}",
                    tertiary_text=f"Kalan: ₺{bill['remaining_amount']:.2f} | {status_texts.get(bill['status'], 'Bilinmiyor')}",
                    on_release=lambda x, b=bill: self.show_bill_detail(b['id'])
                )
                
                item.add_widget(IconLeftWidget(icon=status_icons.get(bill['status'], 'receipt')))
                
                self.ids.bills_list.add_widget(item)
        except Exception as e:
            print(f"Error loading all bills: {e}")
            toast(f"Adisyonlar yüklenirken hata: {str(e)}")
    
    def show_new_bill_dialog(self):
        """Yeni adisyon dialogunu göster"""
        content = MDBoxLayout(
            orientation="vertical",
            spacing="12dp",
            size_hint_y=None,
            height="150dp"
        )
        
        customer_field = MDTextField(hint_text="Müşteri Adı *", required=True)
        table_field = MDTextField(hint_text="Masa Numarası")
        notes_field = MDTextField(hint_text="Notlar", multiline=True)
        
        content.add_widget(customer_field)
        content.add_widget(table_field)
        content.add_widget(notes_field)
        
        self.dialog = MDDialog(
            title="Yeni Adisyon",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="İPTAL",
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="OLUŞTUR",
                    on_release=lambda x: self.create_bill(
                        customer_field.text,
                        table_field.text,
                        notes_field.text
                    )
                ),
            ],
        )
        self.dialog.open()
    
    def create_bill(self, customer_name, table_number, notes):
        """Yeni adisyon oluştur"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        if not customer_name:
            toast("Müşteri adı zorunludur!")
            return
        
        bill_id = app.db.create_bill(customer_name, table_number, notes)
        toast("Adisyon oluşturuldu!")
        
        self.dialog.dismiss()
        self.show_bill_detail(bill_id)
    
    def show_bill_detail(self, bill_id):
        """Adisyon detayını göster"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        self.current_bill_id = bill_id
        bill = app.db.get_bill(bill_id)
        
        if not bill:
            toast("Adisyon bulunamadı!")
            return
        
        content = MDBoxLayout(
            orientation="vertical",
            spacing="8dp",
            padding="8dp",
            size_hint_y=None,
            height="450dp"
        )
        
        # Başlık bilgileri
        from kivymd.uix.label import MDLabel
        header_text = f"""
[b]Müşteri:[/b] {bill['customer_name']}
[b]Masa:[/b] {bill.get('table_number', '-')}
[b]Durum:[/b] {self._get_status_text(bill['status'])}

[b]Toplam:[/b] ₺{bill['total_amount']:.2f}
[b]Ödenen:[/b] ₺{bill['paid_amount']:.2f}
[b]Kalan:[/b] ₺{bill['remaining_amount']:.2f}
        """
        content.add_widget(MDLabel(text=header_text.strip(), markup=True, size_hint_y=None, height="120dp"))
        
        # Ürün listesi
        from kivymd.uix.list import MDList
        from kivy.uix.scrollview import ScrollView
        
        items_list = MDList()
        
        for item in bill.get('items', []):
            list_item = TwoLineAvatarIconListItem(
                text=f"{item['product_name']} x{item['quantity']}",
                secondary_text=f"₺{item['unit_price']:.2f} | Toplam: ₺{item['total_price']:.2f}"
            )
            list_item.add_widget(IconLeftWidget(icon="food"))
            
            # Silme butonu (sadece açık adisyonlarda)
            if bill['status'] != 'paid':
                delete_icon = IconRightWidget(
                    icon="delete",
                    on_release=lambda x, i=item: self.remove_item_from_bill(i['id'])
                )
                list_item.add_widget(delete_icon)
            
            items_list.add_widget(list_item)
        
        scroll = ScrollView(size_hint_y=1)
        scroll.add_widget(items_list)
        content.add_widget(scroll)
        
        # Butonlar
        buttons = [
            MDFlatButton(
                text="KAPAT",
                on_release=lambda x: self.dialog.dismiss()
            )
        ]
        
        if bill['status'] != 'paid':
            buttons.insert(0, MDRaisedButton(
                text="ÜRÜN EKLE",
                on_release=lambda x: self.show_add_product_to_bill_menu()
            ))
            buttons.insert(1, MDRaisedButton(
                text="ÖDEME AL",
                on_release=lambda x: self.show_payment_dialog(bill_id)
            ))
        
        self.dialog = MDDialog(
            title="Adisyon Detayı",
            type="custom",
            content_cls=content,
            buttons=buttons,
        )
        self.dialog.open()
    
    def _get_status_text(self, status):
        """Durum metnini getir"""
        status_map = {
            'open': 'Açık',
            'partial': 'Kısmi Ödeme',
            'paid': 'Ödendi'
        }
        return status_map.get(status, 'Bilinmiyor')
    
    def show_add_product_to_bill_menu(self):
        """Adisyona ürün ekleme menüsünü göster"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        products = app.db.get_all_products()
        
        menu_items = []
        for product in products:
            menu_items.append({
                "text": f"{product['name']} - ₺{product['sale_price']:.2f}",
                "on_release": lambda x=product: self.add_product_to_bill(x['id']),
                "viewclass": "OneLineListItem",
                "height": dp(48),
            })
        
        self.product_menu = MDDropdownMenu(
            caller=self.dialog.ids.container if self.dialog else self,
            items=menu_items,
            width_mult=4,
        )
        self.product_menu.open()
    
    def add_product_to_bill(self, product_id):
        """Adisyona ürün ekle"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        
        if not app.db or not self.current_bill_id:
            return
        
        if self.product_menu:
            self.product_menu.dismiss()
        
        success = app.db.add_bill_item(self.current_bill_id, product_id, 1)
        
        if success:
            toast("Ürün eklendi!")
            if self.dialog:
                self.dialog.dismiss()
            self.show_bill_detail(self.current_bill_id)
        else:
            toast("Ürün eklenemedi!")
    
    def remove_item_from_bill(self, item_id):
        """Adisyondan ürün çıkar"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        success = app.db.remove_bill_item(item_id)
        
        if success:
            toast("Ürün çıkarıldı!")
            if self.dialog:
                self.dialog.dismiss()
            if self.current_bill_id:
                self.show_bill_detail(self.current_bill_id)
        else:
            toast("Ürün çıkarılamadı!")
    
    def show_payment_dialog(self, bill_id):
        """Ödeme dialogunu göster"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        # Adisyon bilgilerini al
        bill = app.db.get_bill(bill_id)
        
        if not bill:
            return
        
        if self.dialog:
            self.dialog.dismiss()
        
        content = MDBoxLayout(
            orientation="vertical",
            spacing="12dp",
            size_hint_y=None,
            height="200dp"
        )
        
        from kivymd.uix.label import MDLabel
        content.add_widget(MDLabel(
            text=f"Kalan Tutar: ₺{bill['remaining_amount']:.2f}",
            font_style="H6"
        ))
        
        amount_field = MDTextField(
            hint_text="Ödeme Tutarı (₺) *",
            required=True,
            input_filter="float",
            text=str(bill['remaining_amount'])
        )
        
        # Ödeme yöntemi seçimi için dropdown menü
        payment_method_field = MDTextField(
            hint_text="Ödeme Yöntemi",
            text="Nakit",
            disabled=True
        )
        
        notes_field = MDTextField(hint_text="Notlar", multiline=True)
        
        content.add_widget(amount_field)
        content.add_widget(payment_method_field)
        content.add_widget(notes_field)
        
        self.dialog = MDDialog(
            title="Ödeme Al",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="İPTAL",
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="ÖDEME AL",
                    on_release=lambda x: self.process_payment(
                        bill_id,
                        amount_field.text,
                        'cash',
                        notes_field.text
                    )
                ),
            ],
        )
        self.dialog.open()
    
    def process_payment(self, bill_id, amount, payment_method, notes):
        """Ödemeyi işle"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        if not amount:
            toast("Ödeme tutarı zorunludur!")
            return
        
        try:
            amount = float(amount)
        except ValueError:
            toast("Geçersiz ödeme tutarı!")
            return
        
        if amount <= 0:
            toast("Ödeme tutarı 0'dan büyük olmalıdır!")
            return
        
        success = app.db.add_payment(bill_id, amount, payment_method, notes)
        
        if success:
            toast("Ödeme alındı!")
            self.dialog.dismiss()
            self.load_open_bills()
        else:
            toast("Ödeme alınamadı!")


Builder.load_string(KV)
