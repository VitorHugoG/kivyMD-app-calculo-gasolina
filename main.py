from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.list import ThreeLineListItem
import sqlite3 
from datetime import date

TouchBehavior.duration_long_touch = 0.01


class MyLayout(BoxLayout):

    scr_mngr = ObjectProperty(None)

    def calcular(self):

        self.gasolina = self.scr_mngr.screen1.gasolina.text
        self.alcool = self.scr_mngr.screen1.alcool.text

        proibidos = ',;]^`-{}'

        if((self.gasolina.isalpha() or self.gasolina.strip() in proibidos) | (self.alcool.isalpha() or self.alcool.strip() in proibidos)):
            self.scr_mngr.screen1.label.text = 'Digite um valor válido!'
        else:
            porcentagem = float(self.alcool)/float(self.gasolina)  

            self.resposta = "Melhor escolha é Alcool " if porcentagem <= 0.85 else "Melhor escolha é Gasolina"

            self.scr_mngr.screen1.label.text = self.resposta    
        self.valor = 0
        
    def inserir_banco(self):
        
        proibidos = ',;]^`-{}'

        self.gasolina = self.scr_mngr.screen1.gasolina.text
        self.alcool = self.scr_mngr.screen1.alcool.text

        if((self.gasolina.isalpha() or self.gasolina.strip() in proibidos) | (self.alcool.isalpha() or self.alcool.strip() in proibidos)):
            self.scr_mngr.screen1.label.text = 'Digite um valor válido!'
        else:
            today = date.today()
            porcentagem = float(self.alcool)/float(self.gasolina) 

            self.melhor_combustivel = self.alcool if porcentagem <= 0.85 else self.gasolina

            conn = sqlite3.connect('historico_alcool.db')

            #Criando um cursor

            c = conn.cursor()

            #inserindo no banco de dados
            
            c.execute("INSERT INTO combustivel VALUES (:first, :second, :third)",
                {
                    'first': self.melhor_combustivel,
                    'second': today,
                    'third': self.resposta
                }
            )

            #Mensagem de aceito

            self.scr_mngr.screen1.label.text = "Adicionado ao banco!"

            #limpando os inputs
            self.scr_mngr.screen1.gasolina.text = ""
            self.scr_mngr.screen1.alcool.text = ""

            #commit 

            conn.commit()

            #fechando o banco de dados

            conn.close()
    
    def mostrar_precos(self):
        
        self.valor = 0 
       
        conn = sqlite3.connect('historico_alcool.db')

        #Criando um cursor

        c = conn.cursor()

        #select no banco de dados
        
        c.execute("SELECT * FROM combustivel ")

        dados = c.fetchall()

        for dado in dados:
            self.scr_mngr.screen3.container.add_widget(
                ThreeLineListItem(
                    text=f'Preço:{dado[0]}', 
                    secondary_text = f'Data:{dado[1]}',
                    tertiary_text = f'{dado[2]}',
                    _height = 180
                )
            )


        #commit 

        conn.commit()

        #fechando o banco de dados

        conn.close()

            


KV = '''
MyLayout:
    scr_mngr: scr_mngr
    orientation: 'vertical'
    manager: scr_mngr
    ScreenManager:
        id: scr_mngr
        screen1: screen1
        screen3: screen3

        Screen:
            id:screen2
            name:'screen2'
            md_bg_color: 'black'
            FloatLayout:
                Image:
                    source:'bomba-de-combustivel.png'
                    size_hint_y: .2
                    size_hint_x: .2
                    pos_hint:{"center_x": .5, "center_y": .8}

                MDIconButton:
                    icon: "bluetooth"
                    pos_hint: {"center_x": .5, "center_y": .2}
                    size_hint_x: .2
                    size_hint_y: .1

                MDRectangleFlatButton:
                    text: "Iniciar"
                    theme_text_color: "Custom"
                    text_color: "white"
                    line_color: "white"
                    size_hint_x: .5
                    size_hint_y: .1
                    pos_hint: {"center_x": .5, "center_y": .620}
                    on_press: root.manager.current = 'screen1'
                
                MDRectangleFlatButton:
                    text: "Melhores preços gasolina"
                    theme_text_color: "Custom"
                    text_color: "white"
                    line_color: "white"
                    size_hint_x: .5
                    size_hint_y: .1
                    pos_hint: {"center_x": .5, "center_y": .450}
                    on_press: root.manager.current = 'screen3'
                    
        Screen:
            id:screen3
            name:'screen3'
            md_bg_color: 'black'
            container:container


            MDScrollView:  
                MDList:
                    id:container
                    pos_hint: {"center_x": .5, "center_y": .6}
                    
                    

            FloatLayout:
                MDIconButton:
                    icon: "arrow-u-left-top"
                    pos_hint: {"center_x": .1, "center_y": .950}
                    on_press: root.manager.current = 'screen2'

                
                MDRaisedButton:
                    text: 'Mostrar'
                    size_hint_x: .4
                    size_hint_y: .1
                    md_bg_color: "purple"
                    pos_hint: {'center_y': .1, 'center_x': .7}
                    on_release: root.mostrar_precos()
                
                
            

        Screen:
            id:screen1
            name:'screen1'
            alcool: alcool
            gasolina: gasolina
            label: label

            FloatLayout:

                MDIconButton:
                    icon: "arrow-u-left-top"
                    pos_hint: {"center_x": .1, "center_y": .950}
                    on_press: root.manager.current = 'screen2'

                MDLabel:
                    text: "Calcular Combustivel"
                    halign: "center"
                    theme_text_color: "Custom"
                    pos_hint: {"center_y": .9 , "center_x": .5}
                    text_color: "white"
                    font_style: "H5"
                
                MDTextField:
                    id: alcool
                    hint_text: "Alcool"
                    helper_text: "Digite o valor do alcool"
                    pos_hint: {"center_y": .8 , "center_x": .5}
                    size_hint_x: .8
                    size_hint_y: .1
                    input_filter: 'float'
                    required: True
                
        
                MDTextField:
                    id: gasolina
                    hint_text: "Gasolina"
                    helper_text: "Digite o valor da Gasolina"
                    pos_hint: {"center_y": .6 , "center_x": .5}
                    size_hint_x: .8
                    size_hint_y: .1
                    input_filter: 'float'
                    required: True
        
                MDRaisedButton:
                    text: 'Calcular'
                    size_hint_x: .5
                    size_hint_y: .1
                    md_bg_color: "purple"
                    pos_hint: {'center_y': .420, 'center_x': .5}
                    on_release: root.calcular()

                MDRectangleFlatIconButton:
                    text: "Salvar Melhor Opção"
                    size_hint_x: .5
                    size_hint_y: .1
                    line_color: 0,0,0,0
                    md_bg_color: "purple"
                    text_color: "white"
                    icon: "database-arrow-up-outline"
                    pos_hint: {"center_x": .5, "center_y": .280}
                    on_release: root.inserir_banco()
                    
                
                MDLabel:
                    id: label
                    text: "Insira os valores"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 132, 255, 111, 1
                    pos_hint: {'center_y': .1, 'center_x': .5}
                    font_style: 'H5'
            
        
        
'''


class Projeto(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        
        #Criando uma conexão com o banco de dados

        conn = sqlite3.connect('historico_alcool.db')

        #Criando um cursor

        c = conn.cursor()

        #Criando a tabela Melhores Combustiveis

        c.execute(""" CREATE TABLE if not exists combustivel(
            preco real,
            data text,
            tipo text
        )
        
        """)

        #commit 

        conn.commit()

        #fechando o banco de dados

        conn.close()
        

        return Builder.load_string(KV)


Projeto().run()
