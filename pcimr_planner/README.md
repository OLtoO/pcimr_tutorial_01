This package provides code to move a 2-D robot from its starting position to its goal.

A simple algorithm, only working for this problem, subscribes to the Robot Position and the robot scanner. It published to the topic /move to move the robot to the goal.

An instance of simple_sim_node in pcimr_simulation has to be running.
rosrun pcimr_planner nody.py starts the planner and moves the robot.
