#!/usr/bin/env python

import sys
import rospy
from max_messages.srv import *

def move_servo_client(x, y, a, b):
    rospy.wait_for_service('/max_head/mouth')
    try:
        add_two_ints = rospy.ServiceProxy('/max_head/mouth', Mouth)
        add_two_ints(x, y, a ,b)
        #return resp1
    except rospy.ServiceException, e:
        print "Service call failed   vv: %s"%e

def usage():
    return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 5:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
        a = int(sys.argv[3])
        b = int(sys.argv[4])
    else:
        print usage()
        sys.exit(1)
    print "Requesting %s %s"%(x, y)
    move_servo_client(x, y, a ,b)
