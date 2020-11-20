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
        global scan_data
        scan_data = data.ranges

#init_pos service call
rospy.wait_for_service('init_pos', timeout=10)
init_pos = rospy.ServiceProxy('init_pos', InitPos)
init_pos(2, 0)

#publish to /move
mover = rospy.Publisher('/move', String)

#subscriber /scan topic
scan = rospy.Subscriber('/scan', LaserScan, callback, 0)

#subscriber to /robot_pos topic
pos = rospy.Subscriber('/robot_pos', Point, callback, 1)



rospy.init_node('planner', anonymous=True)

subscrate = rospy.Rate(1)

while not rospy.is_shutdown():
    subscrate.sleep()
    print(pos_data)
    if(scan_data[2]>1.0):
        mover.publish('N')
    elif(scan_data[3]>1.0):
        mover.publish('E')
    else:
        print('Goal reached')