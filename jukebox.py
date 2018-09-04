import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.core.audio import SoundLoader

from pygame import mixer  # Load the required library

mixer.init()


class Lista(ListItemButton):
    pass


class JukeboxWidget(BoxLayout):

    lista_musicas = ObjectProperty()
    musica_atual = ObjectProperty()
    arquivos = os.listdir(
        "./Musicas")
    sound = None

    def pegar_nome(self):
        if self.lista_musicas.adapter.selection:
            mixer.music.stop()
            selection = self.lista_musicas.adapter.selection[0].text
            self.musica_atual.text = selection
            mixer.music.load('./Musicas/'+selection)
            mixer.music.play()

    def atualizar_lista(self):
        self.lista_musicas.adapter.data.extend(self.arquivos)
        self.lista_musicas._trigger_reset_populate()


class JukeboxApp(App):

    jk = None

    def build(self):
        self.jk = JukeboxWidget()
        return self.jk

    def on_start(self):
        self.jk.atualizar_lista()


juke = JukeboxApp()
juke.run()
