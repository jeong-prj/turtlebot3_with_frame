cmake_minimum_required(VERSION 2.8.3)
project(control_frame_teleop)

add_compile_options(-std=c++11)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  geometry_msgs
  std_msgs
  message_generation
)



set(CMAKE_CXX_FLAGS "-L/usr/local/lib -pthread")


add_message_files(
  FILES
  TriggerMsg.msg
 )

generate_messages(
   DEPENDENCIES
   std_msgs
 )


catkin_package(
  INCLUDE_DIRS
  LIBRARIES teleop_servo1
  CATKIN_DEPENDS roscpp std_msgs geometry_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)


add_executable(trigger_pub_with_various_angle /home/eoj/catkin_ws/src/teleop_frame/src/trigger_pub_with_various_angle.cpp)
target_link_libraries(trigger_pub_with_various_angle ${catkin_LIBRARIES})
add_dependencies(trigger_pub_with_various_angle ${mode_second}_EXPORTED_TARGETS ${catkin_EXPORTED_TARGETS})

