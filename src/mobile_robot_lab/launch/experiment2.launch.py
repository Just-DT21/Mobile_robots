from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    publisher = Node(
        package="mobile_robot_lab",
        executable="publisher_node",
        name="publisher_node",
        output="screen",
    )

    subscriber = Node(
        package="mobile_robot_lab",
        executable="subscriber_node",
        name="subscriber_node",
        output="screen",
    )

    return LaunchDescription([publisher, subscriber])
