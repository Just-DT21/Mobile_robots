from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():
    world = PathJoinSubstitution([
        FindPackageShare("mobile_robot_lab"),
        "worlds",
        "experiment5_world.sdf",
    ])

    return LaunchDescription([
        ExecuteProcess(
            cmd=["gz", "sim", "-r", world],
            output="screen",
        )
    ])
