import kivy
kivy.require('1.5.1')

import random

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Line, Ellipse
from kivy.properties import NumericProperty


class DiceWidget(Widget):
    number = NumericProperty(0)

    def __init__(self, **kwargs):
        super(DiceWidget, self).__init__(**kwargs)
        self.bind(size=self.redraw)
        self.bind(pos=self.redraw)

        # Components drawn on the canvas
        self.outline = None
        self.dots = []

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


class DiceApp(App):
    def build(self):
        layout = BoxLayout(padding=10, orientation='vertical')
        dice_layout = BoxLayout(padding=20, spacing=20, orientation='horizontal')
        dice1 = DiceWidget()
        dice2 = DiceWidget()
        dice_layout.add_widget(dice1)
        dice_layout.add_widget(dice2)
        dice1.number = 0
        dice2.number = 0

        layout.add_widget(dice_layout)

        sum_label = Label(text="?", font_size='60sp')
        layout.add_widget(sum_label)

        roll = Button(text="Roll")

        def on_roll(instance):
            dice1.number = random.randrange(1, 7)
            dice2.number = random.randrange(1, 7)
            sum_label.text = str(dice1.number + dice2.number)

        roll.bind(on_press=on_roll)
        layout.add_widget(roll)

        return layout

if __name__ in ('__main__', '__android__'):
    DiceApp().run()
