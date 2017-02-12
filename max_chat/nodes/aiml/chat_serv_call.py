#! /usr/bin/env python
'''
<star/> is not working here
from chat_serv_call import Knowledge
>>> kn = Knowledge()
>>> kn.Grade('left', 'turn')


'''

import rospy
import sys
import rospy
from max_messages.srv import *


class Knowledge:
    """ 
    a class to python to return knowledge
    """
    def __init__(self):
        rospy.wait_for_service('/cmd_server')
        self.send_cmd = rospy.ServiceProxy('/cmd_server', Cmd)

    def Grade(self, name, value):
        self.send_cmd(name, value)
        return "ok"


       

