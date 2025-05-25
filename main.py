import sys
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QGridLayout, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# --- Fuzzy Girdi ve Çıktılar Tanımı ---

yol = ctrl.Antecedent(np.arange(0, 11, 1), 'yol')
hava = ctrl.Antecedent(np.arange(0, 11, 1), 'hava')
yuk = ctrl.Antecedent(np.arange(0, 101, 1), 'yuk')
trafik = ctrl.Antecedent(np.arange(0, 11, 1), 'trafik')
mesafe = ctrl.Antecedent(np.arange(0, 1001, 1), 'mesafe')

ortalama_hiz = ctrl.Consequent(np.arange(0, 121, 1), 'ortalama_hiz')
sure = ctrl.Consequent(np.arange(0, 241, 1), 'sure')  # dakika cinsinden

# --- Üyelik Fonksiyonları (Girdiler) ---
yol['duz'] = fuzz.trimf(yol.universe, [0, 0, 3])
yol['yokus'] = fuzz.trimf(yol.universe, [2, 5, 8])
yol['virajli'] = fuzz.trimf(yol.universe, [7, 10, 10])

hava['acik'] = fuzz.trimf(hava.universe, [0, 0, 3])
hava['bulutlu'] = fuzz.trimf(hava.universe, [2, 5, 8])
hava['yagisli'] = fuzz.trimf(hava.universe, [7, 10, 10])

yuk['hafif'] = fuzz.trimf(yuk.universe, [0, 0, 30])
yuk['orta'] = fuzz.trimf(yuk.universe, [20, 50, 80])
yuk['agir'] = fuzz.trimf(yuk.universe, [70, 100, 100])

trafik['az'] = fuzz.trimf(trafik.universe, [0, 0, 3])
trafik['orta'] = fuzz.trimf(trafik.universe, [2, 5, 8])
trafik['yogun'] = fuzz.trimf(trafik.universe, [7, 10, 10])

mesafe['kisa'] = fuzz.trimf(mesafe.universe, [0, 0, 200])
mesafe['orta'] = fuzz.trimf(mesafe.universe, [150, 400, 700])
mesafe['uzun'] = fuzz.trimf(mesafe.universe, [600, 1000, 1000])

# --- Üyelik Fonksiyonları (Çıktılar) ---
ortalama_hiz['dusuk'] = fuzz.trimf(ortalama_hiz.universe, [0, 0, 40])
ortalama_hiz['orta'] = fuzz.trimf(ortalama_hiz.universe, [30, 60, 90])
ortalama_hiz['yuksek'] = fuzz.trimf(ortalama_hiz.universe, [80, 110, 120])

sure['kisa'] = fuzz.trimf(sure.universe, [0, 0, 60])
sure['orta'] = fuzz.trimf(sure.universe, [40, 90, 140])
sure['uzun'] = fuzz.trimf(sure.universe, [120, 180, 240])

# --- Kurallar ---
kurallar = [
    ctrl.Rule(yol['duz'] & hava['acik'] & yuk['hafif'] & trafik['az'] & mesafe['kisa'], 
              (ortalama_hiz['yuksek'], sure['kisa'])),
    ctrl.Rule(yol['duz'] & hava['bulutlu'] & yuk['orta'] & trafik['orta'] & mesafe['orta'], 
              (ortalama_hiz['orta'], sure['orta'])),
    ctrl.Rule(yol['virajli'] | hava['yagisli'] | yuk['agir'] | trafik['yogun'] | mesafe['uzun'], 
              (ortalama_hiz['dusuk'], sure['uzun'])),
    ctrl.Rule(yol['yokus'] & trafik['orta'], (ortalama_hiz['orta'], sure['orta'])),
    ctrl.Rule(yuk['agir'] & trafik['yogun'], (ortalama_hiz['dusuk'], sure['uzun'])),
    ctrl.Rule(mesafe['orta'] & trafik['az'], (ortalama_hiz['yuksek'], sure['orta'])),
    ctrl.Rule(mesafe['uzun'] & trafik['orta'], (ortalama_hiz['orta'], sure['uzun'])),
]

sistem = ctrl.ControlSystem(kurallar)
sim = ctrl.ControlSystemSimulation(sistem)

# --- PyQt5 GUI ---

class FuzzyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Fuzzy Motosiklet Yolculuğu Tahmin Sistemi")

        layout = QGridLayout()

        labels = ['Yol Durumu (0-10):', 'Hava Durumu (0-10):', 'Yük (0-100):', 'Trafik (0-10):', 'Mesafe (km, 0-1000):']
        self.entries = []

        for i, text in enumerate(labels):
            layout.addWidget(QLabel(text), i, 0)
            entry = QLineEdit()
            layout.addWidget(entry, i, 1)
            self.entries.append(entry)

        self.btnHesapla = QPushButton("Hesapla")
        layout.addWidget(self.btnHesapla, len(labels), 0)
        self.btnHesapla.clicked.connect(self.hesapla)

        self.btnTemizle = QPushButton("Temizle")
        layout.addWidget(self.btnTemizle, len(labels), 1)
        self.btnTemizle.clicked.connect(self.temizle)

        self.sonucLabel = QLabel("")
        layout.addWidget(self.sonucLabel, len(labels)+1, 0, 1, 2)

        # Grafik için Matplotlib FigureCanvas
        self.figure = Figure(figsize=(8, 3))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas, len(labels)+2, 0, 1, 2)

        self.setLayout(layout)
        self.resize(600, 400)

    def ciz_uyelik_fonksiyonlari(self, ort_hiz_degeri, sure_degeri):
        self.figure.clear()
        ax1 = self.figure.add_subplot(121)
        ax2 = self.figure.add_subplot(122)

        # Ortalama hız üyelik fonksiyonları
        ax1.plot(ortalama_hiz.universe, ortalama_hiz['dusuk'].mf, 'b', label='Düşük')
        ax1.plot(ortalama_hiz.universe, ortalama_hiz['orta'].mf, 'g', label='Orta')
        ax1.plot(ortalama_hiz.universe, ortalama_hiz['yuksek'].mf, 'r', label='Yüksek')
        ax1.axvline(ort_hiz_degeri, color='k', linestyle='--', label=f'Çıktı: {ort_hiz_degeri:.1f} km/h')
        ax1.set_title('Ortalama Hız')
        ax1.legend()

        # Süre üyelik fonksiyonları
        ax2.plot(sure.universe, sure['kisa'].mf, 'b', label='Kısa')
        ax2.plot(sure.universe, sure['orta'].mf, 'g', label='Orta')
        ax2.plot(sure.universe, sure['uzun'].mf, 'r', label='Uzun')
        ax2.axvline(sure_degeri, color='k', linestyle='--', label=f'Çıktı: {sure_degeri:.1f} dk')
        ax2.set_title('Süre (dakika)')
        ax2.legend()

        self.canvas.draw()

    def hesapla(self):
        try:
            y = float(self.entries[0].text())
            h = float(self.entries[1].text())
            yu = float(self.entries[2].text())
            t = float(self.entries[3].text())
            m = float(self.entries[4].text())

            if not (0 <= y <= 10 and 0 <= h <= 10 and 0 <= yu <= 100 and 0 <= t <= 10 and 0 <= m <= 1000):
                raise ValueError("Girdiler aralık dışı! Lütfen belirtilen aralıklarda değer girin.")

            sim.input['yol'] = y
            sim.input['hava'] = h
            sim.input['yuk'] = yu
            sim.input['trafik'] = t
            sim.input['mesafe'] = m

            sim.compute()

            ort_hiz = sim.output['ortalama_hiz']
            sure_saat = sim.output['sure']

            self.sonucLabel.setText(
                f"Tahmini Ortalama Hız: {ort_hiz:.2f} km/h\nTahmini Süre: {sure_saat:.2f} dakika"
            )

            self.ciz_uyelik_fonksiyonlari(ort_hiz, sure_saat)

        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def temizle(self):
        for entry in self.entries:
            entry.clear()
        self.sonucLabel.setText("")
        self.figure.clear()
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FuzzyApp()
    ex.show()
    sys.exit(app.exec_())