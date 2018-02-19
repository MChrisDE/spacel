from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.properties import ObjectProperty
import os
from random import randint
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')
Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'resizable', 0)

from kivy.core.window import Window


class Game(FloatLayout):
    player = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.clock = Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.walls = []
        self.time = 120
    def update(self, dt):
        self.player.move()
        self.move_walls()
        for i in self.walls:
            if self.player.collide_widget(i):
                self.stop()
        if self.time > 20:
            self.time -= 0.1
        if randint(0, int(self.time)) == 1:
            self.spawn_wall()

    def spawn_wall(self):
        d = Wall()
        self.walls.append(d)
        self.add_widget(d)

    def move_walls(self):
        for i in self.walls:
            i.move()
            if i.x < (0 - i.width):
                self.walls.remove(i)

    def stop(self):
        self.clock.cancel()
        self.menu = Menu()
        self.add_widget(self.menu)

    def reset(self):
        self.clock.cancel()
        if self.walls:
            self.clear_widgets(children=self.walls)
            self.walls = []
        self.clear_widgets(children=[self.menu])
        self.time = 120
        self.player.reset()
        self.clock()


class Player(Widget):
    vector = Vector(0, 0)

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.controller = (Window.width * .09, Window.height * .16)
        self.touch = True
        self.pos = (Window.width * .5, Window.height * .5)

    def on_touch_move(self, touch):
        self.on_touch_down(touch)
        self.touch = False

    def on_touch_down(self, touch):
        self.vector = Vector(touch.x - self.controller[0], touch.y - self.controller[1]).normalize() * 5
        self.touch = False

    def on_touch_up(self, touch):
        self.touch = True

    def move(self):
        if self.touch:
            self.vector = self.vector * .95
        if Window.width - self.width >= self.x + self.vector[0] >= 0:
            self.x += self.vector[0]
        if Window.height - self.height >= self.y + self.vector[1] >= 0:
            self.y += self.vector[1]

    def reset(self):
        self.pos = (Window.width * .5, Window.height * .5)
        self.vector = Vector(0,0)
        self.touch = True

class Controls(Widget):
    pass


class Wall(Widget):
    def __init__(self, **kwargs):
        super(Wall, self).__init__(**kwargs)
        self.direction = randint(0, 3)
        self.vector = Vector(5, 0).rotate(self.direction * 90)

        if self.direction == 0 or self.direction == 2:
            self.size_hint = (randint(50, 100) / Window.width, randint(50, 300) / Window.height)
            self.y = randint(0, Window.height - self.height)
            if self.direction == 0:
                self.x = -self.width
            else:
                self.x = Window.width
        if self.direction == 1 or self.direction == 3:
            self.size_hint = (randint(50, 300) / Window.width, randint(50, 100) / Window.height)
            self.x = randint(0, Window.width - self.width)
            if self.direction == 1:
                self.y = -self.height
            else:
                self.y = Window.height

    def move(self):
        self.pos = self.vector + self.pos

    def __del__(self):
        self.canvas.clear()


class Menu(Widget):
    pass


class SpaceL(App):
    def build(self):
        self.load_kv('main.kv')
        self.game = Game()
        return self.game


if __name__ == '__main__':
    SpaceL().run()
