#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo "=========================================="
echo "      MOBILE ROBOT ROS 2 LAB"
echo "      ROS 2 Jazzy | Simulation Only"
echo "=========================================="
echo

if [ -f /opt/ros/jazzy/setup.bash ]; then
  source /opt/ros/jazzy/setup.bash
else
  echo "[ERROR] ROS 2 Jazzy was not found at /opt/ros/jazzy."
  echo "Install ROS 2 Jazzy on the lab PC first."
  exit 1
fi

if [ ! -d install/mobile_robot_lab ]; then
  echo "[SETUP] First run detected. Building the ROS 2 package..."
  colcon build --symlink-install
fi

source install/setup.bash

echo
echo "Select experiment:"
echo "  1) ROS 2 Nodes / Topics / Publisher / Subscriber / Turtlesim"
echo "  2) Python Publisher / Subscriber"
echo
read -rp "Enter experiment number [1-2]: " EXP

case "$EXP" in
  1)
    echo
    echo "[RUN] Experiment 1: Turtlesim ROS 2 communication"
    echo "[INFO] A simulator window and keyboard-control terminal will open."
    echo "[INFO] In another terminal you can run:"
    echo "       ros2 node list"
    echo "       ros2 topic list"
    echo "       ros2 topic echo /turtle1/cmd_vel"
    ros2 launch mobile_robot_lab experiment1.launch.py
    ;;
  2)
    echo
    echo "[RUN] Experiment 2: Python publisher/subscriber"
    ros2 launch mobile_robot_lab experiment2.launch.py
    ;;
  *)
    echo "Invalid choice."
    exit 1
    ;;
esac
