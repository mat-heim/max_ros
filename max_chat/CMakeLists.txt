cmake_minimum_required(VERSION 2.8.3)
project(max_chat)


find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
)

catkin_python_setup()

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES robbie_ai
#  CATKIN_DEPENDS roscpp rospy std_msgs
#  DEPENDS system_lib
)


