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
from kivy.uix.image import Image

Config.set('graphics','fullscreen','0')
mixer.init()


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
                self.mudar_pagina_musicas()
                self.qtde_tocada = 0
                self.quant_text.text = str(self.qtde_tocada)

                
    def atualizar_lista(self):
        self.lista_musicas.adapter.data.extend(self.arquivos)
        self.lista_musicas._trigger_reset_populate()

    def parar_musica(self):
        mixer.music.stop()

    def mudar_pagina_dinheiro(self):
        self.screen_manager.current = "principal"

    def mudar_pagina_musicas(self):
        self.screen_manager.current = "branca"
        
    def mudar_pagina_presenca(self):
        if self.screen_manager.current == "branca":
            self.screen_manager.current = "dinheiro"
            

class JukeboxApp(App):

    jk = None
    dinheiro = 0
    
    def HandlerDinheiro(self, pin):
        self.dinheiro += 1
        if self.dinheiro >= 2:
            self.jk.mudar_pagina_dinheiro()
            self.dinheiro = 0
            
    def HandlerPresenca(self, pin):
        self.jk.mudar_pagina_presenca()

    def build(self):
        self.jk = JukeboxWidget()
        return self.jk

    def on_start(self):
        self.jk.atualizar_lista()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23,GPIO.IN)
        GPIO.setup(24,GPIO.IN)
        GPIO.add_event_detect(23,GPIO.RISING)
        GPIO.add_event_callback(23,self.HandlerDinheiro)
        GPIO.add_event_detect(24,GPIO.RISING)
        GPIO.add_event_callback(24,self.HandlerPresenca)


    def on_stop(self):
        GPIO.cleanup()


juke = JukeboxApp()
juke.run()


