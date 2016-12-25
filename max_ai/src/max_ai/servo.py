#!/usr/bin/env python
'''
from robbie_behave.task import *
AUTODOCK = AutoDock()
RECHARGE = Sequence("RECHARGE", [NAV_DOCK_TASK, AUTODOCK])
'''
import rospy
from pi_trees_ros.pi_trees_ros import *
from ros_arduino_msgs.srv import *
from max_messages.srv import *
from utilities import *
dir = os.path.dirname(os.path.abspath(__file__))
rm= Robbie_memory()#from utilities

class Happy(Task):
    def __init__(self, timer=2, *args):
        name = "HAPPY_"
        super(Happy, self).__init__(name)   
        self.finished = False
        self.counter = timer
        self.name = name
        self._eyes = rospy.ServiceProxy('/max_head/eyes', Eyes) 
        self._eye_brows = rospy.ServiceProxy('/max_head/eye_brow', EyeBrows)   
        self._ears = rospy.ServiceProxy('/max_head/ears', Ears) 
        self._mouth = rospy.ServiceProxy('/max_head/mouth', Mouth)   
        self._neck = rospy.ServiceProxy('/max_head/neck', Neck)       
    def run(self):
        try:
            rospy.loginfo('HAPPY START.')
            self._eyes(100, 60) 
            self._eye_brows(110, 70)  
            self._ears(30,160)
            self._mouth(110,60,110,60)
            self._neck(90,90)
            rm.E_Update(0.1,0.1)
            return TaskStatus.SUCCESS  
            message = "HAPPY FINISHED"
            rospy.loginfo(message)
            self.finished = True
        except rospy.ServiceException, e:
            print "Service call failed   vv: %s"%e
            return TaskStatus.FAILURE

class Angry(Task):
    def __init__(self, timer=2, *args):
        name = "ANGRY_"
        super(Angry, self).__init__(name)   
        self.finished = False
        self.counter = timer
        self.name = name
        self._eyes = rospy.ServiceProxy('/max_head/eyes', Eyes) 
        self._eye_brows = rospy.ServiceProxy('/max_head/eye_brow', EyeBrows)   
        self._ears = rospy.ServiceProxy('/max_head/ears', Ears) 
        self._mouth = rospy.ServiceProxy('/max_head/mouth', Mouth)   
        self._neck = rospy.ServiceProxy('/max_head/neck', Neck)       
    def run(self):
        try:
            rospy.loginfo('ANGRY START.')
            self._eyes(100, 60) 
            self._eye_brows(110, 70)  
            self._ears(30,160)
            self._mouth(90,90,90,80)
            self._neck(90,90)
            rm.E_Update(0.1,0.1)
            return TaskStatus.SUCCESS  
            message = "ANGRY FINISHED"
            rospy.loginfo(message)
            self.finished = True
        except rospy.ServiceException, e:
            print "Service call failed   vv: %s"%e
            return TaskStatus.FAILURE

class Sad(Task):
    def __init__(self, timer=2, *args):
        name = "SAD_"
        super(Sad, self).__init__(name)   
        self.finished = False
        self.counter = timer
        self.name = name
        self._eyes = rospy.ServiceProxy('/max_head/eyes', Eyes) 
        self._eye_brows = rospy.ServiceProxy('/max_head/eye_brow', EyeBrows)   
        self._ears = rospy.ServiceProxy('/max_head/ears', Ears) 
        self._mouth = rospy.ServiceProxy('/max_head/mouth', Mouth)   
        self._neck = rospy.ServiceProxy('/max_head/neck', Neck)       
    def run(self):
        try:
            rospy.loginfo('SAD START.')
            self._eyes(100, 60) 
            self._eye_brows(90, 90)  
            self._ears(90,90)
            self._mouth(60,110,60,110)
            self._neck(90,90)
            rm.E_Update(0.1,0.1)
            return TaskStatus.SUCCESS  
            message = "SAD FINISHED"
            rospy.loginfo(message)
            self.finished = True
        except rospy.ServiceException, e:
            print "Service call failed   vv: %s"%e
            return TaskStatus.FAILURE

class Stop(Task):
    def __init__(self, timer=2, *args):
        name = "STOP_"
        super(Stop, self).__init__(name)   
        self.finished = False
        self.counter = timer
        self.name = name
        self._eyes = rospy.ServiceProxy('/max_head/eyes', Eyes) 
        self._eye_brows = rospy.ServiceProxy('/max_head/eye_brow', EyeBrows)   
        self._ears = rospy.ServiceProxy('/max_head/ears', Ears) 
        self._mouth = rospy.ServiceProxy('/max_head/mouth', Mouth)   
        self._neck = rospy.ServiceProxy('/max_head/neck', Neck)  
        self._eyelight = rospy.ServiceProxy('/max_head/analog_write', AnalogWrite)     
    def run(self):
        try:
            rospy.loginfo('STOP START.')
            self._eyes(100, 60) 
            self._eye_brows(110, 70)  
            self._ears(90,90)
            self._mouth(90,90,90,80)
            self._neck(90,90)
            self._eyelight(39,0)
            rm.E_Update(0.1,0.1)
            return TaskStatus.SUCCESS  
            message = "STOP FINISHED"
            rospy.loginfo(message)
            self.finished = True
        except rospy.ServiceException, e:
            print "Service call failed   vv: %s"%e
            return TaskStatus.FAILURE

class Start(Task):
    def __init__(self, timer=2, *args):
        name = "START_"
        super(Start, self).__init__(name)   
        self.finished = False
        self.counter = timer
        self.name = name
        self._eyes = rospy.ServiceProxy('/max_head/eyes', Eyes) 
        self._eye_brows = rospy.ServiceProxy('/max_head/eye_brow', EyeBrows)   
        self._ears = rospy.ServiceProxy('/max_head/ears', Ears) 
        self._mouth = rospy.ServiceProxy('/max_head/mouth', Mouth)   
        self._neck = rospy.ServiceProxy('/max_head/neck', Neck)  
        self._eyelight = rospy.ServiceProxy('/max_head/analog_write', AnalogWrite)     
    def run(self):
        try:
            rospy.loginfo('START START.')
            self._eyes(100, 60) 
            self._eye_brows(110, 70)  
            self._ears(30,160)
            self._mouth(90,90,90,80)
            self._neck(90,90)
            self._eyelight(39,200)
            rm.E_Update(0.1,0.1)
            return TaskStatus.SUCCESS  
            message = "START FINISHED"
            rospy.loginfo(message)
            self.finished = True
        except rospy.ServiceException, e:
            print "Service call failed   vv: %s"%e
            return TaskStatus.FAILURE
