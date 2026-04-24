#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


# =========================================================
# STATES
# =========================================================
STATE_SCANNING = 0
STATE_PARKED = 1


class ParkingNode(Node):
    def __init__(self):
        super().__init__('parking_node')

        # Publisher
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        # Subscribers
        self.scan_sub = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10
        )

        self.odom_sub = self.create_subscription(
            Odometry,
            'odom',
            self.odom_callback,
            10
        )

        # Parameters
        self.FORWARD_SPEED = 0.10
        self.FRONT_STOP_DIST = 0.50

        # Target stop position between yellow dividers
        self.TARGET_X = 2.0

        # State
        self.state = STATE_SCANNING
        self.robot_x = 0.0
        self.slot_detected = False

        self.get_logger().info("====================================")
        self.get_logger().info("Autonomous Parking Node - STARTED")
        self.get_logger().info("Driving forward, scanning for parking slot...")
        self.get_logger().info("Using LiDAR + Odom for reliable parking")
        self.get_logger().info("====================================")

    # =========================================================
    # HELPERS
    # =========================================================

    def publish_cmd(self, linear, angular):
        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        self.cmd_pub.publish(msg)

    def deg_to_idx(self, ranges, degree):
        n = len(ranges)
        return int((degree % 360) * n / 360)

    def avg_range(self, ranges, center_idx, half_window):
        valid = []

        for i in range(
            max(0, center_idx - half_window),
            min(len(ranges), center_idx + half_window + 1)
        ):
            if not math.isinf(ranges[i]) and not math.isnan(ranges[i]):
                valid.append(ranges[i])

        if len(valid) == 0:
            return float('inf')

        return sum(valid) / len(valid)

    # =========================================================
    # ODOM CALLBACK
    # =========================================================

    def odom_callback(self, msg):
        self.robot_x = msg.pose.pose.position.x

    # =========================================================
    # LIDAR CALLBACK
    # =========================================================

    def scan_callback(self, msg):
        if self.state == STATE_PARKED:
            self.publish_cmd(0.0, 0.0)
            return

        ranges = msg.ranges

        # Front obstacle safety check
        front_idx = self.deg_to_idx(ranges, 90)
        front_dist = self.avg_range(ranges, front_idx, 20)

        # Right-side parking scan
        right_idx = self.deg_to_idx(ranges, 270)
        right_dist = self.avg_range(ranges, right_idx, 35)

        self.get_logger().info(
            f"Right distance = {right_dist:.2f}, X = {self.robot_x:.2f}"
        )

        # Safety stop if wall too close
        if front_dist < self.FRONT_STOP_DIST:
            self.get_logger().info("Front obstacle detected - stopping")
            self.publish_cmd(0.0, 0.0)
            return

        # LiDAR explanation part: detect open slot region
        if right_dist > 1.8 and not self.slot_detected:
            self.slot_detected = True
            self.get_logger().info(
                "Parking slot detected using LiDAR"
            )

        # Odom precision part: stop exactly between yellow dividers
        if self.slot_detected and self.robot_x >= self.TARGET_X:
            self.get_logger().info(
                "Reached target position between yellow dividers"
            )
            self.publish_cmd(0.0, 0.0)
            self.state = STATE_PARKED
            return

        # Continue moving forward
        self.publish_cmd(self.FORWARD_SPEED, 0.0)


# =========================================================
# MAIN
# =========================================================

def main(args=None):
    rclpy.init(args=args)

    node = ParkingNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info("Shutting down")

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
