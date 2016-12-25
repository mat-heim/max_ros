#!/usr/bin/env python
'''
rostopic pub -1 /max_tasks std_msgs/Float32 -- 1


'''
import rospy

from pi_trees_ros.pi_trees_ros import *
from std_msgs.msg import Float32, String, Int16
from max_messages.srv import *
from ros_arduino_msgs.srv import *
from max_ai.mcp_tasks import *
from max_ai.servo import *
import time



        



class PhoenixControl():
    def __init__(self):
        rospy.init_node("Phoenix_Control")
       
        
       
        # The root node when all top levels tasks have SUCCESS: program exits
        BEHAVE = Sequence("behave")
        FACIAL_GESTURES = Iterator("FACIAL_GESTURES")
        BEHAVE.add_child(FACIAL_GESTURES)

        CHECK_START = MonitorTask("CHECK_START", "max_tasks", Float32, self.check_start)
        CHECK_HAPPY = MonitorTask("CHECK_HAPPY", "max_tasks", Float32, self.check_happy)
        CHECK_SAD = MonitorTask("CHECK_SAD", "max_tasks", Float32, self.check_sad)
        CHECK_ANGRY = MonitorTask("CHECK_ANGRY", "max_tasks", Float32, self.check_angry)
        PRINT_MESSAGE = DisplayMessage("PRINT_MESSAGE", "Starting max")
        CHECK_STOP = MonitorTask("CHECK_STOP", "max_tasks", Float32, self.check_stop)
        PRINT_MESSAGE1 = DisplayMessage("PRINT_MESSAGE1", "Stopping Max")
        START_FACE = Start()
        HAPPY_FACE = Happy()
        ANGRY_FACE = Angry()
        SAD_FACE = Sad()
        STOP_FACE = Stop()
        START = Sequence("START",[CHECK_START, START_FACE, PRINT_MESSAGE], reset_after=True)
        HAPPY = Sequence("HAPPY",[CHECK_HAPPY, HAPPY_FACE], reset_after=True)
        SAD = Sequence("SAD",[CHECK_SAD, SAD_FACE], reset_after=True)
        ANGRY = Sequence("ANGRY",[CHECK_ANGRY, ANGRY_FACE], reset_after=True)
        STOP = Sequence("STOP",[CHECK_STOP, STOP_FACE, PRINT_MESSAGE1], reset_after=True)
        
        # Create the top level tasks in order.  Sequence executes each of its child behaviors until one of them fails
        
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
            
    def check_start(self, msg):
        if msg.data is None:
            rospy.loginfo("check start: " + str(int(msg.data)))
            return TaskStatus.RUNNING
        else:
            if msg.data == 1:
                #rospy.loginfo("start start: " + str(int(msg.data)))              
                return TaskStatus.SUCCESS
            else:
                #rospy.loginfo("start fail: " + str(int(msg.data))) 
                return TaskStatus.FAILURE  

    def check_happy(self, msg):
        if msg.data is None:
            rospy.loginfo("check happy: " + str(int(msg.data)))
            return TaskStatus.RUNNING
        else:
            if msg.data == 2:
                #rospy.loginfo("happy happy: " + str(int(msg.data)))              
                return TaskStatus.SUCCESS
            else:
                #rospy.loginfo("happy fail: " + str(int(msg.data))) 
                return TaskStatus.FAILURE 

    def check_sad(self, msg):
        if msg.data is None:
            #rospy.loginfo("check sad: " + str(int(msg.data)))
            return TaskStatus.RUNNING
        else:
            if msg.data == 3:
                #rospy.loginfo("sad sad: " + str(int(msg.data)))              
                return TaskStatus.SUCCESS
            else:
                #rospy.loginfo("sad fail: " + str(int(msg.data))) 
                return TaskStatus.FAILURE   

    def check_angry(self, msg):
        if msg.data is None:
            #rospy.loginfo("check angry: " + str(int(msg.data)))
            return TaskStatus.RUNNING
        else:
            if msg.data == 4:
                #rospy.loginfo("angry angry: " + str(int(msg.data)))              
                return TaskStatus.SUCCESS
            else:
                #rospy.loginfo("angry fail: " + str(int(msg.data))) 
                return TaskStatus.FAILURE   
   

    def check_stop(self, msg):
        if msg.data is None:
            #rospy.loginfo("check null: " + str(int(msg.data)))
            return TaskStatus.RUNNING
        else:
            if msg.data == 9:
                #rospy.loginfo("start stop: " + str(int(msg.data)))              
                return TaskStatus.SUCCESS
            else:
                #rospy.loginfo("stop fail: " + str(int(msg.data))) 
                return TaskStatus.FAILURE    
   
            
    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        #self.move_base.cancel_all_goals()
        #self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)






         
            





if __name__ == '__main__':
    tree = PhoenixControl()
