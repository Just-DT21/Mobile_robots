#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo "=================================================="
echo "          MOBILE ROBOT ROS 2 LAB"
echo "          ROS 2 Jazzy | Simulation Only"
echo "=================================================="
echo

if [ -f /opt/ros/jazzy/setup.bash ]; then
  source /opt/ros/jazzy/setup.bash
else
  echo "[ERROR] ROS 2 Jazzy was not found at /opt/ros/jazzy."
  echo "Install ROS 2 Jazzy on the lab PC first."
  exit 1
fi

if ! command -v colcon >/dev/null 2>&1; then
  echo "[ERROR] colcon is not installed."
  exit 1
fi

if [ ! -d install/mobile_robot_lab ]; then
  echo "[SETUP] First run detected. Building the ROS 2 package..."
  colcon build --symlink-install
else
  echo "[SETUP] Rebuilding to include the latest experiment files..."
  colcon build --symlink-install
fi

source install/setup.bash

echo
echo "Select experiment:"
echo "  1) ROS 2 Nodes / Topics / Publisher / Subscriber / Turtlesim"
echo "  2) Python Publisher / Subscriber"
echo "  5) Gazebo Harmonic Custom World + Model Insertion"
echo "  6) PID Waypoint Tracking + Motion Control"
echo
read -rp "Enter experiment number [1,2,5,6]: " EXP

case "$EXP" in
  1)
    echo
    echo "[RUN] Experiment 1: Turtlesim ROS 2 communication"
    ros2 launch mobile_robot_lab experiment1.launch.py
    ;;
  2)
    echo
    echo "[RUN] Experiment 2: Python publisher/subscriber"
    ros2 launch mobile_robot_lab experiment2.launch.py
    ;;
  5)
    echo
    echo "[RUN] Experiment 5: Gazebo Harmonic custom world"
    echo "[INFO] World contains a ground plane, lighting and geometric models."
    echo "[INFO] Gazebo will open in simulation mode."
    if ! command -v gz >/dev/null 2>&1; then
      echo "[ERROR] Gazebo (gz) was not found."
      echo "Install Gazebo Harmonic on the lab PC first."
      exit 1
    fi
    ros2 launch mobile_robot_lab experiment5.launch.py
    ;;
  6)
    echo
    echo "[RUN] Experiment 6: PID waypoint tracking"
    echo "[INFO] Turtlesim + PID controller will run automatically."
    echo "[INFO] Distance threshold: ed < 0.10 m"
    echo "[INFO] Results: ~/mobile_robot_lab_ex6_results/"
    ros2 launch mobile_robot_lab experiment6.launch.py
    ;;
  *)
    echo "Invalid choice."
    exit 1
    ;;
esac
