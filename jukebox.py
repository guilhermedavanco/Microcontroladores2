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

#Configurações iniciais da tela e inicialização do som
Config.set('graphics','fullscreen','0')
mixer.init()

#Classe da lista de músicas
class Lista(ListItemButton):
    pass

#Widget principal, que é exibido na tela. Contém todos os elementos separados
#em layouts do Kivy
class JukeboxWidget(BoxLayout):
    qtde_tocada = 0 #Contador de músicas
    
    #Definições de variáveis
    quant_text = ObjectProperty()
    lista_musicas = ObjectProperty()
    musica_atual = ObjectProperty()
    screen_manager = ObjectProperty()
    sound = None 
    
    #Listagem de musicas
    arquivos = os.listdir(
        "./Musicas")

    #Função responsável por tocar a música
    def pegar_nome(self):
        #Checagem de seleção de música
        if self.lista_musicas.adapter.selection:
            mixer.music.stop() #Caso haja música já tocando, para a música
            selection = self.lista_musicas.adapter.selection[0].text #Recebe o texto do item selecionado na lista
            self.musica_atual.text = 'Musica atual:\n' + selection #Exibição da música selecionada no label
            mixer.music.load('./Musicas/'+selection) #Carrega a música no player
            mixer.music.play()
            self.qtde_tocada += 1 #Incrementa o contador de músicas
            self.quant_text.text = str(self.qtde_tocada) #Contador é exibido em um label
            if self.qtde_tocada == 10: 
                #Reseta o programa
                self.mudar_pagina_musicas()
                self.qtde_tocada = 0
                self.quant_text.text = str(self.qtde_tocada)

    #Atualiza a lista de músicas
    def atualizar_lista(self):
        self.lista_musicas.adapter.data.extend(self.arquivos) #Adiciona os itens na lista
        self.lista_musicas._trigger_reset_populate() #Reseta a lista

    def parar_musica(self): 
        mixer.music.stop()

    #Funções de mudança de página
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
    
    #Conta a quantidade de pulsos, e, quando atingir a contagem, muda a página
    def HandlerDinheiro(self, pin):
        self.dinheiro += 1
        if self.dinheiro >= 2:
            self.jk.mudar_pagina_dinheiro()
            self.dinheiro = 0
     
    #Muda a página quando o sensor de presença for acionado
    def HandlerPresenca(self, pin):
        self.jk.mudar_pagina_presenca()

    #Cria o Widget
    def build(self):
        self.jk = JukeboxWidget()
        return self.jk

    #Inicialização geral do programa
    def on_start(self):
        #Chama a atualização da lista de músicas
        self.jk.atualizar_lista()
        
        #Configurações do GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23,GPIO.IN)
        GPIO.setup(24,GPIO.IN)
        GPIO.add_event_detect(23,GPIO.RISING)
        GPIO.add_event_callback(23,self.HandlerDinheiro)
        GPIO.add_event_detect(24,GPIO.RISING)
        GPIO.add_event_callback(24,self.HandlerPresenca)

    #Limpa o GPIO ao finalizar o programa
    def on_stop(self):
        GPIO.cleanup()

#Inicia o programa
juke = JukeboxApp()
juke.run()


