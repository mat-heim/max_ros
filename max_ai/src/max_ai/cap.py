# Robbie's capabilites class
# This class contains information about what commands we can give the Robbie's
# hardware through the telemetry command interface. If the NLP module detects
# the voice audio is a command, we convert is into an actual
# Robbie's robot command

import sys
import re
import time

from pattern.en import parse
from pattern.en import pprint
from pattern.en import parsetree
from pattern.en import wordnet
from pattern.en import pluralize, singularize
from pattern.en import conjugate, lemma, lexeme


class capabilitiesClass:
    def __init__(self):
        # List of verbs that are translated into Robbie's robot commands
        self.lastCmd = ()
        self.c = ('turn',
                  'go',
                  'give'
                  'get'
                  'look',
                  'analyze',
                  'find',
                  'come',
                  'speak',
                  'move',
                  'grab',
                  'drop')

    # Return True if verb is in Robbie's capabilities list
    def capable(self, s):
        return s in self.c

    # Construct an actual Robbie's command list from a sentence Analysis class instance
    # The commands in this list can be passed diretly to the Robbie's telementry fifo
    def constructCmd(self, sa):
        if sa.getSentenceHead('VP') == 'turn':
            if sa.getFirstWord('CD') != None:
                return ['turn to ' + sa.getFirstWord('CD').string]
            elif sa.getSentenceChunk('ADJP') != None:
                if sa.getSentenceChunk('ADJP').string == 'right':
                    return ['turn 0 1000000']
                elif sa.getSentenceChunk('ADJP').string == 'left':
                    return ['turn 1 1000000']
        elif sa.getSentenceHead('VP') == 'go':
            return ['obj go']
        elif sa.getSentenceHead('VP') == 'give':
            return ['obj give']
        elif sa.getSentenceHead('VP') == 'get':
            return ['obj get']
        elif sa.getSentenceHead('VP') == 'look':
            return ['orient fwd']
        elif sa.getSentenceHead('VP') == 'analyze':
            return ['obj analyze']
        elif sa.getSentenceHead('VP') == 'find':
            return ['obj find']
        elif sa.getSentenceHead('VP') == 'grab':
            return ['obj pickup']
        elif sa.getSentenceHead('VP') == 'get':
            return ['obj get']
        elif sa.getSentenceHead('VP') == 'drop':
            return ['obj drop']
        elif sa.getSentenceHead('VP') == 'come':
            return ['set track 1',  # Enable object tracking
                    'set state 2']  # Change Robbie's state from RC to Orientation
        elif sa.getSentenceHead('VP') == 'move':
            if sa.getSentenceChunk('ADVP') != None:
                if sa.getSentenceChunk('ADVP').string == 'forward':
                    return ['move 1 1000000']
                elif sa.getSentenceChunk('ADVP').string == 'back':
                    return ['move 2 1000000']
                else:
                    return "Sorry, I don't understand"
        elif sa.getSentenceHead('VP') == 'speak':
            if sa.getSentenceRole('ADVP') == 'louder':
                return ['set volume 20',
                        'say is this better?']
            elif sa.getSentenceRole('ADVP') == 'quietly':
                return ['set volume -20',
                        'say is this better?']
            else:
                return "Sorry, I don't understand"
        else:
            return "say I don't know that command"
