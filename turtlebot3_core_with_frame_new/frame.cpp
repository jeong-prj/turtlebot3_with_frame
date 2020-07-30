
#include "frame.h"

frameC::frameC(){

}
frameC::~frameC(){
    
}

void frameC::init(){
    DEBUG_SERIAL.begin(1000000);
    
    dxl_wb_.begin(DEVICE_NAME, BAUDRATE);
    dxl_wb_.ping(DXL_ID);

    dxl_wb_.jointMode(DXL_ID);
}

void frameC::goal(const std_msgs::UInt16& cmd_msg){
  dxl_wb_.goalPosition(DXL_ID, cmd_msg.data); //set servo angle, should be from 0-180 
 
}
