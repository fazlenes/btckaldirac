from kivy.app import App
from kivy.metrics import sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


class BinanceHesaplamaUI(BoxLayout):

    def __init__(self, **kwargs):
        super(BinanceHesaplamaUI, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = (sp(30), sp(30), sp(30), sp(30))

        scrollview = ScrollView(size_hint=(1, None), size=(sp(0), sp(500)))
        scrollview.add_widget(self.create_form())
        self.add_widget(scrollview)

        self.sonuc_label = Label(text='', size_hint=(1, None), font_size=sp(24), halign="center", valign="middle")
        self.add_widget(self.sonuc_label)

    def create_form(self):
        form_layout = GridLayout(cols=2, spacing=sp(10), size_hint_y=None, row_default_height=sp(70))
        form_layout.bind(minimum_height=form_layout.setter('height'))

        form_layout.add_widget(Label(text='Ana Para:', size_hint_x=None, width=sp(300), halign="right"))
        self.ana_para_input = TextInput(multiline=False, size_hint_x=None, width=sp(300), font_size=sp(18))
        form_layout.add_widget(self.ana_para_input)

        form_layout.add_widget(Label(text='Kaldıraç Oranı:', size_hint_x=None, width=sp(300), halign="right"))
        self.kaldirac_orani_input = TextInput(multiline=False, size_hint_x=None, width=sp(300), font_size=sp(18))
        form_layout.add_widget(self.kaldirac_orani_input)

        form_layout.add_widget(Label(text='Giriş Fiyatı:', size_hint_x=None, width=sp(300), halign="right"))
        self.giris_fiyati_input = TextInput(multiline=False, size_hint_x=None, width=sp(300), font_size=sp(18))
        form_layout.add_widget(self.giris_fiyati_input)

        form_layout.add_widget(Label(text='Çıkış Fiyatı:', size_hint_x=None, width=sp(300), halign="right"))
        self.cikis_fiyati_input = TextInput(multiline=False, size_hint_x=None, width=sp(300), font_size=sp(18))
        form_layout.add_widget(self.cikis_fiyati_input)

        form_layout.add_widget(Label(text='Pozisyon Tipi:', size_hint_x=None, width=sp(300), halign="right"))
        self.pozisyon_tipi_input = TextInput(multiline=False, size_hint_x=None, width=sp(300), font_size=sp(18))
        form_layout.add_widget(self.pozisyon_tipi_input)

        self.hesapla_button = Button(text='Hesapla', size_hint=(None, None), size=(sp(200), sp(50)), font_size=sp(18))
        self.hesapla_button.bind(on_press=self.on_hesapla)
        form_layout.add_widget(Label())  # Boş etiket, düğmenin altında bir boşluk oluşturmak için
        form_layout.add_widget(self.hesapla_button)

        return form_layout

    def on_hesapla(self, instance):
        ana_para = self.ana_para_input.text
        kaldirac_orani = self.kaldirac_orani_input.text
        giris_fiyati = self.giris_fiyati_input.text
        cikis_fiyati = self.cikis_fiyati_input.text
        pozisyon_tipi = self.pozisyon_tipi_input.text.lower()

        # Girdi kontrolü
        if not ana_para or not kaldirac_orani or not giris_fiyati or not cikis_fiyati or not pozisyon_tipi:
            self.sonuc_label.text = "Yanlış girdi! Lütfen tüm alanları doldurun."
            return

        try:
            ana_para = float(ana_para)
            kaldirac_orani = int(kaldirac_orani)
            giris_fiyati = float(giris_fiyati)
            cikis_fiyati = float(cikis_fiyati)
        except ValueError:
            self.sonuc_label.text = "Yanlış girdi! Lütfen sayısal değerleri doğru formatta girin."
            return

        pozisyon_buyuklugu = ana_para * kaldirac_orani

        # Kar veya zarar miktarını hesapla
        if pozisyon_tipi == "long":
            # Kar veya zarar hesaplama
            if cikis_fiyati > giris_fiyati:
                kar = (pozisyon_buyuklugu / giris_fiyati) * cikis_fiyati - pozisyon_buyuklugu
                zarar_miktari = 0
            else:
                kar = (pozisyon_buyuklugu / giris_fiyati) * giris_fiyati - pozisyon_buyuklugu
                zarar_miktari = abs((pozisyon_buyuklugu / giris_fiyati) * cikis_fiyati - pozisyon_buyuklugu)

            durum = "Kar" if kar > 0 else "Zarar"

            # Likidasyon fiyatını hesapla
            likidasyon_fiyati = giris_fiyati * (1 - 1 / kaldirac_orani)

        elif pozisyon_tipi == "short":
            # Kar veya zarar hesaplama
            if cikis_fiyati < giris_fiyati:
                kar = (pozisyon_buyuklugu / giris_fiyati) * abs(cikis_fiyati - giris_fiyati)
                zarar_miktari = 0
            else:
                kar = (pozisyon_buyuklugu / giris_fiyati) * abs(giris_fiyati - cikis_fiyati)
                zarar_miktari = abs((pozisyon_buyuklugu / giris_fiyati) * abs(cikis_fiyati - giris_fiyati))

            durum = "Kar" if kar > 0 else "Zarar"

            # Likidasyon fiyatını hesapla
            likidasyon_fiyati = giris_fiyati * (1 + 1 / kaldirac_orani)

        else:
            self.sonuc_label.text = "Yanlış girdi! Pozisyon tipi 'long' veya 'short' olmalıdır."
            return

        if durum == "Kar":
            self.sonuc_label.text = f"Net Durum: Kar\nKar Miktarı: {kar}\nLikidasyon Fiyatı: {likidasyon_fiyati}"
        elif durum == "Zarar":
            self.sonuc_label.text = f"Net Durum: Zarar\nZarar Miktarı: {zarar_miktari}\nLikidasyon Fiyatı: {likidasyon_fiyati}"


class BinanceHesaplamaApp(App):
    def build(self):
        return BinanceHesaplamaUI()


if __name__ == "__main__":
    BinanceHesaplamaApp().run()
