#!/usr/bin/env python


from nlp import NlpClass
import sqlite3
import os
# import time
from datetime import datetime

dir = os.path.dirname(os.path.abspath(__file__))
RM = sqlite3.connect(dir + '/data/robbie_memory.db')


class TerminalInput:
    def __init__(self):
        a = NlpClass()
        debug = True
        print "ENTERING TERMINAL INPUT"
        while True:
            s = raw_input("Enter speech: ")
            a.nlpParse(s, debug)
            dt = datetime.now()
            #RM.execute("insert into RAW_INPUT (RAW, DATE) values (?, ?)",(s, dt))
            #RM.commit()
            # print sentenceAnalysisClass(s)
if __name__ == '__main__':
    st = TerminalInput()
