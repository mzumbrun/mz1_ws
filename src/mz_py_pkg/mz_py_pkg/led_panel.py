#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from my_robot_interfaces.msg import LedStateArray
from my_robot_interfaces.srv import SetLed

 
 
class LedPanelNode(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("led_panel") # MODIFY NAME
        self.led_states_publisher_=self.create_publisher(LedStateArray, "led_states", 10)
        self.led_status_=[0, 1, 0]
        self.led_states_timer_=self.create_timer(4, self.publish_led_states)
        self.set_led_service_= self.create_service(SetLed, "set_led", self.callback_set_led)
        self.get_logger().info("led panel node started")

    def callback_set_led(self, request, response):
        led_number = request.led_number
        state = request.state

        if led_number > len(self.led_status_) or led_number <=0:
            response.success = False
            self.get_logger().error("WRONG NUMBER")
            return response
        
        if state not in [0,1]:
            response.success = False
            return response
        
        self.led_status_[led_number-1] = state
        response.success = True
        self.publish_led_states()
        return response

     
    def publish_led_states(self):
        msg = LedStateArray()
        msg.led_states = self.led_status_
        self.led_states_publisher_.publish(msg)
 
def main(args=None):
    rclpy.init(args=args)
    node = LedPanelNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()