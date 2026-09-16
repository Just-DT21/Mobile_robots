#!/usr/bin/env python3
import csv
import math
import os
import time

import rclpy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from rclpy.node import Node


def clamp(value, low, high):
    return max(low, min(high, value))


def normalize_angle(angle):
    while angle > math.pi:
        angle -= 2.0 * math.pi
    while angle < -math.pi:
        angle += 2.0 * math.pi
    return angle


class PIDWaypointController(Node):
    def __init__(self):
        super().__init__("pid_waypoint_controller")

        self.cmd_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.pose_sub = self.create_subscription(
            Pose, "/turtle1/pose", self.pose_callback, 10
        )

        # Waypoints are inside the ideal 11 x 11 turtlesim workspace.
        self.waypoints = [
            (8.0, 8.0),
            (8.0, 3.0),
            (3.0, 3.0),
            (3.0, 8.0),
            (5.5, 5.5),
        ]
        self.wp_index = 0

        # Tuned for smooth ideal-condition waypoint tracking.
        self.kp_distance = 1.8
        self.ki_distance = 0.015
        self.kd_distance = 0.25

        self.kp_heading = 6.0
        self.ki_heading = 0.01
        self.kd_heading = 0.35

        self.distance_integral = 0.0
        self.heading_integral = 0.0
        self.previous_distance_error = 0.0
        self.previous_heading_error = 0.0
        self.last_time = self.get_clock().now()

        self.pose = None
        self.started = time.time()
        self.history = []

        self.output_dir = os.path.expanduser("~/mobile_robot_lab_ex6_results")
        os.makedirs(self.output_dir, exist_ok=True)

        self.timer = self.create_timer(0.05, self.control_loop)
        self.get_logger().info(
            "Experiment 6 started: PID waypoint tracking with distance threshold ed < 0.10"
        )

    def pose_callback(self, msg):
        self.pose = msg

    def control_loop(self):
        if self.pose is None or self.wp_index >= len(self.waypoints):
            if self.wp_index >= len(self.waypoints):
                self.finish()
            return

        now = self.get_clock().now()
        dt = max((now - self.last_time).nanoseconds / 1e9, 1e-3)
        self.last_time = now

        x, y, theta = self.pose.x, self.pose.y, self.pose.theta
        gx, gy = self.waypoints[self.wp_index]

        distance_error = math.hypot(gx - x, gy - y)
        desired_heading = math.atan2(gy - y, gx - x)
        heading_error = normalize_angle(desired_heading - theta)

        self.distance_integral = clamp(
            self.distance_integral + distance_error * dt, -2.0, 2.0
        )
        self.heading_integral = clamp(
            self.heading_integral + heading_error * dt, -1.0, 1.0
        )

        d_distance = (distance_error - self.previous_distance_error) / dt
        d_heading = (heading_error - self.previous_heading_error) / dt

        linear = (
            self.kp_distance * distance_error
            + self.ki_distance * self.distance_integral
            + self.kd_distance * d_distance
        )
        angular = (
            self.kp_heading * heading_error
            + self.ki_heading * self.heading_integral
            + self.kd_heading * d_heading
        )

        # Reduce forward motion while turning, producing a clean path.
        linear *= max(0.0, math.cos(heading_error))
        linear = clamp(linear, 0.0, 2.0)
        angular = clamp(angular, -4.0, 4.0)

        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        self.cmd_pub.publish(msg)

        self.history.append(
            (
                time.time() - self.started,
                x,
                y,
                theta,
                linear,
                angular,
                distance_error,
            )
        )

        self.previous_distance_error = distance_error
        self.previous_heading_error = heading_error

        if distance_error < 0.10:
            self.get_logger().info(
                f"Waypoint {self.wp_index + 1}/{len(self.waypoints)} reached: "
                f"ed={distance_error:.3f} m"
            )
            self.wp_index += 1
            self.distance_integral = 0.0
            self.heading_integral = 0.0
            self.previous_distance_error = 0.0
            self.previous_heading_error = 0.0

    def finish(self):
        if self.timer is None:
            return

        self.timer.cancel()

        stop = Twist()
        self.cmd_pub.publish(stop)

        self.save_csv()
        self.save_plots()

        self.get_logger().info(
            f"All {len(self.waypoints)} waypoints reached. "
            f"Results saved in {self.output_dir}"
        )
        self.get_logger().info("Experiment 6 complete. You can now show the plots to the instructor.")

        # Prevent repeated finish calls.
        self.timer = None

    def save_csv(self):
        path = os.path.join(self.output_dir, "pid_data.csv")
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["time_s", "x", "y", "theta", "linear_velocity", "angular_velocity", "distance_error"]
            )
            writer.writerows(self.history)

    def save_plots(self):
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except Exception as exc:
            self.get_logger().warning(
                f"matplotlib is unavailable, so PNG graphs were not generated: {exc}"
            )
            return

        if not self.history:
            return

        t = [r[0] for r in self.history]
        x = [r[1] for r in self.history]
        y = [r[2] for r in self.history]
        v = [r[4] for r in self.history]
        w = [r[5] for r in self.history]
        e = [r[6] for r in self.history]

        # Required result: linear and angular velocity with respect to time.
        plt.figure()
        plt.plot(t, v, label="Linear velocity")
        plt.plot(t, w, label="Angular velocity")
        plt.xlabel("Time (s)")
        plt.ylabel("Velocity")
        plt.title("PID Motion Control: Velocity vs Time")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "velocity_vs_time.png"))
        plt.close()

        # Required result: X-position vs Y-position.
        plt.figure()
        plt.plot(x, y, label="Robot trajectory")
        wx = [p[0] for p in self.waypoints]
        wy = [p[1] for p in self.waypoints]
        plt.plot(wx, wy, marker="o", linestyle="--", label="Waypoints")
        plt.xlabel("X position")
        plt.ylabel("Y position")
        plt.title("PID Waypoint Tracking: X vs Y")
        plt.grid(True)
        plt.axis("equal")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "trajectory_x_vs_y.png"))
        plt.close()

        # Required result: distance error plot.
        plt.figure()
        plt.plot(t, e, label="Distance error")
        plt.axhline(0.10, linestyle="--", label="Threshold = 0.10 m")
        plt.xlabel("Time (s)")
        plt.ylabel("Distance error (m)")
        plt.title("PID Waypoint Tracking: Distance Error")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "distance_error.png"))
        plt.close()


def main(args=None):
    rclpy.init(args=args)
    node = PIDWaypointController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()


if __name__ == "__main__":
    main()
