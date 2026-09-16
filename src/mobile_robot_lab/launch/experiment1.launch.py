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

    teleop = Node(
        package="turtlesim",
        executable="turtle_teleop_key",
        name="teleop_turtle",
        output="screen",
        prefix="xterm -e",
    )

    return LaunchDescription([
        turtlesim,
        TimerAction(period=2.0, actions=[teleop]),
        ExecuteProcess(
            cmd=["bash", "-lc",
                 "echo ''; echo '--- ROS 2 inspection commands ---'; "
                 "echo 'ros2 node list'; "
                 "echo 'ros2 topic list'; "
                 "echo 'ros2 topic info /turtle1/cmd_vel'; "
                 "echo 'ros2 interface show geometry_msgs/msg/Twist'; "
                 "echo 'ros2 topic echo /turtle1/cmd_vel'; "
                 "echo ''; echo 'Use arrow keys in the teleop window to move the turtle.'"],
            output="screen",
        ),
    ])
