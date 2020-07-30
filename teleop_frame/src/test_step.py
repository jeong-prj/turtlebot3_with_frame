#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt16


class Control:
    def __init__(self):
        rospy.init_node("control_step", anonymous=True)
        self.servo_pub = rospy.Publisher('/servo', UInt16, queue_size = 10)
        self.trigger = 'c'
        self.serv = UInt16()
        
    def Delay(self, data):
        self.rate = rospy.Rate(data)
        self.rate.sleep()

    def TriggerCallback(self, data):
        self.trigger = data.trigger
        
    def main(self):
        self.Delay(20)
        while True:
            self.trigger = raw_input('a, b, c :')
            print(self.trigger)
            if self.trigger == 'a':
                print("1")
                self.PickUp()
                
            elif self.trigger == 'b':
                print("-1")
                self.PickDown()
                
            elif self.trigger == 'c':
                self.Stop()
            
        
    def PickUp(self):
        self.serv.data = 120
        self.servo_pub.publish(self.serv)
        self.Delay(2.3)
        self.trigger = 'c'

    def PickDown(self):
        self.serv.data = 50
        self.servo_pub.publish(self.serv)
        self.Delay(2.8)
        self.trigger = 'c'
        
    def Stop(self):
        self.serv.data = 80
        self.servo_pub.publish(self.serv)
        
Turtle = Control()

if __name__ == "__main__":
    Turtle.main()
