"""


"""


# import sys
# import re
import sqlite3


RM = sqlite3.connect('robbie_memory.sqlite')
cursor = RM.cursor()

class QuestDef():
    def __init__(self):
        # list of parameters that robbie controll ie battery. location
        self.states = ('health', 'emotions', 'battery')  # robot states

    # answer the how for noun question
    def query(self, c):
        cursor.execute('''SELECT s FROM is_a WHERE o =?''', (c,))
        user = cursor.fetchone()
        # if user == 'None':
        #return user


        return "the " + str(c) + " is a "  + str(user)# returns robot states
