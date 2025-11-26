# AdisyonApp - Kullanım Kılavuzu

## 📖 İçindekiler
1. [Başlangıç](#başlangıç)
2. [Ana Sayfa](#ana-sayfa)
3. [Ürün Yönetimi](#ürün-yönetimi)
4. [Adisyon İşlemleri](#adisyon-işlemleri)
5. [Ödeme Alma](#ödeme-alma)
6. [Raporlar](#raporlar)
7. [İpuçları](#ipuçları)

---

## Başlangıç

### İlk Çalıştırma

1. **Uygulamayı başlatın:**
   ```bash
   python start.py
   ```
   veya
   ```bash
   python main.py
   ```

2. **Örnek veriler ile başlayın:**
   ```bash
   python test_data.py
   ```
   Bu komut 15 örnek ürün ve 5 örnek adisyon oluşturur.

3. **Navigasyon:**
   - Sol üst menü ikonuna tıklayarak yan menüyü açın
   - Hızlı erişim için ana sayfadaki kartları kullanın

---

## Ana Sayfa

### Özellikler
- **Hoş Geldiniz Kartı**: Güncel tarih ve karşılama
- **Hızlı Erişim Menüsü**: 
  - Yeni Adisyon
  - Ürünler
  - Ödemeler
  - Raporlar
- **Bugünün Özeti**: Günlük istatistikler
  - Toplam adisyon sayısı
  - Toplam satış tutarı
  - Toplam tahsilat

### Kullanım
1. Uygulama her açıldığında ana sayfa gösterilir
2. İstatistikler otomatik güncellenir
3. Kartlara tıklayarak ilgili bölüme geçin

---

## Ürün Yönetimi

### Yeni Ürün Ekleme

1. **Ürünler** menüsüne gidin
2. Sağ üst köşedeki **+** ikonuna tıklayın
3. Formu doldurun:
   - **Ürün Adı*** (zorunlu)
   - **Açıklama** (opsiyonel)
   - **Satış Fiyatı*** (zorunlu) - TL cinsinden
   - **Maliyet Fiyatı** (opsiyonel) - Kar marjı için
   - **Kategori** (opsiyonel) - Örn: "Sıcak İçecekler"
   - **Stok Miktarı** (opsiyonel) - Envanter takibi
4. **Resim Seç** butonuna tıklayarak ürün resmi ekleyin
5. **EKLE** butonuna tıklayın

### Ürün Düzenleme

1. Ürün listesinden düzenlemek istediğiniz ürünü bulun
2. Sağdaki **kalem** ikonuna tıklayın
3. Bilgileri güncelleyin
4. **KAYDET** butonuna tıklayın

### Ürün Silme

1. Düzenle moduna girin
2. **SİL** butonuna tıklayın
3. Ürün "pasif" olarak işaretlenir (veritabanından silinmez)

### Ürün Arama

1. Üst kısımdaki arama kutusuna yazın
2. Ürünler otomatik filtrelenir
3. Arama: ad, açıklama veya kategori

### Kar Marjı Hesaplama

Kar marjı otomatik hesaplanır:
```
Kar Marjı = ((Satış Fiyatı - Maliyet) / Satış Fiyatı) × 100
```

**Örnek:**
- Satış Fiyatı: ₺35
- Maliyet: ₺12
- Kar Marjı: %65.7

---

## Adisyon İşlemleri

### Yeni Adisyon Oluşturma

1. **Adisyonlar** menüsüne gidin
2. Sağ üst köşedeki **+** ikonuna tıklayın
3. Bilgileri girin:
   - **Müşteri Adı*** (zorunlu)
   - **Masa Numarası** (opsiyonel)
   - **Notlar** (opsiyonel)
4. **OLUŞTUR** butonuna tıklayın

### Adisyona Ürün Ekleme

1. Adisyon listesinden ilgili adisyonu seçin
2. **ÜRÜN EKLE** butonuna tıklayın
3. Açılan menüden ürün seçin
4. Ürün otomatik eklenir (miktar: 1)
5. Aynı işlemi tekrarlayarak miktar artırın

### Adisyondan Ürün Çıkarma

1. Adisyon detayına gidin
2. Çıkarmak istediğiniz ürünün sağındaki **çöp kutusu** ikonuna tıklayın
3. Ürün adisyondan kaldırılır
4. Toplam otomatik güncellenir

### Adisyon Durumları

- **🕐 Açık**: Henüz ödeme yapılmamış
- **🕑 Kısmi Ödeme**: Kısmen ödenmiş
- **✅ Ödendi**: Tam ödenmiş ve kapatılmış

### Adisyon Listesi

**Açık Tab:**
- Sadece açık ve kısmen ödenmiş adisyonlar
- Hızlı erişim için

**Tümü Tab:**
- Tüm adisyonlar (açık, kısmi, ödendi)
- Geçmiş kayıtları görüntüleme

---

## Ödeme Alma

### Ödeme İşlemi

1. **Yöntem 1 - Adisyon Listesinden:**
   - Adisyon listesinde sağdaki **💰** ikonuna tıklayın

2. **Yöntem 2 - Adisyon Detayından:**
   - Adisyon detayını açın
   - **ÖDEME AL** butonuna tıklayın

3. **Ödeme Formunu Doldurun:**
   - **Ödeme Tutarı**: Varsayılan olarak kalan tutar gelir
   - **Ödeme Yöntemi**: Nakit, Kart veya Havale
   - **Notlar**: Opsiyonel açıklama

4. **ÖDEME AL** butonuna tıklayın

### Kısmi Ödeme

1. Ödeme tutarına kalan tutardan **daha az** bir miktar girin
2. Ödemeyi onaylayın
3. Adisyon durumu "Kısmi Ödeme" olarak güncellenir
4. Kalan tutar gösterilir
5. İstediğiniz kadar kısmi ödeme alabilirsiniz

### Tam Ödeme

1. Ödeme tutarına **kalan tutarın tamamını** girin
2. Ödemeyi onaylayın
3. Adisyon durumu "Ödendi" olarak güncellenir
4. Adisyon otomatik kapatılır

### Fazla Ödeme

1. Ödeme tutarına kalan tutardan **fazla** girebilirsiniz
2. Para üstü sistem tarafından hesaplanır
3. Adisyon tam ödendi olarak işaretlenir

### Ödeme Geçmişi

**Ödemeler** menüsünden:
- Tüm ödemeleri görüntüleyin
- Müşteri, tutar ve ödeme yöntemine göre filtreleme
- Bugünkü toplam tahsilat

---

## Raporlar

### Günlük Rapor

**Ana Bilgiler:**
- Toplam adisyon sayısı
- Toplam satış tutarı
- Toplam tahsilat

**Detaylı Rapor için:**
1. "Detaylı Rapor" butonuna tıklayın
2. Ödeme yöntemi dağılımı
3. En çok satan ürünler (Top 10)

### Aylık Rapor

1. "Aylık Rapor" butonuna tıklayın
2. Bulunduğunuz ayın özeti
3. Günlük satış dağılımı
4. Trend analizi

### Kar/Zarar Raporu

**Son 7 Gün için:**
- Toplam gelir
- Toplam maliyet
- Net kar
- Kar marjı (%)

**Detaylı Rapor:**
1. "Detaylı Kar/Zarar" butonuna tıklayın
2. Ürün bazında kar analizi
3. Her ürün için:
   - Satış adedi
   - Gelir
   - Maliyet
   - Net kar

### En Çok Satan Ürünler

- Ana sayfada günlük top 5
- Rapor sayfasında detaylı liste
- Adet ve ciro bazında sıralama

---

## İpuçları

### Hızlı İşlem Yöntemleri

1. **Hızlı Adisyon:**
   - Ana sayfadan direkt "Yeni Adisyon"
   - Müşteri adını girin ve hemen ürün ekleyin

2. **Toplu Ürün Ekleme:**
   - Aynı ürünü tekrar ekleyerek miktar artırın
   - Veya ürün detayında miktar düzenleyin

3. **Hızlı Ödeme:**
   - Adisyon listesinde direkt 💰 ikonuna tıklayın
   - Varsayılan tutar kabul edilirse direkt ödeyin

### Verimli Kullanım

1. **Kategoriler Kullanın:**
   - Ürünleri kategorilere ayırın
   - Arama ve filtreleme kolaylaşır

2. **Maliyet Girişi:**
   - Her ürün için maliyet girin
   - Kar analizi yapabilirsiniz

3. **Stok Takibi:**
   - Stok miktarlarını güncel tutun
   - Tükenen ürünleri kolayca görün

4. **Notlar:**
   - Adisyonlara not ekleyin
   - Özel istekleri kaydedin

### Güvenlik ve Yedekleme

1. **Veritabanı Yedekleme:**
   ```bash
   # Veritabanını kopyalayın
   cp database/adisyon.db database/adisyon_backup.db
   ```

2. **Düzenli Arşivleme:**
   - Aylık raporları kaydedin
   - Eski adisyonları arşivleyin

3. **Resim Yedekleme:**
   - `assets/images/` klasörünü yedekleyin
   - Ürün resimlerini kaybetmeyin

### Sorun Giderme

**Uygulama Açılmıyor:**
```bash
# Gereksinimleri kontrol edin
pip list | grep kivy

# Yeniden yükleyin
pip install -r requirements.txt
```

**Veritabanı Hatası:**
```bash
# Yeni veritabanı oluşturun
python test_data.py clear
python test_data.py
```

**Resimler Görünmüyor:**
- Resim yollarını kontrol edin
- Desteklenen formatlar: PNG, JPG, JPEG
- Android'de izinleri kontrol edin

### Kısayol Tuşları (Masaüstü)

- **Esc**: Dialog'ları kapat
- **Ctrl+Q**: Uygulamayı kapat (Windows/Linux)
- **Cmd+Q**: Uygulamayı kapat (Mac)

### Mobil Kullanım İpuçları

1. **Yan Menü**: Soldan sağa kaydırarak açın
2. **Geri Dönme**: Android geri tuşu ile
3. **Liste Kaydırma**: Yukarı/aşağı kaydırın
4. **Uzun Basma**: Detaylı bilgi için

---

## Sık Sorulan Sorular

**S: Ürün resmi nasıl eklenir?**
C: Ürün eklerken/düzenlerken "Resim Seç" butonuna tıklayın ve galeriden seçin.

**S: Adisyon silinebilir mi?**
C: Hayır, ancak kapalı adisyonlar listeye eklenmez. Geçmiş kayıt olarak saklanır.

**S: Kısmi ödeme kaç kez alınabilir?**
C: Sınırsız. Kalan tutar bitene kadar kısmi ödeme alabilirsiniz.

**S: Veritabanı nerede saklanır?**
C: `database/adisyon.db` dosyasında SQLite formatında.

**S: APK nasıl oluşturulur?**
C: `APK_BUILD.md` dosyasına bakın.

---

## Destek

Sorun yaşarsanız:
1. README.md dosyasını okuyun
2. Issue açın (GitHub)
3. Log dosyalarını kontrol edin

---

**Güncelleme:** 26 Kasım 2025
**Versiyon:** 1.0.0
