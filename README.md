# Mobile_robots

ROS 2 Jazzy mobile robot lab repository. The goal is to avoid re-programming the lab PC every time and keep the experiments ready to clone and run.

## Lab setup

Requirements on the lab PC:
- Ubuntu with ROS 2 Jazzy
- Turtlesim
- colcon
- A graphical desktop session

Clone and enter the repository:

```bash
git clone https://github.com/Just-DT21/Mobile_robots.git
cd Mobile_robots
```

Start the lab launcher:

```bash
bash lab.sh
```

The first run automatically builds the ROS 2 Python package. After that, the launcher gives an experiment menu.

## Experiments currently implemented

### Experiment 1
ROS 2 nodes, topics, publishers, subscribers and messages using Turtlesim.

It demonstrates:
- `/teleop_turtle`
- `/turtlesim`
- `/turtle1/cmd_vel`
- `geometry_msgs/msg/Twist`
- topic inspection and message echo
- keyboard-controlled turtle motion
- ROS graph inspection

### Experiment 2
ROS 2 workspace and Python package with a publisher and subscriber.

It demonstrates:
- `ament_python` package structure
- Python publisher node
- Python subscriber node
- `std_msgs/msg/String`
- publisher/subscriber communication on `/chatter`

## Simulation-first

The experiments are intended to be demonstrated in simulation under ideal conditions. No physical robot or hardware is required for the implemented experiments.

## Useful manual commands

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 node list
ros2 topic list
ros2 topic info /turtle1/cmd_vel
ros2 interface show geometry_msgs/msg/Twist
ros2 topic echo /turtle1/cmd_vel
```
