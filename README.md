# 🏍️ Fuzzy Motosiklet Yolculuk Tahmin Sistemi

![Image](https://github.com/user-attachments/assets/ac75cd41-46b3-4cb9-9169-d41e3a4ac403)

##	AMAÇ
Motosikletle yapılan yolculuklarda; yol tipi, hava durumu, trafik yoğunluğu ve taşıma yükü gibi değişkenler göz önünde bulundurularak:
- Tahmini **ortalama hız**,
- Tahmini **süre** (dakika cinsinden)

değerlerini hesaplayan bir tahmin aracı geliştirmek.


## Projenin Çalıştırılması 

⦁ git clone https://github.com/oktayagdag/fuzzy-motosiklet.git 

⦁ cd fuzzy-motosiklet 

⦁ pip install -r requirements.txt 

⦁ python main.py 

 
## ⚙️ Kullanılan Teknolojiler

| Teknoloji | Açıklama |
|----------|----------|
| Python | Programlama dili |
| PyQt5 | Grafik arayüz (GUI) için |
| Scikit-Fuzzy (`skfuzzy`) | Bulanık mantık sistemi |
| NumPy | Sayısal işlemler |
| Matplotlib | Grafik çizimi (üyelik fonksiyonları görselleştirme) |

---
## 📌 Özellikler

- 5 adet bulanık girdi: yol, hava, yük, trafik, mesafe
- 2 adet bulanık çıktı: ortalama hız (km/h), tahmini süre (dakika)
- PyQt5 ile modern grafiksel kullanıcı arayüzü
- Matplotlib ile çıktıların üyelik fonksiyonları grafiği
- Kullanıcıdan anlık veri alarak bulanık çıkarım işlemi gerçekleştirme


## KODLARIN AKIŞI VE AÇIKLAMALARI

### 🔧 1. Kütüphanelerin İçe Aktarılması
 
```python
import sys
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from PyQt5.QtWidgets import ...
from matplotlib.backends.backend_qt5agg import ...
from matplotlib.figure import Figure
```
⦁ numpy: Sayısal işlemler ve diziler için.

⦁ skfuzzy: Bulanık mantık işlemleri için.

⦁ PyQt5: Arayüzü oluşturmak için.

⦁ matplotlib: Grafik çizmek için.


### 🎛️ 2. Girdi ve Çıktı Değişkenlerinin Tanımı

```python
yol = ctrl.Antecedent(...)
hava = ctrl.Antecedent(...)
...
ortalama_hiz = ctrl.Consequent(...)
sure = ctrl.Consequent(...)
```

⦁ Antecedent: Girdi (input) değişkenleri: yol, hava, yuk, trafik, mesafe.

⦁ Consequent: Çıktı (output) değişkenleri: ortalama_hiz, sure.


### 📈 3. Üyelik Fonksiyonları (Membership Functions)

```python
yol['duz'] = fuzz.trimf(yol.universe, [0, 0, 3])
...
ortalama_hiz['dusuk'] = fuzz.trimf(...)

```

⦁ Girdiler ve çıktılar, bulanık kümelere ayrılıyor:

⦁ Örn: yol → "düz", "yokuş", "virajlı"

⦁ ortalama_hiz → "düşük", "orta", "yüksek"

⦁ trimf: Üçgen üyelik fonksiyonu tanımlar.


### 📋 4. Kuralların Tanımı (Fuzzy Kuralları)


```python
kurallar = [
    ctrl.Rule(yol['duz'] & hava['acik'] & yuk['hafif'] & trafik['az'] & mesafe['kisa'],
              (ortalama_hiz['yuksek'], sure['kisa'])),
    ...
]
```

⦁ Her kural, girişlerin durumlarına göre ortalama hız ve süreyi belirler.

⦁ & (VE), | (VEYA) operatörleri ile mantıksal ifadeler oluşturulur.

⦁ 7 adet örnek kural tanımlanmış.

### 🧠 5. Kontrol Sistemi ve Simülasyon

```python
sistem = ctrl.ControlSystem(kurallar)
sim = ctrl.ControlSystemSimulation(sistem)
```
⦁ Kurallar bir kontrol sistemine yüklenir.

⦁ Girdi değerlerine göre çıktıların hesaplanabilmesi için sim nesnesi tanımlanır.


### 📦 Genel Akış Diyagramı (Kısa Özet)
1- Kullanıcı değerleri girer.

2- Fuzzy Logic sistemi bu değerlere göre:

3- Ortalama hız (km/h)

4- Yolculuk süresi (dakika)
hesaplar.

5- Sonuç ekrana yazılır.

Aynı zamanda üyelik fonksiyonları grafikle gösterilir.


### ✍️ Geliştirici
Oktay Akdağ – Bilişim Sistemleri ve Teknolojileri Bölümü

Bulanık Mantık – 2025

Danışman: Doktor Öğretim Üyesi HÜSEYİN YANIK
