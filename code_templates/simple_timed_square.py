#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
import time

state = 1
change_state = True
  
rclpy.init(args=None)
node = Node("square")

vel_pub = node.create_publisher(TwistStamped, "cmd_vel", 10)
vel = TwistStamped()
timestamp = node.get_clock().now().nanoseconds

while rclpy.ok():
    time_now = node.get_clock().now().nanoseconds
    elapsed_time = (time_now - timestamp) * 1e-9
    if change_state:
        timestamp = node.get_clock().now().nanoseconds
        change_state = False
        vel.twist.linear.x = 0.0
        vel.twist.angular.z = 0.0
        node.get_logger().info(f"Changing to state: {state}")
    elif state == 1:
        if elapsed_time > 2:
            state = 2
            change_state = True
        else:
            vel.twist.linear.x = 0.05
            vel.twist.angular.z = 0.0
    elif state == 2:
        if elapsed_time > 4:
            state = 1
            change_state = True
        else:
            vel.twist.angular.z = 0.2
            vel.twist.linear.x = 0.0

    node.get_logger().info(
        f"Publishing Velocities:\n"
        f"  linear.x: {vel.twist.linear.x:.2f} [m/s] | angular.z: {vel.twist.angular.z:.2f} [rad/s].",
        throttle_duration_sec=1,
    )
    vel_pub.publish(vel)
    
    try:
        rclpy.spin_once(node, timeout_sec=0.1)
        time.sleep(0.1) # 10Hz loop rate
    except KeyboardInterrupt:
        print("Keyboard Interrupt detected. Shutting down.")
        break

node.destroy_node()