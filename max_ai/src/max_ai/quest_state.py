"""
this only works with nouns
company name and tickers are no supported yet

"""


import sys
import re

class QuestState():
    def __init__(self):
        # list of parameters that robbie controll ie battery. location
        self.states = ('health','emotions','battery')# robot states
        self.forex = ('euro', 'dollar', 'pound', 'aussie', 'peso')# currency
        self.stocks =('lynas','bhp')# company names are not nouns




    # answer the how for noun question
    def status(self, c):
        if c in self.states:
            return "the " + str(c) + " is at 13.8"# returns robot states
        elif c in self.forex:
            return "the " + str(c) + " is at 107.856"# returns forex values
        elif c == 'market':
            return "the market is down today"
        elif c == "cat":
            return "the cat is happy"
        elif c == "weather":
            return "the weather is fine"
        else:
            return "I have no knowledge of " + str(c)