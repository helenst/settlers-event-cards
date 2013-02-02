settlers-dice-cards
===================

Settlers of Catan Event Cards replacement app written in Kivy

Background
----------

This is meant for use with the Settlers of Catan board game, which by default uses two dice to determine what happens on each round - the game is supposed to be balanced around statistical distribution of dice rolls but over the course of a game there are not nearly enough rolls to bring out that distribution, resulting in a lot of tears and tantrums. You may like that kind of thing, but for those preferring a more civilised game there was also a deck of cards which you could buy separately and use instead of dice to ensure a statistically perfect distribution, reducing the game's randomness and placing greater emphasis on strategy. It doesn't seem to be possible to buy the cards any more, hence the app.

(see http://boardgamegeek.com/boardgame/20038/catan-event-cards for more about the Event Cards)

There is also a web-based version of the same thing on Game Pixies (http://gamepixies.com/settlers/) - written by @dgym


Kivy
----

Kivy is a Python-based app development toolkit which supports Android, iOS and also desktop platforms for ease of development. I first heard of it at PyConUK 2012 and was interested to give it a try. (I've so far only run the app on my Linux desktop and within the Android launcher - it hasn't been packaged up yet)

http://kivy.org/


Features
--------
* Hit the button to roll a pair of "dice"
* Sound effects for dice roll
* Accelerometer integration - roll on shake

TODO
----
* Settings screen (disable sound / accelerometer)
* Improve graphics - anti-aliasing and rounded corners would be nice
