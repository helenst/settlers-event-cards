import kivy
kivy.require('1.5.1')

import random
import itertools
from functools import partial

from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.widget import Widget

# Not used in here directly but import is needed for .kv file
from dice import DiceWidget
from shake import ShakeDetector


class DiceScreen(Widget):

    def __init__(self, **kwargs):
        super(DiceScreen, self).__init__(**kwargs)
        self.cards = []
        self.rolling = False
        self.roll_sound = None
        self.play_sounds = False
        self.shake_to_roll = False

        self.shake_detector = ShakeDetector(on_shake=self.roll_dice)
        self.roll_sound = SoundLoader.load('diceroll.wav')

    def configure(self, config):
        self.play_sounds = config.getint('sound', 'effects') == 1
        self.shake_to_roll = config.getint('accelerometer', 'shake') == 1

        # Enable / disable the shake detector
        if self.shake_to_roll:
            self.shake_detector.enable()
        else:
            self.shake_detector.disable()

    def renew_cards(self):
        self.cards = list(itertools.product(range(1, 7), range(1, 7)))
        random.shuffle(self.cards)

    def next_card(self):
        if not self.cards:
            self.renew_cards()
        return self.cards.pop()

    def roll_dice(self):

        def animate_roll(n, *args):
            if n > 0:
                self.dice1.number = random.randrange(1, 7)
                self.dice2.number = random.randrange(1, 7)
                Clock.schedule_once(partial(animate_roll, n - 1), 0.05)
            else:
                self.dice1.number, self.dice2.number = self.next_card()
                self.sum_label.text = str(self.dice1.number + self.dice2.number)
                self.rolling = False

        if not self.rolling:
            self.rolling = True
            self.sum_label.text = '?'
            Clock.schedule_once(partial(animate_roll, 20), 0.05)

            if self.play_sounds:
                if self.roll_sound.state == 'play':
                    self.roll_sound.stop()
                self.roll_sound.play()


class DiceApp(App):
    def build(self):
        self.screen = DiceScreen()
        self.screen.configure(self.config)

        return self.screen

    def build_config(self, config):
        config.setdefaults('sound', {
            'effects': 1
        })
        config.setdefaults('accelerometer', {
            'shake': 1
        })

    def build_settings(self, settings):
        settings.add_json_panel('Dice', self.config, 'settings.json')

    def on_config_change(self, config, section, key, value):
        self.screen.configure(config)

    def on_pause(self):
        # Allow switching away from app
        return True


if __name__ in ('__main__', '__android__'):
    DiceApp().run()
