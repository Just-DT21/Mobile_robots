from launch import LaunchDescription
from launch.actions import TimerAction, ExecuteProcess
from launch_ros.actions import Node


def generate_launch_description():
    turtlesim = Node(
        package="turtlesim",
        executable="turtlesim_node",
        name="turtlesim",
        output="screen",
    )

    pid_controller = Node(
        package="mobile_robot_lab",
        executable="pid_waypoint_node",
        name="pid_waypoint_controller",
        output="screen",
    )

    show_instructions = ExecuteProcess(
        cmd=[
            "bash",
            "-lc",
            "sleep 2; "
            "echo '===== EXPERIMENT 6: PID WAYPOINT TRACKING ====='; "
            "echo 'The PID controller is running automatically.'; "
            "echo 'Distance threshold: ed < 0.10 m'; "
            "echo 'Waypoints: (8,8) -> (8,3) -> (3,3) -> (3,8) -> (5.5,5.5)'; "
            "echo 'Results folder: ~/mobile_robot_lab_ex6_results/'; "
            "echo 'To watch velocity commands, open another terminal and run:'; "
            "echo 'ros2 topic echo /cmd_vel'; "
            "echo '================================================'"
        ],
        output="screen",
    )

    return LaunchDescription([
        turtlesim,
        TimerAction(period=1.5, actions=[pid_controller]),
        TimerAction(period=2.0, actions=[show_instructions]),
    ])
