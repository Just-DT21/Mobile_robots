from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node


def generate_launch_description():
    turtlesim = Node(
        package="turtlesim",
        executable="turtlesim_node",
        name="turtlesim",
        output="screen",
    )

    # Open keyboard control in a separate terminal so the simulator remains visible.
    teleop_cmd = (
        "if command -v gnome-terminal >/dev/null 2>&1; then "
        "gnome-terminal -- bash -lc 'ros2 run turtlesim turtle_teleop_key; exec bash'; "
        "elif command -v xterm >/dev/null 2>&1; then "
        "xterm -e 'bash -lc \"ros2 run turtlesim turtle_teleop_key; exec bash\"'; "
        "else "
        "echo '[ERROR] Need gnome-terminal or xterm for keyboard control.'; "
        "fi"
    )

    teleop = ExecuteProcess(
        cmd=["bash", "-lc", teleop_cmd],
        output="screen",
    )

    instructions = ExecuteProcess(
        cmd=["bash", "-lc",
             "sleep 3; "
             "echo ''; echo '===== EXPERIMENT 1: LIVE ROS 2 INSPECTION ====='; "
             "echo 'Run these commands in a second terminal while the turtle is moving:'; "
             "echo '  ros2 node list'; "
             "echo '  ros2 topic list'; "
             "echo '  ros2 node info /teleop_turtle'; "
             "echo '  ros2 node info /turtlesim'; "
             "echo '  ros2 topic info /turtle1/cmd_vel'; "
             "echo '  ros2 interface show geometry_msgs/msg/Twist'; "
             "echo '  ros2 topic echo /turtle1/cmd_vel'; "
             "echo 'Use arrow keys in the teleop terminal. Press Ctrl+C to stop.'; "
             "echo '==============================================='"],
        output="screen",
    )

    return LaunchDescription([
        turtlesim,
        TimerAction(period=2.0, actions=[teleop]),
        instructions,
    ])
