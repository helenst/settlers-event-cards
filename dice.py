import kivy
kivy.require('1.5.1')

import random
import itertools

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line, Ellipse
from kivy.properties import NumericProperty


class DiceWidget(Widget):
    number = NumericProperty(0)

    def __init__(self, **kwargs):
        super(DiceWidget, self).__init__(**kwargs)

        self.bind(size=self.redraw, pos=self.redraw)

        # Components drawn on the canvas
        self.outline = None
        self.dots = []
        self.number = 0

        self.redraw()

    def redraw(self, *args, **kwargs):
        self.update_dots()
        self.canvas.clear()
        for dot in self.dots:
            self.canvas.add(self.outline)
            self.canvas.add(dot)

    def on_number(self, instance, number):
        self.update_dots()
        self.redraw()

    def update_dots(self):

        # Size of the die face
        dim = min(self.width, self.height)

        line_x = self.center_x - dim / 2
        line_y = self.center_y - dim / 2
        self.outline = Line(rectangle=(line_x, line_y, dim, dim))

        # Dots are drawn on a grid dividing the die face into 16 squares
        # and starting from the bottom left. Define coords for each.
        #  _______
        # |_|_|_|_|
        # |_|_|_|_|
        # |_|_|_|_|
        # |_|_|_|_|
        #

        # Locations of dots for each face
        dotmap = {
            0: (),
            1: ((2, 2),),
            2: ((1, 1), (3, 3)),
            3: ((1, 1), (2, 2), (3, 3)),
            4: ((1, 1), (1, 3), (3, 3), (3, 1)),
            5: ((1, 1), (1, 3), (2, 2), (3, 3), (3, 1)),
            6: ((1, 1), (1, 2), (1, 3), (3, 1), (3, 2), (3, 3))
        }

        # Size of a dot
        w = dim / 5
        h = dim / 5

        # Size of a grid unit
        unit = dim / 4

        # Define the dots
        self.dots = []
        for x, y in dotmap[self.number]:
            self.dots.append(Ellipse(
                pos=(line_x + (x * unit) - w / 2,
                     line_y + (y * unit) - h / 2),
                size=(w, h)))


class DiceScreen(Widget):

    def __init__(self, **kwargs):
        super(DiceScreen, self).__init__(**kwargs)
        self.cards = []

    def renew_cards(self):
        self.cards = list(itertools.product(range(1, 7), range(1, 7)))
        random.shuffle(self.cards)

    def next_card(self):
        if not self.cards:
            self.renew_cards()
        return self.cards.pop()

    def roll_dice(self):
        self.dice1.number, self.dice2.number = self.next_card()
        self.sum_label.text = str(self.dice1.number + self.dice2.number)


class DiceApp(App):
    def build(self):
        return DiceScreen()


if __name__ in ('__main__', '__android__'):
    DiceApp().run()
