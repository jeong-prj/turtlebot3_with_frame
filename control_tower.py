#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import rospy
from std_msgs.msg import UInt16
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
from multi_robot.msg import aruco_msgs
import numpy as np
from rospy.numpy_msg import numpy_msg


class Control:
    def __init__(self):
        rospy.init_node("control_tower")
        
        self.mode_pub=rospy.Publisher('/mode_msg',Int32,queue_size=10) 
        self.mani_robot_stop_pub=rospy.Publisher('/mani_robot_stop',Int32,queue_size=10)#self_drive.py
        self.call_frame_pub=rospy.Publisher('/call_frame',Int32,queue_size=10) #call_robot2.py
        self.mani_move_pub =rospy.Publisher('/mani_move_msg',Int32,queue_size=10)
        self.frame_move_pub = rospy.Publisher('/control_frame', UInt16, queue_size=10)#frame_node.py send mode up or down 
        self.return_frame_pub=rospy.Publisher('/return_frame_msg',Int32,queue_size=10)#home.py
        
        self.mani_stop = Int32()
        self.frame_mode = Int32()
        self.mani_state = Int32()
        
        self.call = -1
        self.home = -1
        self.mani_mode = "Ready to Pick up box" 
        self.mode = 0
        
        #acuco
        self.aurco_move_pub =rospy.Publisher('/start_arco',Int32,queue_size=10)
        self.aruco_mode = -1
    def main(self):
          #모든 상태가 0일 때 mani_move동작
        while not rospy.is_shutdown():
            self.starting_trigger()
            ####메니 동작
            if self.mode == 0:               #mani만 움직이는 동안
                rospy.loginfo(self.mode)
                if self.aruco_mode == 1:  #aruco 발견시
                    self.mode = 1
                else:
                    self.mani_robot_stop_pub.publish(1) #mani robot 움직임

            
            elif self.mode == 1:             #아르코마커 발견시
                rospy.loginfo(self.mode)
                if self.aruco_move_mode == 0: #아르코(물체)에 접근 했을 때
                    self.mode = 2
                else:
                    self.mani_robot_stop_pub.publish(0) #mani robot 움직임 정지
                    self.aurco_move_pub.publish(1) #아르코(물체)에 접근 이동노드 on


            elif self.mode == 2: #물체에 접군 후
                rospy.loginfo(self.mode)
                self.aurco_move_pub.publish(0)#아르코(물체)에 접근 이동노드off
                if self.aruco_id == 1: #작은물체 인식 하면
                    self.mani_move_pub.publish(1) #mani 작은 동작 시작
                    self.mode = 3
                elif self.aruco_id == 2: #큰물체 인식 하면
                    self.mani_move_pub.publish(2) #mani 큰 동작 시작
                    self.mode = 4


            elif self.mode == 3: #작은 물제 집는동안
                rospy.loginfo(self.mode)
                if self.mani_mode == "Release small box":
                    self.mani_mode = "Ready to Pick up box"
                    self.mode = 0
            
            elif self.mode == 4: #큰 물체 잡는 동안
                rospy.loginfo(self.mode)
                if self.mani_mode == "Pick up large box": 
                    self.mani_mode = "Ready to Release large box"
                    self.call_frame_pub.publish(1)#call frame_robot to large box
                    self.frame_move_pub.publish(1) #frame up
                elif self.mani_mode == "Release large box":
                    self.mani_mode = "Ready to Pick up box"
                    self.return_frame_pub.publish(1)
                    self.mode = 0
            
            elif self.home == 1: #frame_robot reach to home
                self.frame_move_pub.publish(2) #frame down
            ###메니 동작 완료

            # else: #모든 상태가 0일 때 mani_move동작:
            #     self.mani_robot_stop_pub(1)

    def starting_trigger(self):
        rospy.Subscriber("/Mani_state", Int32, self.ManiCallback)
        rospy.Subscriber("/call_fin", Int32, self.CallCallback)        
        rospy.Subscriber("/home_fin", Int32, self.HomeCallback)
        rospy.Subscriber('/aruco_msg',Int32, self.aruco)
        rospy.Subscriber('/id_msg',Int32, self.aruco_id)
        rospy.Subscriber("/aruco_move", Int32, self.aruco_move) #aruco_move.py
        
    def aruco(self,msg):
        self.aruco_mode = msg.data
    def aruco_id(self,msg):
        self.aruco_id =msg.data
    def aruco_move(self,msg):
        self.aruco_move_mode = msg.data
         
    def ManiCallback(self, data):
        if self.mani_mode == "Ready to Pick up box"  and data.data == 1:
           self.mani_mode = "Release small box"
           print("Setting mode Release small box")
           
        elif self.mani_mode == "Ready to Pick up box"  and data.data == 2:
            self.mani_mode = "Pick up large box" 
            print("Setting Pick up large box")
            
        elif self.mani_mode == "Ready to Release large box" and data.data == 2 and self.call == 1:
            self.mani_mode = "Release large box"
            self.call = -1
            print("Setting mode Release large box")

    def CallCallback(self, data):
        self.call = data.data  
        
    def HomeCallback(self, data):
        self.home = data.data 
        
    def Delay(self, data):
        self.rate = rospy.Rate(data)
        self.rate.sleep()

        
def main():
   
    Turtle = Control()
    Turtle.main()

if __name__ == "__main__":
    main()
