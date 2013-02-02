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


class DiceScreen(Widget):

    def __init__(self, play_sounds, **kwargs):
        super(DiceScreen, self).__init__(**kwargs)
        self.cards = []
        self.roll_sound = SoundLoader.load('diceroll.wav')
        self.rolling = False
        self.play_sounds = play_sounds

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
        play_sounds = self.config.getint('sound', 'effects') == '1'
        self.shake_to_roll = self.config.getint('accelerometer', 'shake') == '1'
        self.screen = DiceScreen(play_sounds)

        import shake
        self.detector = shake.ShakeDetector()

        def on_shake(how_hard):
            if self.shake_to_roll:
                self.screen.roll_dice()
        self.detector.on_shake(on_shake)

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
        name = (section, key)
        if name == ('sound', 'effects'):
            self.screen.play_sounds = (value == '1')
        elif name == ('accelerometer', 'shake'):
            self.shake_to_roll = (value == '1')


if __name__ in ('__main__', '__android__'):
    DiceApp().run()
