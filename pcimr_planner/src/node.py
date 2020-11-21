#!/usr/bin/env python
import sys
import rospy
import roslib
import numpy as np

from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Point
from pcimr_simulation.srv import InitPos

scan_data=2
pos_data=2

def callback(data, call):
    #Scanner
    if (call):
        global pos_data
        pos_data = [data.x,data.y]

    #Position
    else:
        global sc_data
        sc_data = data.ranges

#init_pos service call

def pos_init():
    rospy.wait_for_service('init_pos')
    try:
        init_pos_srv = rospy.ServiceProxy('init_pos', InitPos)
        resp = init_pos_srv(2, 0)
        if resp:
            print(f"Position initialized to 2, 0")
        else:
            print("Position initialization service returned False.")
    except Exception as e:
        print(f"Couldn't initialize position. Reason {e}")

#pos_init()

#publish to /move
mover = rospy.Publisher('/move', String, queue_size=10)

#subscriber /scan topic
scan = rospy.Subscriber('/scan', LaserScan, callback, 0)

#subscriber to /robot_pos topic
pos = rospy.Subscriber('/robot_pos', Point, callback, 1)



rospy.init_node('planner', anonymous=True)
pos_init()
subscrate = rospy.Rate(1)

#first option: move North
#second option: move East
while not rospy.is_shutdown():
    subscrate.sleep()
    print(pos_data)
    if(sc_data[2]>1.0):
        mover.publish('N')
    elif(sc_data[3]>1.0):
        mover.publish('E')
    else:
        print('Goal reached')