import kivy
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.uix.checkbox import CheckBox
from kivy.config import ConfigParser
from kivy.uix.settings import Settings
from kivy.clock import Clock
from kivy.uix.button import Button

# Builder.load_file("drinkcount.kv")
kivy.require('2.1.0')

from kivy.app import App

class ScreenManagement(ScreenManager):
    pass

class Item(GridLayout):
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

class MainScreen(Screen):
    info = StringProperty()
    items = ObjectProperty()
    def do_action(self):
        self.info = "New info"
        self.items.add_widget(Item(name='Test'))

class DataScreen(Screen):
    pass

class MenuScreen(Screen):
    settings = ObjectProperty()
    def build(self):
        self.config = ConfigParser()
        self.config.read('drinkcount.ini')

class DrinkCountApp(App):
    def build(self):
        return ScreenManagement()


if __name__ == '__main__':
    print("Starting...")
    DrinkCountApp().run()