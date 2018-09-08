import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.core.audio import SoundLoader
from pygame import mixer
from kivy.uix.screenmanager import ScreenManager, Screen

mixer.init()


class Lista(ListItemButton):
    pass


class JukeboxWidget(BoxLayout):

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

    def atualizar_lista(self):
        self.lista_musicas.adapter.data.extend(self.arquivos)
        self.lista_musicas._trigger_reset_populate()

    def parar_musica(self):
        mixer.music.stop()

    def mudar_pagina(self):
        if self.screen_manager.current == "principal":
            self.screen_manager.current = "branca"
        else:
            self.screen_manager.current = "principal"


class JukeboxApp(App):

    jk = None

    def build(self):
        self.jk = JukeboxWidget()
        return self.jk

    def on_start(self):
        self.jk.atualizar_lista()


juke = JukeboxApp()
juke.run()
