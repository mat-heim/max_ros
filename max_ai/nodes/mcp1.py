#!/usr/bin/env python
'''

'''
import rospy

from pi_trees_ros.pi_trees_ros import *
from std_msgs.msg import Float32, String, Int16
from max_messages.srv import *
from max_ai.mcp_tasks import *
import time



eye_request = EyesRequest() 
ears_request = EarsRequest() 
neck_request = NeckRequest()
brow_request = EyeBrowsRequest()
mouth_request = MouthRequest()     



class PhoenixControl():
    def __init__(self):
        rospy.init_node("Phoenix_Control")
       
        
       
        # The root node when all top levels tasks have SUCCESS: program exits
        BEHAVE = Sequence("behave")

        # Create the top level tasks in order.  Sequence executes each of its child behaviors until one of them fails
        
        START = Sequence("START")#start motions
        STOP = Sequence("STOP")#start motions
        '''


        '''
        

        # Add the subtrees to the root node in order of priority
        
        BEHAVE.add_child(START)
        #BEHAVE.add_child(STOP)
       
        # node to star the robot 
        with START:
            
            #eye pan and tilt value
            eye_request.a = 100
            eye_request.b = 60
            #eye brow value
            brow_request.a = 80
            brow_request.b = 80
            ears_request.a = 30
            ears_request.b = 160
            neck_request.a = 90
            neck_request.b = 80
            mouth_request.a = 90
            mouth_request.b = 90
            mouth_request.c = 90
            mouth_request.d = 80
            # reset the robot to the start configuration
            MOVE_EYES = ServiceTask("MOVE_EYES","max_head/eyes", Eyes,  eye_request)
            MOVE_EYEBROWS = ServiceTask("MOVE_EYEBROWS","max_head/eye_brow", EyeBrows,  brow_request)
            MOVE_EARS = ServiceTask("MOVE_EARS","max_head/ears", Ears, ears_request)
            MOVE_NECK = ServiceTask("MOVE_NECK","max_head/neck", Neck,  neck_request)
            MOVE_MOUTH = ServiceTask("MOVE_MOUTH","max_head/mouth", Mouth,  mouth_request)
            PRINT_MESSAGE = DisplayMessage("PRINT_MESSAGE", "Max is online")
            SCAN_TIMER = Timer(20) # 1 MINUTE TIMER

            START.add_child(MOVE_EYES)
            START.add_child(MOVE_EYEBROWS)
            START.add_child(MOVE_EARS)
            START.add_child(MOVE_NECK)
            START.add_child(MOVE_MOUTH)
            #START.add_child(PRINT_MESSAGE)
            #START.add_child(SCAN_TIMER)

        with STOP:
            
            #eye pan and tilt value
            eye_request.a = 100
            eye_request.b = 100
            #eye brow value
            brow_request.a = 80
            brow_request.b = 80
            ears_request.a = 90
            ears_request.b = 90
            neck_request.a = 90
            neck_request.b = 80
            mouth_request.a = 90
            mouth_request.b = 90
            mouth_request.c = 90
            mouth_request.d = 80
            # reset the robot to the start configuration
            MOVE_EYES = ServiceTask("MOVE_EYES","max_head/eyes", Eyes,  eye_request)
            MOVE_EYEBROWS = ServiceTask("MOVE_EYEBROWS","max_head/eye_brow", EyeBrows,  brow_request)
            MOVE_EARS = ServiceTask("MOVE_EARS","max_head/ears", Ears, ears_request)
            MOVE_NECK = ServiceTask("MOVE_NECK","max_head/neck", Neck,  neck_request)
            MOVE_MOUTH = ServiceTask("MOVE_MOUTH","max_head/mouth", Mouth,  mouth_request)
            # ADD SLEEP
            #ADD VOICE

            STOP.add_child(MOVE_EYES)
            STOP.add_child(MOVE_EYEBROWS)
            STOP.add_child(MOVE_EARS)
            STOP.add_child(MOVE_NECK)
            STOP.add_child(MOVE_MOUTH)
    
        print "Behavior Tree Structure"
        print_tree(BEHAVE)

        # Run the tree
        while not rospy.is_shutdown():
            BEHAVE.run()
            rospy.sleep(0.1)
            
       
   
            
    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        #self.move_base.cancel_all_goals()
        #self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)






         
            





if __name__ == '__main__':
    tree = PhoenixControl()
