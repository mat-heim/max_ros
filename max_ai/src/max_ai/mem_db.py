#!/usr/bin/python

'''
memory class 
stored in sqlite data base
holds raw input and memories in parse taged columns

'''

import sys
import re
import sqlite3
import os

from datetime import date, datetime
from pattern.en import parse
from pattern.en import pprint
from pattern.en import parsetree
from pattern.en import wordnet
from pattern.en import pluralize, singularize
from pattern.en import conjugate, lemma, lexeme
#dir = os.path.dirname(os.path.abspath(__file__))
dir = '/home/erni/catkin_ws/src/max_ros/max_ai/src/max_ai/'
RM = sqlite3.connect(dir +'robbie_memory.sqlite')
#RM = sqlite3.connect(dir + '/data/robbie_memory.db')
cursor = RM.cursor()


# Information about a single concept
class conceptClass:
    def __init__(self, state='none', locality='none'):
        self.state = state  # what/how is 'concept'
        self.reference = 'none'  # unused
        self.locality = locality  # where is 'concept'
        self.person = '3sg'  # e.g. a thing is 3rd-person, singular
        self.isProperNoun = False  # True if proper noun: e.g. Robert
        self.properties = {}  # Dict of custom properties, e.g. 'age' = 39, 'color' = 'blue'


# Robbie memory class. Collection of concepts
class memoryClass():
    def __init__(self):
        self.concepts = {}
        self.person = {'I': '1sg',
                       'you': '2sg'
                       }
        self.posessivePronouns = {'1sg': 'my',
                                  '2sg': 'your',
                                  '3sg': 'its'
                                  }

    # Add a concept to memory
    def add(self, c):
        # add oncept to raw_input table in robbie_memory
        # x=
        # dt = datetime.now()
        # RM.execute("insert into RAW_INPUT (RAW, DATE) values (?, ?)",(c, dt))
        # RM.commit()

        self.concepts[c] = conceptClass()
        if c in self.person:
            self.concepts[c].person = self.person[c]

        else:
            self.concepts[c].person = '3sg'

    # Return True if concept 'c' (string) is in memory
    def known(self, c):
        cursor.execute('''SELECT concept, location FROM memory WHERE concept =?''', (c,))
        user = cursor.fetchone()
        # if user == 'None':
        return user

    def add_memory(self, a, b):
        c = '3sg'
        dt = datetime.now()
        RM.execute("insert into memory (concept, location, person,DATE) values (?, ?, ?, ?)", (a, b, c, dt))
        RM.commit()

    def update_memory(self, a, b):
        cursor.execute('''UPDATE memory SET location  = ? WHERE concept = ? ''', (b, a))
        RM.commit()

    def search_memory(self, a):
        cursor.execute('''SELECT concept,location, person FROM memory WHERE concept =?''', (a,))
        user = cursor.fetchone()
        return user

    def search_profile(self, a):
        cursor.execute('''SELECT value FROM profile WHERE item =?''', (a,))
        user = cursor.fetchone()
        return user

    def Dump(self):
        return (self.concepts.state)
