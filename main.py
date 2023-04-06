import kivy
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, NumericProperty

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.widget import Widget
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.button import MDTextButton

from kivy.config import ConfigParser
from kivy.uix.settings import Settings
from kivy.clock import Clock
from kivymd.utils import asynckivy

from kivy.uix.screenmanager import CardTransition, SlideTransition

# Builder.load_file("drinkcount.kv")
kivy.require('2.1.0')

from kivy.app import App

class ScreenManagement(MDScreenManager):
    def change(self, screen):
        self.current = screen
    def goto_settings(self):
        self.transition = CardTransition()
        self.transition.direction = 'up'
        self.transition.mode = 'push'
        self.current = 'menu'
    def goto_data(self):
        self.transition = SlideTransition()
        self.transition.direction = 'left'
        self.current = 'data'
    def goto_main(self):
        if self.current == 'menu':
            self.transition = CardTransition()
            self.transition.direction = 'down'
            self.transition.mode = 'pop'
        else:
            self.transition = SlideTransition()
            self.transition.direction = 'right'
        self.current = 'main'


class Item(MDGridLayout):
    name = StringProperty()
    icon = StringProperty()
    marks = NumericProperty()
    def __init__(self, **kwargs):
        self.value = 0
        self.marks = 0
        super(Item, self).__init__(**kwargs)
    def item_press(self, who):
        print('Press', who, self.ids.name.text)
        self.clock = Clock.schedule_interval(self.item_hold, .01)
    def item_hold(self, dt):
        self.value = self.value + 1
        self.set_bars(self.value)
        if self.value >= 100:
            self.value = 0
            self.clock.cancel()
            self.marks = self.marks + 1
            self.update()
    def item_release(self, who):
        self.clock.cancel()
        self.value = 0
        self.set_bars(self.value)
    def set_bars(self, value):
        self.ids.pbt.value = value
        self.ids.pbb.value = value
    def update(self):
        print('Updating...', self.marks)
        for i, mark in enumerate(self.ids.marks.children):
            mark.background_color = (0, 0, 1, 1) if (20 - i) <= self.marks else (.5, .5, .5, 1)

class MainScreen(MDScreen):
    info = StringProperty()
    items = ObjectProperty()
    def do_action(self):
        self.info = "New info"
        self.items.add_widget(Item(name='Test'))

class DataScreen(MDScreen):
    pass

class MenuScreen(MDScreen):
    settings = ObjectProperty()
    def build(self):
        self.config = ConfigParser()
        self.config.read('drinkcount.ini')

class Main(MDBoxLayout):
    manager = ObjectProperty()
    bar = ObjectProperty()
    def action_back(self):
        self.bar.right_action_items = [
            [ 'chevron-left', lambda x: self.goto_main() ]
        ]
    def goto_settings(self):
        self.manager.goto_settings()
        self.action_back()
    def goto_data(self):
        self.manager.goto_data()
        self.action_back()
    def goto_main(self):
        self.manager.goto_main()
        self.bar.right_action_items = [
            [ 'chart-bar', lambda x: self.goto_data() ],
            [ 'menu', lambda x: self.goto_settings() ],
        ]

class DrinkCountApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        return Main()
    def on_start(self):
        async def generate():
            self.root.goto_main()
        Clock.schedule_once(lambda x: asynckivy.start(generate()))



if __name__ == '__main__':
    print("Starting...")
    DrinkCountApp().run()