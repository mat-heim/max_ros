"""

"""


import sys
import re

class ConfState():
    def __init__(self):
        # list of parameters that robbie controll ie battery. location
        self.states = ('health','emotions','battery')# robot states
        self.forex = ('euro', 'dollar', 'pound', 'aussie', 'peso')# currency
        self.stocks =('lynas','bhp')# company names are not nouns




    # answer is x in y question
    def conf(self, c):

        return "the " + str(c) + " is  confirmed"# returns robot states