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
from rbx2_msgs.srv import *
import time


class BlackBoard():
    def __init__(self):
        self.battery_level = None
        self.charging = None

        



class PhoenixControl():
    def __init__(self):
        rospy.init_node("Phoenix_Control")

        # Initialize the black board
        self.blackboard = BlackBoard()

        # Set the low battery threshold (between 0 and 100)
        self.low_battery_threshold = rospy.get_param('~low_battery_threshold', 50)  
   
        rospy.Service('cmd_server', Cmd, self.max_Cmd)
        self.task = ""
        # The root node when all top levels tasks have SUCCESS: program exits
        BEHAVE = Sequence("behave")

        # Create the top level tasks in order.  Sequence executes each of its child behaviors until one of them fails
        
        FACIAL_GESTURES = Iterator("FACIAL_GESTURES")#start motions
        # Create the "stay healthy" selector
        STAY_HEALTHY = Selector("STAY_HEALTHY")
        # Add the two subtrees to the root node in order of priority
        BEHAVE.add_child(STAY_HEALTHY)
        BEHAVE.add_child(FACIAL_GESTURES)
       
        # node to start the robot 
        with FACIAL_GESTURES:
            PRINT_MESSAGE = DisplayMessage("PRINT_MESSAGE", "Starting max")
            START_FACE = Start()
            HAPPY_FACE = Happy()
            ANGRY_FACE = Angry()
            SAD_FACE = Sad()
            STOP_FACE = Stop()
            CHECK_START = CallbackTask("CHECK_START", self.check_start) 
            CHECK_HAPPY = CallbackTask("CHECK_HAPPY",self.check_happy)
            CHECK_SAD = CallbackTask("CHECK_SAD", self.check_sad)
            CHECK_ANGRY = CallbackTask("CHECK_ANGRY", self.check_angry)
            CHECK_STOP = CallbackTask("CHECK_STOP", self.check_stop) #check for start message
            STOP_START = CallbackTask("STOP_START", self.stop_task)
            START = Sequence("START",[CHECK_START, START_FACE, PRINT_MESSAGE, STOP_START], reset_after=True)
            HAPPY = Sequence("HAPPY",[CHECK_HAPPY, HAPPY_FACE], reset_after=True)
            SAD = Sequence("SAD",[CHECK_SAD, SAD_FACE], reset_after=True)
            ANGRY = Sequence("ANGRY",[CHECK_ANGRY, ANGRY_FACE], reset_after=True)
            STOP = Sequence("STOP",[CHECK_STOP, STOP_FACE, STOP_START], reset_after=True)


            FACIAL_GESTURES.add_child(START)
            FACIAL_GESTURES.add_child(HAPPY)
            FACIAL_GESTURES.add_child(SAD)
            FACIAL_GESTURES.add_child(ANGRY)
            FACIAL_GESTURES.add_child(STOP)

        # Add the battery check and recharge tasks to the "stay healthy" task
        with STAY_HEALTHY:
            # Monitor the fake battery level by subscribing to the /battery_level topic
            MONITOR_BATTERY = MonitorTask("MONITOR_BATTERY", "battery_level", Float32, self.monitor_battery)
            
            # Is the fake battery level below threshold?
            CHECK_BATTERY = CallbackTask("BATTERY_OK?", self.check_battery)  
            
            # Set the fake battery level back to 100 using a ServiceTask
            CHARGE_COMPLETE = ServiceTask("CHARGE_COMPLETE", "/battery_simulator/set_battery_level", SetBatteryLevel, 100, result_cb=self.recharge_cb)
            
            # Sleep for the given interval to simulate charging
            CHARGING = RechargeRobot("CHARGING", interval=3, blackboard=self.blackboard)
      
            # Build the recharge sequence using inline construction
            RECHARGE = Sequence("RECHARGE", [CHARGING, CHARGE_COMPLETE], reset_after=True)
                
            # Add the check battery and recharge tasks to the stay healthy selector
            STAY_HEALTHY.add_child(CHECK_BATTERY)
            STAY_HEALTHY.add_child(RECHARGE)
            

      
     
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
            rospy.loginfo("check stop: ")
            return TaskStatus.SUCCESS
        else:
            #rospy.loginfo("check start failed: ")
            return TaskStatus.FAILURE  

    def stop_task(self):
        self.task = ''
        rospy.loginfo("reset var: ")
        return TaskStatus.SUCCESS        
 

    def stop_task(self):
        self.task = ''
        rospy.loginfo("stop task: ")
        return TaskStatus.SUCCESS        

    def max_Cmd(self, req):
        self.task = str(req.name)
        print "moving to " + self.task
        return CmdResponse()   

    def monitor_battery(self, msg):
        # Store the battery level as published on the fake battery level topic
        self.blackboard.battery_level = msg.data
        return True
    
    def check_battery(self):
        # Don't run the check if we are charging
        if self.blackboard.charging:
            return False
        
        if self.blackboard.battery_level is None:
            return None
        elif self.blackboard.battery_level < self.low_battery_threshold:
            rospy.loginfo("LOW BATTERY - level: " + str(int(self.blackboard.battery_level)))
            return False
        else:
            return True
    def recharge_cb(self, result):
        rospy.loginfo("BATTERY CHARGED!")
        self.blackboard.battery_level = 100
        self.blackboard.charging = False
        rospy.sleep(2)
        return True  
            
    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        #self.move_base.cancel_all_goals()
        #self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)




         
class RechargeRobot(Task):
    def __init__(self, name, interval=3, blackboard=None):
        super(RechargeRobot, self).__init__(name)
       
        self.name = name
        self.interval = interval
        self.blackboard = blackboard
        
        self.timer = 0
         
    def run(self):
        if self.timer == 0:
            rospy.loginfo("CHARGING THE ROBOT!")
            
        if self.timer < self.interval:
            self.timer += 0.1
            rospy.sleep(0.1)
            self.blackboard.charging = True
            return TaskStatus.RUNNING
        else:
            return TaskStatus.SUCCESS
    
    def reset(self):
        self.status = None
        self.timer = 0            





if __name__ == '__main__':
    tree = PhoenixControl()
