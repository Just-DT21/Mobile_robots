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

if [ -f install/setup.bash ]; then
  source install/setup.bash
fi

echo "Select experiment:"
echo "  1) ROS 2 Nodes / Topics / Publisher / Subscriber / Turtlesim"
echo "  2) Python Publisher / Subscriber"
echo
read -rp "Enter experiment number [1-2]: " EXP

case "$EXP" in
  1)
    echo
    echo "[1/3] Starting Turtlesim..."
    ros2 launch mobile_robot_lab experiment1.launch.py
    ;;
  2)
    echo
    echo "[1/2] Starting Python publisher/subscriber demo..."
    echo "Open the second terminal for the subscriber when prompted."
    ros2 launch mobile_robot_lab experiment2.launch.py
    ;;
  *)
    echo "Invalid choice."
    exit 1
    ;;
esac
