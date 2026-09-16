from setuptools import setup
from glob import glob
import os

package_name = "mobile_robot_lab"

setup(
    name=package_name,
    version="1.0.0",
    packages=[package_name],
    data_files=[
        (
            "share/ament_index/resource_index/packages",
            ["resource/" + package_name],
        ),
        ("share/" + package_name, ["package.xml"]),
        (
            os.path.join("share", package_name, "launch"),
            glob("launch/*.launch.py"),
        ),
        (
            os.path.join("share", package_name, "worlds"),
            glob("worlds/*.sdf"),
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    description="ROS 2 Jazzy mobile robot laboratory experiments.",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "publisher_node = mobile_robot_lab.publisher_node:main",
            "subscriber_node = mobile_robot_lab.subscriber_node:main",
            "pid_waypoint_node = mobile_robot_lab.pid_waypoint_node:main",
        ],
    },
)
