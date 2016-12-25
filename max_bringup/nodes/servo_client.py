#!/usr/bin/env python

import sys
import rospy
from max_messages.srv import *

def move_servo_client(name, value):
    rospy.wait_for_service('/cmd_server')
    try:
        add_two_ints = rospy.ServiceProxy('/cmd_server', Cmd)
        add_two_ints(name, value)
        #return resp1
    except rospy.ServiceException, e:
        print "Service call failed   vv: %s"%e

def usage():
    return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 3:
        x = str(sys.argv[1])
        y = int(sys.argv[2])
        #a = int(sys.argv[3])
        #b = int(sys.argv[4])
    else:
        print usage()
        sys.exit(1)
    print "Requesting %s %s"%(x, y)
    move_servo_client(x, y)
