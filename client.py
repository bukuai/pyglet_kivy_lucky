
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App

import threading
import socket

Builder.load_string('''
<Main>
    name:'main'
    BoxLayout:
        orientation:'vertical'
        Button:
            text:'Prize 1'
            font_size:'35dp'
            type:'1'
            on_release: self.parent.parent.click(self)
        Button:
            text:'Prize 2'
            font_size:'35dp'
            type:'2'
            on_release: self.parent.parent.click(self)
        Button:
            text:'Prize 3'
            font_size:'35dp'
            type:'3'
            on_release: self.parent.parent.click(self)
        Button:
            text:'Sunshine'
            font_size:'35dp'
            type:'5'
            on_release: self.parent.parent.click(self)
        Button:
            text:'Single addition'
            font_size:'35dp'
            type:'100'
            on_release: self.parent.parent.click(self)
        Button:
            text:'host setting'
            font_size:'20dp'
            on_release: self.parent.parent.set()

<Confirm>
    name:'confirm'
    label:label
    b:b
    BoxLayout:
        orientation:'vertical'
        Label:
            id:label
            text:''
            type:''
            font_size:'35dp'
        Button:
            id:b
            text:'Click here to RUN!'
            font_size:'32dp'
            size_hint_y:None
            height:'100dp'
            disabled:False
            on_release:self.parent.parent.click(self)
        Label:
            text:''
        Button:
            text:'Back'
            size_hint_y:None
            height:'70dp'
            on_release:self.parent.parent.back()
        Label:
            text:''
<Setting>
    name:'setting'
    ip:ip
    BoxLayout:
        orientation:'vertical'
        Label:
        TextInput:
            id:ip
            text:'192.168.43.42'
            font_size:'40dp'
            size_hint_y:None
            height:'60dp'
        Label:
        Button:
            text:'save and back'
            size_hint_y:None
            height:'60dp'
            on_release:self.parent.parent.click()
        Label:
            
<ScreenManagement>
    id:sm
    m:m
    c:c
    s:s
    Main:
        id:m
    Confirm:
        id:c
    Setting:
        id:s
''')


def conn(ip, data):
    sk = socket.socket()
    sk.connect((ip, 9999))  # 连接服务器
    sk.send(data.encode('utf8'))
    sk.close()


class Main(Screen):
    def click(self, instance):
        ip = self.parent.s.ip.text
        msg = '0|'+instance.type
        t = threading.Thread(target=conn, args=(ip, msg))
        t.start()

        self.parent.current = 'confirm'
        self.parent.c.label.text = instance.text
        self.parent.c.label.type = instance.type

    def set(self):
        self.parent.current = 'setting'


class Confirm(Screen):
    def back(self):
        self.b.disabled = False
        self.parent.current = 'main'

    def click(self, instance):
        ip = self.parent.s.ip.text
        msg = '1|' + self.label.type
        t = threading.Thread(target=conn, args=(ip, msg))
        t.start()

        instance.disabled = True


class Setting(Screen):
    def click(self):
        self.parent.current = 'main'


class ScreenManagement(ScreenManager):
    pass


class MyApp(App):
    def build(self):
        return ScreenManagement()

if __name__ == '__main__':
    MyApp().run()