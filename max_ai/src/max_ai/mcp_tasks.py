#!/usr/bin/env python

import rospy
import re
import time
#import pywapi
import sys
import time
import tf
import math
from datetime import datetime, timedelta
from time import localtime, strftime
from std_msgs.msg import String
from actionlib import SimpleActionClient

from actionlib_msgs.msg import *
#from geometry_msgs.msg import *
from sound_play.libsoundplay import SoundClient
from datetime import datetime, timedelta
from pi_trees_ros.pi_trees_ros import *
from utilities import *
import markovian
dir = os.path.dirname(os.path.abspath(__file__))


# A class to track global variables
class BlackBoard():
    def __init__(self):
        
        # A list to store rooms and tasks
        self.task_list = list()
        self.emotion = 0.1,0.5
        self.Last_Event = time.time()#clock 
        self.Last_Event1 = time.time()# cloclk 1
        self.run_demo = False
        self.neutral = 0,0
        self.vigilant = 0,1
        self.happy = 1,0
        self.sad = -1,0
        self.bored = 0,-1
        self.excited = 0.5,0.5
        self.angry = -0.5,0.5
        self.relaxed = 0.5,-0.5
        self.depressed = -0.5,-0.5

# Initialize the black board
black_board = BlackBoard()
rm= Robbie_memory()#from utilities
file_ = open(dir + '/data/suntzu.txt')
markov = markovian.Markov(file_)



class SpeakMessage():# NOT a bt task will talk any message
    def __init__(self, message, timer= 2, *args, **kwargs):
        self.message = message
        self.voice = "voice_en1_mbrola"
        self.timer = timer
        # Create the sound client object
        #self.soundhandle = SoundClient()
        # sound_play server
        rospy.sleep(2)
        # Make sure any lingering sound_play processes are stopped.
        #self.soundhandle.stopAll()
        #self.soundhandle.say(self.message, self.voice)
        rospy.sleep(self.timer)


class DisplayMessage(Task):
    def __init__(self, name, message):
        super(DisplayMessage, self).__init__(name)
        
        self.name = name
        self.message = message
 
    def run(self):
        if self.status != TaskStatus.SUCCESS:
            rospy.loginfo(self.message)
            #SpeakMessage(self.message , 3)
            self.status = TaskStatus.SUCCESS
                
        return self.status
    
    def reset(self):
        self.status = None

class Timer(Task):
    def __init__(self, timer, *args):
        name = "Timer"
        super(Timer, self).__init__(name)
        self.name = name
        self.counter = timer
        self.finished = False
        #print timer

    def run(self):
        rospy.sleep(self.counter)
        return TaskStatus.SUCCESS
        

class Timer1(Task):
    def __init__(self, timer, *args):
        name = "Timer1"
        super(Timer1, self).__init__(name)
        self.name = name
        self.counter = timer
        self.finished = False
        #print timer

    def run(self):
        if black_board.Last_Event1 + self.counter < time.time():
            #print black_board.Last_Event + self.counter
            #print time.time()
            print "timer1 finished  " + str(self.counter)
            #rm.E_Update(-0.5,-0.5)
            black_board.Last_Event1 = time.time()
            return TaskStatus.SUCCESS
        else:
            #print 'fail'+ str(black_board.Last_Event)
            return TaskStatus.FAILURE

class Timer3(Task):
    def __init__(self, timer=60, *args):
        name = "TIMER3_" + str(timer)
        super(Timer3, self).__init__(name)    
        self.name = name
        
        self.counter = timer
        self.finished = False
        
    def run(self):
        if self.finished:
            return TaskStatus.SUCCESS
            print "timer 3  finished  " + str(self.counter)
        else:
            
            while self.counter > 0:
                
                #rospy.loginfo(self.counter)
                self.counter -= 1
                rospy.sleep(1)
                return TaskStatus.RUNNING
            
            self.finished = True

class Emotion1(Task):
    def __init__(self, timer=1, *args):
        name = "Emotion1"
        super(Emotion1, self).__init__(name)
        # Set the default TTS voice to use
        self.voice = rospy.get_param("~voice", "voice_en1_mbrola")
        self.robot = rospy.get_param("~robot", "robbie")
        # Create the sound client object
        #self.soundhandle = SoundClient()
        # Wait a moment to let the client connect to the
        # sound_play server
        rospy.sleep(1)
        
        # Make sure any lingering sound_play processes are stopped.
        #self.soundhandle.stopAll()
        


    def run(self):
        self.emotion_state = rm.Emotion_State()
        if self.emotion_state == 'bored':
            print "I'm feeling  bored "
            #print 'i have to do somthing '
            #SpeakMessage(markov.generate_markov_text(), 3)
            rm.E_Update(1,1.5)#us random selected task
        if self.emotion_state == 'neutral':
            print "I'm feeling netural   "
            #self.soundhandle.say( "I'm feeling netural   ", self.voice)
        if self.emotion_state == 'vigilant':
            print "I'm vigilant"
        if self.emotion_state == 'happy':
            print "I'm happy"
            print markov.generate_markov_text()
            rm.E_Update(0.1,0.1)
        if self.emotion_state == 'sad':
            print "I'm very sad"
            print "i want to smash something"
            rm.E_Update(0.7,0.6)
        if self.emotion_state == 'excited':
            print "I'm excited"
        if self.emotion_state == 'vigilant':
            print "I'm vigilant"
        if self.emotion_state == 'angry':
            print "I'm angry"   
        if self.emotion_state == 'relaxed':
            print "I'm relaxed"
        if self.emotion_state == 'depressed':
            print "I'm depressed"
            print rm.MeEmotion_read()
            #SpeakMessage(markov.generate_markov_text())
            #print markov.generate_markov_text()
            rm.E_Update(2,2)#us random selected task
            
            return TaskStatus.FAILURE
        else:
            return TaskStatus.SUCCESS

class CheckVariable(Task):
    def __init__(self, name, message, *args, **kwargs):
        super(CheckVariable, self).__init__(name, *args, **kwargs)
        self.words = message      
    def run(self):
        x = rm.MeMemory_read()
        if x[self.words] > 0:
            #print x[self.words]
            return TaskStatus.SUCCESS
        else:
            #print 'failed'
            return TaskStatus.FAILURE

class SetVariable(Task):
    def __init__(self, name, message, val, *args, **kwargs):
        super(SetVariable, self).__init__(name, *args, **kwargs)
        self.words = message 
        self.val = val     
    def run(self):
        x = rm.MeMemory_read()
        x[self.words]=self.val
        #print x
        rm.MeMemory_write(x)
        return TaskStatus.SUCCESS

#this will block until complete
class Clock(Task):
    def __init__(self, timer=60, *args):
        name = "Clock"
        super(Clock, self).__init__(name)
        self.name = name
        self.counter = timer
        self.finished = False

    def run(self):
        if black_board.Last_Event + self.counter < time.time():
            print black_board.Last_Event -time.time()
            #print time.time()
            print "clock 0 finished"+ str(rm.MeEmotion_read())
            rm.E_Update(-0.1,-0.1)
            black_board.Last_Event = time.time()
            return TaskStatus.FAILURE
        else:
            return TaskStatus.SUCCESS

class Clock1(Task):
    def __init__(self, timer=60, *args):
        name = "Clock1"
        super(Clock1, self).__init__(name)
        self.name = name
        self.counter = timer
        self.finished = False

    def run(self):
        if black_board.Last_Event1 + self.counter < time.time():
            print black_board.Last_Event1 -time.time()
            #print time.time()
            print "clock 1 finished"+ str(rm.MeEmotion_read())
            rm.E_Update(-0.5,-0.5)
            black_board.Last_Event1 = time.time()
            return TaskStatus.FAILURE
        else:
            return TaskStatus.SUCCESS
       
