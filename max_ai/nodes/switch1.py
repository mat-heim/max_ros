#!/usr/bin/env python
'''
rostopic pub -1 /max_tasks std_msgs/Float32 -- 1


'''
import rospy

from pi_trees_ros.pi_trees_ros import *
from std_msgs.msg import Float32, String, Int16
from max_messages.srv import *
from max_ai.mcp_tasks import *
from max_ai.servo import *
import time



        



class PhoenixControl():
    def __init__(self):
        rospy.init_node("Phoenix_Control")
       
        rospy.Service('cmd_server', Cmd, self.max_Cmd)
        self.task = ""
        # The root node when all top levels tasks have SUCCESS: program exits
        BEHAVE = Sequence("behave")

        # Create the top level tasks in order.  Sequence executes each of its child behaviors until one of them fails
        
        #START = Sequence("START")#start motions
        FACIAL_GESTURES = Iterator("FACIAL_GESTURES")
        STAY_HEALTHY = Selector("STAY_HEALTHY")
        # Add the subtrees to the root node in order of priority
        BEHAVE.add_child(STAY_HEALTHY)
        #BEHAVE.add_child(START)
        BEHAVE.add_child(FACIAL_GESTURES)
        
       
        # tasks 
        
        PRINT_MESSAGE = DisplayMessage("PRINT_MESSAGE", "Starting max")
        CHECK_START = CallbackTask("CHECK_START", self.check_start) #check for start message
        CHECK_HAPPY = CallbackTask("CHECK_HAPPY", self.check_happy) #check for HAPPY message
        CHECK_ANGRY = CallbackTask("CHECK_ANGRY", self.check_angry) #check for start message
        CHECK_SAD = CallbackTask("CHECK_SAD", self.check_sad) #check for start message
        CHECK_STOP = CallbackTask("CHECK_STOP", self.check_stop) #check for start message
        STOP_START = CallbackTask("STOP_START", self.stop_task)
        #START1 = Sequence("START1",[CHECK_START, PRINT_MESSAGE, STOP_START], reset_after=True)
        # Is the fake battery level below threshold?
        CHECK_BATTERY = CallbackTask("BATTERY_OK?", self.check_battery) 
        #face functions
        START_FACE = Start()
        HAPPY_FACE = Happy()
        ANGRY_FACE = Angry()
        SAD_FACE = Sad()
        STOP_FACE = Stop()
        # face sequences
        START = Sequence("START",[CHECK_START, START_FACE,PRINT_MESSAGE,STOP_START], reset_after=True)
        HAPPY = Sequence("HAPPY",[CHECK_HAPPY, HAPPY_FACE,STOP_START], reset_after=True)
        SAD = Sequence("SAD",[CHECK_SAD, SAD_FACE,STOP_START], reset_after=True)
        ANGRY = Sequence("ANGRY",[CHECK_ANGRY, ANGRY_FACE,STOP_START], reset_after=True)
        STOP = Sequence("STOP",[CHECK_STOP, STOP_FACE,STOP_START], reset_after=True)

        # Is the fake battery level below threshold?
        CHECK_BATTERY = CallbackTask("BATTERY_OK?", self.check_battery) 

        #Add the tasks to the sequence
        # Add the check battery and recharge tasks to the stay healthy selector
        STAY_HEALTHY.add_child(CHECK_BATTERY)
        FACIAL_GESTURES.add_child(START)
        FACIAL_GESTURES.add_child(HAPPY)
        FACIAL_GESTURES.add_child(SAD)
        FACIAL_GESTURES.add_child(ANGRY)
        FACIAL_GESTURES.add_child(STOP)           

      
     
        print "Behavior Tree Structure"
        print_tree(BEHAVE)

        # Run the tree
        while not rospy.is_shutdown():
            BEHAVE.run()
            rospy.sleep(0.1)
            
    def check_start(self):
        if self.task == 'start':
            rospy.loginfo("check start: ")
            return TaskStatus.SUCCESS
        else:
            #rospy.loginfo("check start failed: ")
            return TaskStatus.FAILURE  

    def check_happy(self):
        if self.task == 'happy':
            #rospy.loginfo("check start: ")
            return TaskStatus.SUCCESS
        else:
            #rospy.loginfo("check start failed: ")
            return TaskStatus.FAILURE  

    def check_sad(self):
        if self.task == 'sad':
            #rospy.loginfo("check start: ")
            return TaskStatus.SUCCESS
        else:
            #rospy.loginfo("check start failed: ")
            return TaskStatus.FAILURE  

    def check_angry(self):
        if self.task == 'angry':
            #rospy.loginfo("check start: ")
            return TaskStatus.SUCCESS
        else:
            #rospy.loginfo("check start failed: ")
            return TaskStatus.FAILURE  

    def check_stop(self):
        if self.task == 'stop':
            #rospy.loginfo("check start: ")
            return TaskStatus.SUCCESS
        else:
            #rospy.loginfo("check start failed: ")
            return TaskStatus.FAILURE  

    def stop_task(self):
        self.task = ''
        rospy.loginfo("stop task: ")
        return TaskStatus.SUCCESS        

    def max_Cmd(self, req):
        self.task = str(req.name)
        print "moving to " + self.task
        return CmdResponse() 

    def check_battery(self):
        # Don't run the check if we are charging
        x = 13
        if x < 14:
            return True
        else:
            return False   
   
            
    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        #self.move_base.cancel_all_goals()
        #self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)




         
            





if __name__ == '__main__':
    tree = PhoenixControl()
