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

from max_ai.utilities import *
dir = os.path.dirname(os.path.abspath(__file__))
rm= Robbie_memory()#from utilities


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
        self.emotion_task = ""
        self.run_control = 'start'
        # The root node when all top levels tasks have SUCCESS: program exits
        BEHAVE = Sequence("behave")

        # Create the top level tasks in order.  Sequence executes each of its child behaviors until one of them fails
        
        FACIAL_GESTURES = Iterator("FACIAL_GESTURES")#start motions
        STAY_HEALTHY = Selector("STAY_HEALTHY")
        EMOTIONS = Iterator("EMOTIONS")
        START_UP = Iterator("START_UP")
        NAVIGATION = Iterator("NAVIGATION")
        CONVERSATION = Iterator("CONVERSATION")
        MOVEMENT = Iterator("MOVEMENT")
        FACE_RECOGNITION = Iterator("FACE_RECOGNITION")
        OBJECT_RECOGNITION = Iterator("OBJECT_RECOGNITION")
        
        # Add the two subtrees to the root node in order of priority
        BEHAVE.add_child(STAY_HEALTHY)
        BEHAVE.add_child(START_UP)
        BEHAVE.add_child(FACIAL_GESTURES)
        BEHAVE.add_child(EMOTIONS)
        BEHAVE.add_child(NAVIGATION)
        BEHAVE.add_child(CONVERSATION)
        BEHAVE.add_child(FACE_RECOGNITION)
        BEHAVE.add_child(MOVEMENT)
        BEHAVE.add_child(OBJECT_RECOGNITION)
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
            HAPPY = Sequence("HAPPY",[CHECK_HAPPY, HAPPY_FACE, STOP_START], reset_after=True)
            SAD = Sequence("SAD",[CHECK_SAD, SAD_FACE, STOP_START], reset_after=True)
            ANGRY = Sequence("ANGRY",[CHECK_ANGRY, ANGRY_FACE, STOP_START], reset_after=True)
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
            CHARGE_COMPLETE = ServiceTask("CHARGE_COMPLETE", "/battery_simulator/set_battery_level", SetBatteryLevel, 300, result_cb=self.recharge_cb)
            
            # Sleep for the given interval to simulate charging
            CHARGING = RechargeRobot("CHARGING", interval=3, blackboard=self.blackboard)
      
            # Build the recharge sequence using inline construction
            RECHARGE = Sequence("RECHARGE", [CHARGING, CHARGE_COMPLETE], reset_after=True)
                
            # Add the check battery and recharge tasks to the stay healthy selector
            STAY_HEALTHY.add_child(CHECK_BATTERY)
            STAY_HEALTHY.add_child(RECHARGE)

        with EMOTIONS:           
            STOP_EMOTIONS = CallbackTask("STOP_EMOTIONS", self.stop_emotions) #check for start message
            EMOTION_CB = Emotion1()
            CLOCK = Clock(60)#will check if greater than 60 secsince last activity
            CLOCK2 = Clock1(300)#will check if greater than 60 secsince last activity
            PRINT_MESSAGE2 = DisplayMessage("PRINT_MESSAGE2", "Starting emotions")
            EMOTION = Sequence("EMOTION",[CLOCK, CLOCK2], reset_after=True)

            EMOTIONS.add_child(EMOTION)

        with START_UP:
            INIT_CHECK = CallbackTask("INIT_CHECK", self.Run_Control)#start up tasks
            START_UP_TASKS = Sequence("START_UP_TASKS",[INIT_CHECK, START_FACE, STOP_START], reset_after=True)
            START_UP.add_child(START_UP_TASKS)
            
        with NAVIGATION:
            INIT_NAVIGATION = CallbackTask("INIT_NAVIGATION", self.check_navigation)#start up tasks
            NAVIGATION_TASKS = Sequence("NAVIGATION_TASKS",[INIT_NAVIGATION, START_FACE, STOP_START], reset_after=True)
            NAVIGATION.add_child(NAVIGATION_TASKS)
            
        with CONVERSATION:
            INIT_CONVERSATION = CallbackTask("INIT_CONVERSATION", self.check_concersion)#start up tasks
            CONVERSATION_TASKS = Sequence("CONVERSATION_TASKS",[INIT_CONVERSATION, START_FACE, STOP_START], reset_after=True)
            CONVERSATION.add_child(CONVERSATION_TASKS)
            
        with FACE_RECOGNITION:
            INIT_FACE_RECOGNITION = CallbackTask("INIT_FACE_RECOGNITION", self.check_face_recognition)#start up tasks
            FACE_RECOGNITION_TASKS = Sequence("FACE_RECOGNITION_TASKS",[INIT_FACE_RECOGNITION, START_FACE, STOP_START], reset_after=True)
            FACE_RECOGNITION.add_child(FACE_RECOGNITION_TASKS)
            
        with MOVEMENT:
            INIT_MOVEMENT = CallbackTask("INIT_MOVEMENT", self.check_movement)#start up tasks
            MOVEMENT_TASKS = Sequence("MOVEMENT_TASKS",[INIT_MOVEMENT, START_FACE, STOP_START], reset_after=True)
            MOVEMENT.add_child(MOVEMENT_TASKS)
            
        with OBJECT_RECOGNITION:
            INIT_OBJECT_RECOGNITION = CallbackTask("INIT_OBJECT_RECOGNITION", self.check_object_recognition)#start up tasks
            OBJECT_RECOGNITION_TASKS = Sequence("OBJECT_RECOGNITION_TASKS",[INIT_OBJECT_RECOGNITION, START_FACE, STOP_START], reset_after=True)
            OBJECT_RECOGNITION.add_child(OBJECT_RECOGNITION_TASKS)
            
        
     
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
            #rospy.loginfo("check stop: ")
            return TaskStatus.SUCCESS
        else:
            #rospy.loginfo("check start failed: ")
            return TaskStatus.FAILURE  

    def stop_emotions(self):
        if self.task == 'emotion':
            #rospy.loginfo("stop emotion: ")
            return TaskStatus.FAILURE
        else:
            #rospy.loginfo("check start failed: ")
            return TaskStatus.SUCCESS

    def Run_Control(self):
        if self.run_control == "start":
            #rospy.loginfo("RUN TIME FAILURE: ")
            return TaskStatus.SUCCESS
        else:
            #rospy.loginfo("RUN TIME SUCCESS: ")
            return TaskStatus.FAILURE            
 

    def stop_task(self):
        self.task = ''
        self.run_control = ''
        #rospy.loginfo("stop task: ")
        return TaskStatus.SUCCESS        

    def max_Cmd(self, req):
        self.task = str(req.name)
        #print "moving to " + self.task
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
    
    def check_navigation(self):
        if self.task == 'navigation':
            #rospy.loginfo("check navigation: ")
            return TaskStatus.SUCCESS
        else:
            #rospy.loginfo("check navigation failed: ")
            return TaskStatus.FAILURE  
	  
    def check_concersion(self):
        if self.task == 'concersion':
            #rospy.loginfo("check concersion: ")
            return TaskStatus.SUCCESS
        else:
            #rospy.loginfo("check concersion failed: ")
            return TaskStatus.FAILURE  
	  
    def check_face_recognition(self):
        if self.task == 'face_recognition':
            #rospy.loginfo("check face_recognition: ")
            return TaskStatus.SUCCESS
        else:
            #rospy.loginfo("check face_recognition failed: ")
            return TaskStatus.FAILURE  
	  
    def check_movement(self):
        if self.task == 'movement':
            #rospy.loginfo("check movement: ")
            return TaskStatus.SUCCESS
        else:
            #rospy.loginfo("check movement failed: ")
            return TaskStatus.FAILURE 
	  
    def check_object_recognition(self):
        if self.task == 'object_recognition':
            #rospy.loginfo("check object_recognition: ")
            return TaskStatus.SUCCESS
        else:
            #rospy.loginfo("check object_recognition failed: ")
            return TaskStatus.FAILURE  	  
	  
            
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
