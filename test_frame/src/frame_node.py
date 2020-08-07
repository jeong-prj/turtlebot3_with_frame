#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt32
from std_msgs.msg import UInt16


class Frame:
    def __init__(self):
        rospy.init_node("frame_state", anonymous=True)
        self.servo_pub = rospy.Publisher('/servo', UInt16, queue_size=10)
        self.serv = UInt16()
        self.mode = "Ready to Raise up" #before raise up
        

    def main(self):
        print("starting,,,")
        while True:
            # 1. Program starting trigger subscribe
            self.frame_trigger()
            if self.mode == "Raise up": #When recieve the control msg: 1 by sender.py 
		        #Raise up the frame
                self.PickUp()
                self.servo_pub.publish(self.serv)
                self.mode = "Ready to Put down"
                ROS_INFO(self.mode)
                
            elif self.mode == "Put down": #When recieve the control msg: 2 by sender.py 
                #Put down the frame
                self.PickDown()
                self.servo_pub.publish(self.serv)
                #self.home_pub.publish(self.home)
                self.mode = "Ready to Raise up"
                ROS_INFO(self.mode)
                    
    def frame_trigger(self):
        #get mode from control_tower
        rospy.Subscriber("/control_frame", UInt32, self.FrameCallback)
       

    def FrameCallback(self, data):
        if self.mode == "Ready to Raise up" and data.data == 1:
            self.mode = "Raise up"
            print("setting mode Raise up")
        elif self.mode == "Ready to Put down" and data.data == 2:
            self.mode = "Put down"
            ROS_INFO("setting mode Put down")

    def Delay(self, data):
        self.rate = rospy.Rate(data)
        self.rate.sleep()

    def PickUp(self):
        ROS_INFO(self.mode)
        self.Delay(3)
        self.serv.data = 2000
        self.Delay(3)

    def PickDown(self):
        ROS_INFO(self.mode)
        self.Delay(3)
        self.serv.data = 0
        self.Delay(3)


Turtle = Frame()

if __name__ == "__main__":
    Turtle.main()
    
    
    
