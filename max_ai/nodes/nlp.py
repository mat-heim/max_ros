#!/usr/bin/env python

import sys
# import getopt
import re
# import subprocess
# import xml.etree.ElementTree as ET
# import csv
import random
from espeak import espeak
from subprocess import call

# import os

from pattern.en import parse
from pattern.en import pprint
from pattern.en import parsetree
from pattern.en import wordnet
from pattern.en import pluralize, singularize
from pattern.en import conjugate, lemma, lexeme

from max_ai.sa import sentenceAnalysisClass
from max_ai.cap import capabilitiesClass
from max_ai.mem_db import memoryClass
from max_ai.quest_state import QuestState
from max_ai.conf_state import ConfState
from max_ai.quest_def import QuestDef
from max_ai.look_up import LookUp

class NlpClass:
    def __init__(self):

        self.memory = memoryClass()  # memory of concepts
        self.cap = capabilitiesClass()
        self.quest_state = QuestState()
        self.conf_state = ConfState()
        self.quest_def = QuestDef()
        self.look_up = LookUp()
        # Add a concept 'I', defining robbie's identity
        self.memory.add('I')
        self.memory.concepts['I'].state = 'great'  # dynamically reflect Robbie's mood by telemetry
        self.memory.concepts['I'].person = '1sg'  # 2st person singular
        self.memory.concepts['I'].isProperNoun = True
        # Synonymes for certain response forms, to give some natural response
        # variations
        self.responseVariations = {"yes": ("Yes.",
                                           "Affirmative.",
                                           "Definitely.",
                                           "Sure.",
                                           "Absolutely."),
                                   "acknowledge": ("I see.",
                                                   "OK.",
                                                   "Acknowledged.",
                                                   "If you say so.",
                                                   "Copy that.",
                                                   "I'll remember that."),
                                   "gratitude": ("Thanks!",
                                                 "I appreciate that.",
                                                 "You are too kind.",
                                                 "Oh stop it."),
                                   "insulted": ("I'm sorry you feel that way.",
                                                "Well, you're not too hot either.",
                                                "Look who's talking.",
                                                "Can't we just be nice."),
                                   "gratitudeReply": ("You're very welcome!",
                                                      "Sure thing!",
                                                      "No worries!",
                                                      "Don't mention it!"),
                                   "bye": ("See you later.",
                                           "It was a pleasure.",
                                           "Bye bye."),
                                   "hi": ("Hi, how are you.",
                                          "Hey there.",
                                          "What's going on!"),
                                   "no": ("No.",
                                          "Negative.",
                                          "I don't think so.",
                                          "Definitely not.",
                                          "No way.",
                                          "Not really.")
                                   }

        self.positivePhrases = ['smart',
                                'impressive',
                                'cool']
        self.negativePhrases = ['stupid',
                                'annoying',
                                'boring']

        self.emotionMap = [['angry.',
                            'aggrevated',
                            'very excited',
                            'very happy'],
                           ['frustrated',
                            'stressed',
                            'excited',
                            'happy.'],
                           ['sad',
                            'doing OK',
                            'doing well',
                            'doing very well.'],
                           ['depressed',
                            'sleepy',
                            'bored',
                            'relaxed']]

    def randomizedResponseVariation(self, response):
        idx = random.randint(0, len(self.responseVariations[response]) - 1)
        return self.responseVariations[response][idx]

    def getPersonalProperty(self, sa):
        # Question refers back to Robbie's: how is 'your' X  
        print sa.getSentenceRole(sa.concept) in self.memory.concepts['I'].properties
        if sa.getSentenceRole(sa.concept) in self.memory.concepts['I'].properties:
            print self.memory.concepts['I'].properties[sa.getSentenceRole(sa.concept)][0]
            print self.memory.concepts['I'].properties[sa.getSentenceRole(sa.concept)][1]  # name is returned as none

            # self.response("say my " + self.memory.concepts['I'].properties[sa.getSentenceRole(sa.concept)][0] + " is " + self.memory.concepts['I'].properties[sa.getSentenceRole(sa.concept)][1])
            # else:
            # self.response("say I don't know what my " + sa.getSentenceRole(sa.concept) + " is ")

    def response(self, s):
        print'my responce is     :' + s
        espeak.synth(s)
        #espeak -v mb-en1 -p 40 -s140 (s)
        #call(["espeak","-v", "mb-en1",(s)])

    def nlpParse(self, line, debug=1):
        text = parsetree(line, relations=True, lemmata=True)
        for sentence in text:
            sa = sentenceAnalysisClass(sentence, debug)
            st = sa.sentenceType()

        print 'sentance type  ' + str(st)
        print 'concept: ' + sa.concept

        # Question state: 'how is X'
        if st == 'questionState':
            # print 'company name  ' +str(re.search('be (.+?)/NNP', str(text)).group(1))
            try:
                 noun = str(re.search('the (.+?)/NN', str(text)).group(1))# return noun
                 self.response(self.quest_state.status(noun))
            except:
                self.response("this dose not compute")

        # Confirm state: 'is X Y'
        elif st == 'confirmState':
            self.response(self.conf_state.conf('test'))

        # Question definition: 'what/who is X'
        elif st == 'questionDefinition':
            #print 'look of your'
            print sa.MyChunk()# this will return your
            if sa.MyChunk() is not "your":#  change and add try
                print 'your is'
            if sa.is2ndPersonalPronounPosessive('OBJ'):
                # Question refers back to Robbie's: what is 'your' X. Look up Robbie's's personal property
                # error if not in the database
                self.response('My ' + sa.getSentenceRole(sa.concept) + ' is ' + str(
                    self.memory.search_profile(sa.getSentenceRole(sa.concept))[0]))
            else:
                try:
                    noun = str(re.search('/a (.+?)/NN', str(text)).group(1))# return noun

                    print noun
                    self.response(self.quest_def.query(noun))
                except:
                    noun = str(re.search('/be (.+?)/NN', str(text)).group(1))# return noun

                    print noun
                    self.response(self.quest_def.query(noun))

                # except:
                    # self.response("this dose not compute")
                # move to quest lookup function

            #print 'definition role  ' + sa.getSentenceRole(sa.concept)

            # else:
            # Question about person, object or thing


        # State: 'X is Y'
        elif st == 'statement':
            if sa.is2ndPersonalPronounPosessive('SBJ'):
                # Refers back to robbie: 'your' X is Y 
                if sa.getSentenceRole(sa.concept) not in self.memory.concepts['I'].properties:
                    self.memory.concepts['I'].properties[sa.getSentenceRole(sa.concept)] = [
                        sa.getSentenceRole(sa.concept), sa.getSentencePhrase('OBJ')]
                self.response("say ok")
            else:
                if sa.getSentenceRole(sa.concept) == 'I':
                    # Statement about Robbie's, do not memorize this (Robbie's maintains its own state based on Robbie's telemetry
                    # but instead react to statement
                    print 'ww ' + sa.getSentenceRole('ADJP')
                    if sa.getSentenceRole('ADJP') in self.positivePhrases:
                        # Saying something nice will maximize happiness and arousal
                        # self.response("set mood 500 500 ")
                        self.response("say " + self.randomizedResponseVariation('gratitude'))
                    else:
                        # Saying something insulting will minimize happiness and increase arousal
                        # self.response("set mood -300 50 ")
                        self.response("say " + self.randomizedResponseVariation('insulted'))
                else:
                    if not self.memory.known(sa.getSentenceRole(sa.concept)):
                        self.memory.add(sa.getSentenceRole(sa.concept))
                    self.memory.concepts[sa.getSentenceRole(sa.concept)].state = sa.getSentencePhrase('ADJP')
                    self.response("say " + self.randomizedResponseVariation('acknowledge'))

                    # State locality: 'X is in Y'
        elif st == 'stateLocality':
            # print 'the concept is ' + sa.getSentenceRole(sa.concept)
            # check if we have this concept
            # print self.memory.known(sa.getSentenceRole(sa.concept))
            if not self.memory.known(sa.getSentenceRole(sa.concept)):
                self.memory.add_memory(sa.getSentenceRole(sa.concept), sa.getSentencePhrase('PNP'))  # Add the concept
                # self.memory.concepts[sa.getSentenceRole(sa.concept)].locality = sa.getSentencePhrase('PNP')#add locality?????????????
                # print 'the rest is ' + sa.getSentencePhrase('PNP')
                # self.memory.add_memory(sa.getSentenceRole(sa.concept),sa.getSentencePhrase('PNP'))
                self.response("I will remember that")
            else:
                self.memory.update_memory(sa.getSentenceRole(sa.concept), sa.getSentencePhrase('PNP'))
                self.response('I have updated my memory')


        # Question locality: 'Where is X'
        elif st == 'questionLocality':
            # print 'the concept is ' + sa.getSentenceRole(sa.concept)
            if not self.memory.known(sa.getSentenceRole(sa.concept)):
                # self.response("I dont know about that  " + sa.getSentenceRole(sa.concept))
                print 'look up result is   ' + str(self.look_up.query(sa.getSentenceRole(sa.concept),'where'))

            if self.memory.known(sa.getSentenceRole(sa.concept)):
                self.response(sa.getSentencePhrase(sa.concept) + ' ' + conjugate('be', self.memory.search_memory(
                    sa.getSentenceRole(sa.concept))[2]) + ' ' +
                              self.memory.search_memory(sa.getSentenceRole(sa.concept))[1])
                # print self.memory.search_memory(sa.getSentenceRole(sa.concept))[2]
                # self.response("mood 50 20")
                # print sa.getSentencePhrase(sa.concept)# the cat
                # print self.memory.concepts[sa.getSentenceRole(sa.concept)].person

                # Command
        elif st == 'command':
            if self.cap.capable(sa.getSentenceHead("VP")):
                # Command is a prefixed Robbie's command to be given through telemetry
                self.response("say " + self.randomizedResponseVariation('yes') + " I can")
                print 'cmd  ' + str(self.cap.constructCmd(sa))
                # for cmd in self.cap.constructCmd(sa):
                # self.response(cmd)

            else:
                # Not knowing stuff makes Robbie sad and a little aroused
                # self.response("mood -50 20")
                # self.response("facial " + str(EXPR_SHAKENO))
                # self.response("say " + self.randomizedResponseVariation('no'))
                self.response("say I'm afraid I can't do that. I don't know how to " + sa.getSentenceHead('VP'))

                # who is
        elif st == 'questionProperNoun':
            self.response(self.randomizedResponseVariation('hi'))

        elif st == 'greeting':
            self.response(self.randomizedResponseVariation('hi'))

        elif st == 'greeting':
            self.response(self.randomizedResponseVariation('hi'))

        elif st == 'bye':
            self.response(self.randomizedResponseVariation('bye'))

        elif st == 'gratitude':
            self.response("say " + self.randomizedResponseVariation('gratitudeReply'))

        elif st == 'adverbPhrase':
            if sa.getSentenceHead('ADJP') == 'further':
                for cmd in self.cap.lastCmd:
                    self.response(cmd)
        else:
            self.response("say sorry, I don't understand")
        self.cap.lastCmd = self.cap.constructCmd(sa)
