#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt16
from geometry_msgs.msg import Twist


class Control:
    def __init__(self):
        rospy.init_node("control", anonymous=True)
        self.servo_pub = rospy.Publisher('/servo', UInt16, queue_size=10)
	self.home_pub = rospy.Publisher('/home', UInt16, queue_size=10)
        self.serv = UInt16()
	self.home = UInt16()
        self.mode = "Ready to Raise up" #before raise up
        

    def main(self):
        print("starting,,,")
        while True:
            # 1. Program starting trigger subscribe
            self.starting_trigger()
            if self.mode == "Raise up": #When recieve the control msg: 1 by sender.py 
		        #Raise up the frame
                self.PickUp()
                print(self.mode)
                self.servo_pub.publish(self.serv)
                self.mode = "Ready to Put down"
                
            elif self.mode == "Put down": #When recieve the control msg: 2 by sender.py 
                #Put down the frame
                self.PickDown()
                print(self.mode)
                self.servo_pub.publish(self.serv)
		self.home_pub.publish(self.home)
                self.mode = "Ready to Raise up"
                    
    def starting_trigger(self):
        rospy.Subscriber("/control_frame", UInt16, self.StartingCallback)
       

    def StartingCallback(self, data):
        if self.mode == "Ready to Raise up" and data.data == 1:
            self.mode = "Raise up"
            print("setting mode Raise up")
        elif self.mode == "Ready to Put down" and data.data == 2:
            self.mode = "Put down"
            print("setting mode Put down")
        #else:
            #self.mode = "Ready"
            #print("{}".format(data.data))

    def Delay(self, data):
        self.rate = rospy.Rate(data)
        self.rate.sleep()

    def PickUp(self):
        self.Delay(3)
        self.serv.data = 2000
        self.Delay(3)

    def PickDown(self):
        self.Delay(3)
        self.serv.data = 0
        self.Delay(3)


Turtle = Control()

if __name__ == "__main__":
    Turtle.main()
