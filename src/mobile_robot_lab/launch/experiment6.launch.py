from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node


def generate_launch_description():
    turtle = Node(
        package="turtlesim",
        executable="turtlesim_node",
        name="turtlesim",
        output="screen",
    )

    pid = Node(
        package="mobile_robot_lab",
        executable="pid_waypoint_node",
        name="pid_waypoint_controller",
        output="screen",
    )

    topic_echo_cmd = (
        "if command -v gnome-terminal >/dev/null 2>&1; then "
        "gnome-terminal -- bash -lc 'echo "===== /cmd_vel LIVE ====="; "
        "ros2 topic echo /cmd_vel; exec bash'; "
        "elif command -v xterm >/dev/null 2>&1; then "
        "xterm -e 'bash -lc \"echo ===== /cmd_vel LIVE =====; "
        "ros2 topic echo /cmd_vel; exec bash\"'; "
        "else echo '[INFO] Open another terminal and run: ros2 topic echo /cmd_vel'; fi"
    )

    instructions = ExecuteProcess(
        cmd=["bash", "-lc",
             "sleep 2; "
             "echo ''; echo '===== EXPERIMENT 6: PID WAYPOINT TRACKING ====='; "
             "echo 'PID controller is running automatically.'; "
             "echo 'Distance threshold: ed < 0.10 m'; "
             "echo 'Waypoints: (8,8) -> (8,3) -> (3,3) -> (3,8) -> (5.5,5.5)'; "
             "echo 'Results will be saved to ~/mobile_robot_lab_ex6_results/'; "
             "echo '==============================================='"],
        output="screen",
    )

    topic_echo = ExecuteProcess(
        cmd=["bash", "-lc", topic_echo_cmd],
        output="screen",
    )

    return LaunchDescription([
        turtle,
        TimerAction(period=1.5, actions=[pid]),
        TimerAction(period=2.0, actions=[instructions, topic_echo]),
    ])
