#include <DynamixelWorkbench.h>
#include <std_msgs/UInt16.h>

#if defined(__OPENCM904__)
  #define DEVICE_NAME "3" //Dynamixel on Serial3(USART3)  <-OpenCM 485EXP
#elif defined(__OPENCR__)
  #define DEVICE_NAME ""
#endif   

#define BAUDRATE  1000000
#define DXL_ID    3
#define DEBUG_SERIAL  SerialBT2

class frameC{
    public:
        frameC();
        ~frameC();
        
        void init();
        void goal(const std_msgs::UInt16& cmd_msg);
    private:
        DynamixelWorkbench dxl_wb_;
};
