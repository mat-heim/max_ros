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
       
        
       
        # The root node when all top levels tasks have SUCCESS: program exits
        BEHAVE = Sequence("behave")

        # Create the top level tasks in order.  Sequence executes each of its child behaviors until one of them fails
        
        START = Sequence("START")#start motions
        STOP = Sequence("STOP")#stop motions
        '''


        '''
        

        # Add the subtrees to the root node in order of priority
        
        BEHAVE.add_child(START)
        BEHAVE.add_child(STOP)
       
        # node to startthe robot 
        with START:
            CHECK_START = MonitorTask("CHECK_START", "max_tasks", Float32, self.check_start)
            PRINT_MESSAGE = DisplayMessage("PRINT_MESSAGE", "Starting max")
            START_TASKS = Sequence("START_TASKS",[CHECK_START, PRINT_MESSAGE], reset_after=True)
            START.add_child(START_TASKS)
            #START.add_child(PRINT_MESSAGE)

        with STOP:
            CHECK_STOP = MonitorTask("CHECK_STOP", "max_tasks", Float32, self.check_stop)
            PRINT_MESSAGE1 = DisplayMessage("PRINT_MESSAGE1", "Stopping Max")
            STOP_TASKS = Sequence("STOP_TASKS",[CHECK_STOP, PRINT_MESSAGE1], reset_after=True)

            STOP.add_child(STOP_TASKS)
            #STOP.add_child(PRINT_MESSAGE1)            

      
     
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
                rospy.loginfo("start start: " + str(int(msg.data)))              
                return TaskStatus.SUCCESS
            else:
                rospy.loginfo("start fail: " + str(int(msg.data))) 
                return TaskStatus.FAILURE   

    def check_stop(self, msg):
        if msg.data is None:
            rospy.loginfo("check null: " + str(int(msg.data)))
            return TaskStatus.RUNNING
        else:
            if msg.data == 2:
                rospy.loginfo("start stop: " + str(int(msg.data)))              
                return TaskStatus.SUCCESS
            else:
                rospy.loginfo("stop fail: " + str(int(msg.data))) 
                return TaskStatus.FAILURE    
   
            
    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        #self.move_base.cancel_all_goals()
        #self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)






         
            





if __name__ == '__main__':
    tree = PhoenixControl()
