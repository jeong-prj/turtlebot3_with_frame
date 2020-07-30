#include "ros/ros.h"
#include <stdio.h>
#include "std_msgs/UInt16.h"
#include <termios.h>  
#include <unistd.h>  

int getch(void)  
{  
  int ch = '\n';  
  struct termios buf;  
  struct termios save;  
  
   tcgetattr(0, &save);  
   buf = save;  
   buf.c_lflag &= ~(ICANON|ECHO);  
   buf.c_cc[VMIN] = 1;  
   buf.c_cc[VTIME] = 0;  
   tcsetattr(0, TCSAFLUSH, &buf);  
   ch = getchar();  
   tcsetattr(0, TCSAFLUSH, &save);  
   return ch;  
}  

int main(int argc, char **argv)
{
  ros::init(argc, argv, "trigger_pub");
  ros::NodeHandle nh1;
  ros::Publisher signal_pub = nh1.advertise<std_msgs::UInt16>("/servo",10);
  ros::Rate loop_rate(10);
  std_msgs::UInt16 msg;

  int ch;

  while(ros::ok())
  {
    ros::spinOnce();
    
    for(; !(ch=='\n');){  
  
        ch = getch();  
        printf("%d \n", ch);
        break;  
    }
    switch(ch)
      {// 4000 / 360 = 11.11,, this is 1 do value	
       // 0 - 4000 range
	case 'z':	
	  msg.data = 0;// down no minus    0
	  ROS_INFO("k");
	  break;

	case 'x':		
	  msg.data = 333;// down no minus 30
	  ROS_INFO("k");
	  break;

	case 'c':		
	  msg.data = 500;// down no minus 45
	  ROS_INFO("k");
	  break;

	case 'v':		
	  msg.data = 666;// down no minus 60
	  ROS_INFO("k");
	  break;
	
	case 'a':		
	  msg.data = 1000;// up           90
	  ROS_INFO("k");
	  break;

	case 's':		
	  msg.data = 2000;// up           180
	  ROS_INFO("k");
	  break;

	case 'd':		
	  msg.data = 4000;// up           360
	  ROS_INFO("k");
	  break;
       }

    signal_pub.publish(msg);
    printf("send program start trigger = %d\n", msg.data);
    }
}
