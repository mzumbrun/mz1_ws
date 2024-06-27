#!/usr/bin/env python3
from typing import Any
import rclpy
from rclpy.node import Node
from functools import partial

from example_interfaces.srv import AddTwoInts
 
class AddTwoIntsClientNode(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("node_name") # MODIFY NAME
        self.call_add_two_ints_server(6,7)
        self.call_add_two_ints_server(1,7)
        self.call_add_two_ints_server(5,7)
        self.call_add_two_ints_server(7,7)
        self.call_add_two_ints_server(0,7)

    def call_add_two_ints_server(self, a, b):
        client = self.create_client(AddTwoInts, "add_two_ints")
        while not client.wait_for_service(1.0):
           self.get_logger().warn("waiting for server Add Two Ints ...")
    
        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        future = client.call_async(request) 
        future.add_done_callback(partial(self.callback_call_add_two_ints, a=a, b=b)) 

    def callback_call_add_two_ints(self, future, a, b):
        try:
            response = future.result()
            self.get_logger().info(str(a) + " + " + str(b) + " = " + str(response.sum)) 
        except Exception as e:
            self.get_logger().error("service call failed %r" % (e,) )


 
 
def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsClientNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()