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
        
        START = Sequence("START")#start motions
        '''


        '''
        

        # Add the subtrees to the root node in order of priority
        
        BEHAVE.add_child(START)
       
        # node to start the robot 
        with START:
            PRINT_MESSAGE = DisplayMessage("PRINT_MESSAGE", "Starting max")
            START_FACE = Start()
            CHECK_START = CallbackTask("CHECK_START", self.check_start) #MonitorTask("CHECK_START", "max_tasks", Float32, self.check_start)
            STOP_START = CallbackTask("STOP_START", self.stop_task)
            START1 = Sequence("START1",[CHECK_START, START_FACE, PRINT_MESSAGE, STOP_START], reset_after=True)


            START.add_child(START1)
            

      
     
        print "Behavior Tree Structure"
        print_tree(BEHAVE)

        # Run the tree
        while not rospy.is_shutdown():
            BEHAVE.run()
            rospy.sleep(0.1)
            
    def check_start(self):
        if self.task == 'start':
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
   
            
    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        #self.move_base.cancel_all_goals()
        #self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)




         
            





if __name__ == '__main__':
    tree = PhoenixControl()
