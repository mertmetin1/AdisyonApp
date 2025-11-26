"""
Ürün yönetimi ekranı
"""

import os
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineAvatarIconListItem, ImageLeftWidget, IconRightWidget, IconLeftWidget
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast

KV = """
<ProductsScreen>:
    name: "products"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Ürün Yönetimi"
            elevation: 4
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]
            right_action_items: [["plus", lambda x: root.show_add_product_dialog()]]

        MDBoxLayout:
            orientation: "vertical"
            padding: "8dp"
            spacing: "8dp"

            MDTextField:
                id: search_field
                hint_text: "Ürün ara..."
                icon_right: "magnify"
                size_hint_y: None
                height: "48dp"
                on_text: root.search_products(self.text)

            ScrollView:
                MDList:
                    id: products_list
"""


class ProductsScreen(MDScreen):
    """Ürün yönetimi ekranı"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.file_manager = None
        self.selected_image_path = ""
        self.edit_product_id = None
    
    def on_enter(self):
        """Ekran görüntülendiğinde"""
        self.load_products()
    
    def load_products(self):
        """Ürünleri yükle"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        try:
            products = app.db.get_all_products()
            
            self.ids.products_list.clear_widgets()
            
            for product in products:
                item = TwoLineAvatarIconListItem(
                    text=product['name'],
                    secondary_text=f"₺{product['sale_price']:.2f} | Kar: %{product['profit_margin']:.1f}",
                    on_release=lambda x, p=product: self.show_product_detail(p)
                )
                
                # Resim varsa göster
                if product.get('image_path') and os.path.exists(product['image_path']):
                    item.add_widget(ImageLeftWidget(source=product['image_path']))
                else:
                    item.add_widget(IconLeftWidget(icon="food"))
                
                # Düzenle butonu
                edit_icon = IconRightWidget(
                    icon="pencil",
                    on_release=lambda x, p=product: self.show_edit_product_dialog(p)
                )
                item.add_widget(edit_icon)
                
                self.ids.products_list.add_widget(item)
        except Exception as e:
            print(f"Error loading products: {e}")
            toast(f"Ürünler yüklenirken hata: {str(e)}")
    
    def search_products(self, search_term):
        """Ürün ara"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        if not search_term:
            self.load_products()
            return
        
        products = app.db.search_products(search_term)
        
        self.ids.products_list.clear_widgets()
        
        for product in products:
            item = TwoLineAvatarIconListItem(
                text=product['name'],
                secondary_text=f"₺{product['sale_price']:.2f} | Kar: %{product['profit_margin']:.1f}",
                on_release=lambda x, p=product: self.show_product_detail(p)
            )
            
            if product.get('image_path') and os.path.exists(product['image_path']):
                item.add_widget(ImageLeftWidget(source=product['image_path']))
            else:
                item.add_widget(IconLeftWidget(icon="food"))
            
            edit_icon = IconRightWidget(
                icon="pencil",
                on_release=lambda x, p=product: self.show_edit_product_dialog(p)
            )
            item.add_widget(edit_icon)
            
            self.ids.products_list.add_widget(item)
    
    def show_add_product_dialog(self):
        """Yeni ürün ekleme dialogunu göster"""
        self.edit_product_id = None
        self.selected_image_path = ""
        
        content = MDBoxLayout(
            orientation="vertical",
            spacing="12dp",
            size_hint_y=None,
            height="400dp"
        )
        
        name_field = MDTextField(hint_text="Ürün Adı *", required=True)
        description_field = MDTextField(hint_text="Açıklama", multiline=True)
        sale_price_field = MDTextField(hint_text="Satış Fiyatı (₺) *", required=True, input_filter="float")
        cost_price_field = MDTextField(hint_text="Maliyet Fiyatı (₺)", input_filter="float")
        category_field = MDTextField(hint_text="Kategori")
        stock_field = MDTextField(hint_text="Stok Miktarı", input_filter="int")
        
        image_button = MDRaisedButton(
            text="Resim Seç",
            on_release=lambda x: self.show_file_manager()
        )
        
        content.add_widget(name_field)
        content.add_widget(description_field)
        content.add_widget(sale_price_field)
        content.add_widget(cost_price_field)
        content.add_widget(category_field)
        content.add_widget(stock_field)
        content.add_widget(image_button)
        
        self.dialog = MDDialog(
            title="Yeni Ürün Ekle",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="İPTAL",
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="EKLE",
                    on_release=lambda x: self.save_product(
                        name_field.text,
                        sale_price_field.text,
                        cost_price_field.text,
                        description_field.text,
                        category_field.text,
                        stock_field.text
                    )
                ),
            ],
        )
        self.dialog.open()
    
    def show_edit_product_dialog(self, product):
        """Ürün düzenleme dialogunu göster"""
        self.edit_product_id = product['id']
        self.selected_image_path = product.get('image_path', '')
        
        content = MDBoxLayout(
            orientation="vertical",
            spacing="12dp",
            size_hint_y=None,
            height="400dp"
        )
        
        name_field = MDTextField(hint_text="Ürün Adı *", text=product['name'], required=True)
        description_field = MDTextField(hint_text="Açıklama", text=product.get('description', ''), multiline=True)
        sale_price_field = MDTextField(hint_text="Satış Fiyatı (₺) *", text=str(product['sale_price']), required=True, input_filter="float")
        cost_price_field = MDTextField(hint_text="Maliyet Fiyatı (₺)", text=str(product['cost_price']), input_filter="float")
        category_field = MDTextField(hint_text="Kategori", text=product.get('category', ''))
        stock_field = MDTextField(hint_text="Stok Miktarı", text=str(product['stock_quantity']), input_filter="int")
        
        image_button = MDRaisedButton(
            text="Resim Değiştir",
            on_release=lambda x: self.show_file_manager()
        )
        
        content.add_widget(name_field)
        content.add_widget(description_field)
        content.add_widget(sale_price_field)
        content.add_widget(cost_price_field)
        content.add_widget(category_field)
        content.add_widget(stock_field)
        content.add_widget(image_button)
        
        self.dialog = MDDialog(
            title="Ürün Düzenle",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="SİL",
                    text_color=(1, 0, 0, 1),
                    on_release=lambda x: self.delete_product(product['id'])
                ),
                MDFlatButton(
                    text="İPTAL",
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="KAYDET",
                    on_release=lambda x: self.save_product(
                        name_field.text,
                        sale_price_field.text,
                        cost_price_field.text,
                        description_field.text,
                        category_field.text,
                        stock_field.text
                    )
                ),
            ],
        )
        self.dialog.open()
    
    def save_product(self, name, sale_price, cost_price, description, category, stock):
        """Ürünü kaydet"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        # Validasyon
        if not name or not sale_price:
            toast("Ürün adı ve satış fiyatı zorunludur!")
            return
        
        try:
            sale_price = float(sale_price)
            cost_price = float(cost_price) if cost_price else 0
            stock = int(stock) if stock else 0
        except ValueError:
            toast("Geçersiz fiyat veya stok değeri!")
            return
        
        if self.edit_product_id:
            # Güncelle
            app.db.update_product(
                self.edit_product_id,
                name=name,
                sale_price=sale_price,
                cost_price=cost_price,
                description=description,
                category=category,
                stock_quantity=stock,
                image_path=self.selected_image_path
            )
            toast("Ürün güncellendi!")
        else:
            # Yeni ekle
            app.db.add_product(
                name=name,
                sale_price=sale_price,
                cost_price=cost_price,
                description=description,
                category=category,
                stock_quantity=stock,
                image_path=self.selected_image_path
            )
            toast("Ürün eklendi!")
        
        self.dialog.dismiss()
        self.load_products()
    
    def delete_product(self, product_id):
        """Ürünü sil"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        
        if not app.db:
            return
        
        app.db.delete_product(product_id)
        toast("Ürün silindi!")
        
        self.dialog.dismiss()
        self.load_products()
    
    def show_product_detail(self, product):
        """Ürün detaylarını göster"""
        content = MDBoxLayout(
            orientation="vertical",
            spacing="8dp",
            padding="8dp",
            size_hint_y=None,
            height="300dp"
        )
        
        info_text = f"""
[b]Ürün:[/b] {product['name']}
[b]Kategori:[/b] {product.get('category', '-')}
[b]Açıklama:[/b] {product.get('description', '-')}

[b]Satış Fiyatı:[/b] ₺{product['sale_price']:.2f}
[b]Maliyet:[/b] ₺{product['cost_price']:.2f}
[b]Kar Marjı:[/b] %{product['profit_margin']:.1f}

[b]Stok:[/b] {product['stock_quantity']} adet
        """
        
        from kivymd.uix.label import MDLabel
        content.add_widget(MDLabel(text=info_text.strip(), markup=True))
        
        detail_dialog = MDDialog(
            title="Ürün Detayı",
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(
                    text="KAPAT",
                    on_release=lambda x: detail_dialog.dismiss()
                ),
            ],
        )
        detail_dialog.open()
    
    def show_file_manager(self):
        """Dosya yöneticisini göster"""
        if not self.file_manager:
            self.file_manager = MDFileManager(
                exit_manager=self.exit_manager,
                select_path=self.select_path,
            )
        
        self.file_manager.show(os.path.expanduser("~"))
    
    def select_path(self, path):
        """Dosya seçildiğinde"""
        self.selected_image_path = path
        toast(f"Resim seçildi: {os.path.basename(path)}")
        self.exit_manager()
    
    def exit_manager(self, *args):
        """Dosya yöneticisini kapat"""
        if self.file_manager:
            self.file_manager.close()


Builder.load_string(KV)
