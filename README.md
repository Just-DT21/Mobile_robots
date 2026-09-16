# Mobile_robots

ROS 2 Jazzy mobile robot lab repository. The experiments are simulation-first so they can be cloned and demonstrated on a lab PC without physical robot hardware.

## Lab setup

Requirements:
- Ubuntu with ROS 2 Jazzy
- Turtlesim
- colcon
- Gazebo Harmonic (gz) for Experiment 5
- Graphical desktop session

Clone and enter the repository:

    git clone https://github.com/Just-DT21/Mobile_robots.git
    cd Mobile_robots

Start the launcher:

    bash lab.sh

The launcher rebuilds the package so newly added experiments are included.

## Experiments

### Experiment 1
ROS 2 nodes, topics, publishers, subscribers and messages using Turtlesim.

### Experiment 2
ROS 2 workspace and Python package with a publisher and subscriber using std_msgs/msg/String.

### Experiment 5 - Gazebo World Creation and Model Insertion

Based on the lab sheet: create a custom Gazebo Harmonic SDF world, add a ground plane and lighting, and insert geometric models. The included world contains:
- Ground plane
- Directional light
- Box
- Sphere
- Cylinder
- Capsule
- Ellipsoid

Run with:

    bash lab.sh
    # choose 5

The world can also be launched directly:

    ros2 launch mobile_robot_lab experiment5.launch.py

### Experiment 6 - PID-Based Path Planning and Motion Control

Based on the lab sheet: a ROS 2 Python PID controller tracks predefined waypoints in Turtlesim. It calculates distance and heading errors and publishes velocity commands on /cmd_vel. The waypoint completion threshold is ed < 0.10.

The controller automatically follows:

    (8,8) -> (8,3) -> (3,3) -> (3,8) -> (5.5,5.5)

Run with:

    bash lab.sh
    # choose 6

Live velocity commands can be viewed on /cmd_vel. After the run, the controller saves:

    ~/mobile_robot_lab_ex6_results/
    pid_data.csv
    velocity_vs_time.png
    trajectory_x_vs_y.png
    distance_error.png

These correspond to the required Experiment 6 result plots:
- Linear and angular velocity with respect to time
- X-position vs Y-position
- Distance error

## Simulation-first

All implemented experiments are designed for simulation and ideal lab demonstration. No physical mobile robot is required.

## Useful ROS 2 commands

    source /opt/ros/jazzy/setup.bash
    source install/setup.bash

    ros2 node list
    ros2 topic list
    ros2 topic info /cmd_vel
    ros2 topic echo /cmd_vel
    ros2 interface show geometry_msgs/msg/Twist