import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.core.audio import SoundLoader
from pygame import mixer
from kivy.uix.screenmanager import ScreenManager, Screen
import RPi.GPIO as GPIO
from kivy.config import Config

Config.set('graphics', 'fullscreen', '0')
mixer.init()

pin_noteiro = 23
pin_presenca = 24


class Lista(ListItemButton):
    pass


class JukeboxWidget(BoxLayout):
    qtde_tocada = 0
    quant_text = ObjectProperty()
    lista_musicas = ObjectProperty()
    musica_atual = ObjectProperty()
    screen_manager = ObjectProperty()
    arquivos = os.listdir(
        "./Musicas")
    sound = None

    def pegar_nome(self):
        if self.lista_musicas.adapter.selection:
            mixer.music.stop()
            selection = self.lista_musicas.adapter.selection[0].text
            self.musica_atual.text = 'Musica atual:\n' + selection
            mixer.music.load('./Musicas/'+selection)
            mixer.music.play()
            self.qtde_tocada += 1
            self.quant_text.text = str(self.qtde_tocada)
            if self.qtde_tocada == 10:
                self.qtde_tocada = 0
                self.quant_text.text = str(self.qtde_tocada)
                self.mudar_pagina_musicas()

    def atualizar_lista(self):
        self.lista_musicas.adapter.data.extend(self.arquivos)
        self.lista_musicas._trigger_reset_populate()

    def parar_musica(self):
        mixer.music.stop()

    def mudar_pagina_dinheiro(self):
        self.screen_manager.current = "principal"

    def mudar_pagina_musicas(self):
        self.screen_manager.current = "branca"

    def mudar_pagina_presenca_high():
        if self.screen_manager.current == "branca":
            self.screen_manager.current = "dinheiro"

    def mudar_pagina_presenca_low():
        if self.screen_manager.current == "dinheiro":
            self.screen_manager.current = "branca"


class JukeboxApp(App):

    jk = None
    dinheiro = 0

    def HandlerDinheiro(self, pin):
        self.dinheiro += 1
        if self.dinheiro >= 4:
            self.jk.mudar_pagina_dinheiro()
            self.dinheiro = 0

    def HandlerPresenca(self, pin):
        if GPIO.input(pin_presenca):
            self.jk.mudar_pagina_presenca_high()
        else:
            self.jk.mudar_pagina_presenca_low()

    def build(self):
        self.jk = JukeboxWidget()
        return self.jk

    def on_start(self):
        self.jk.atualizar_lista()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin_noteiro, GPIO.IN)
        GPIO.add_event_detect(pin_noteiro, GPIO.RISING)
        GPIO.add_event_callback(pin_noteiro, self.HandlerDinheiro)
        GPIO.setup(pin_presenca, GPIO.IN)
        GPIO.add_event_detect(pin_presenca, GPIO.BOTH)
        GPIO.add_event_callback(pin_presenca, self.HandlerPresenca)

    def on_stop(self):
        GPIO.cleanup()


juke = JukeboxApp()
juke.run()
