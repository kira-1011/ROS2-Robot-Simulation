import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
import launch_ros


def generate_launch_description():
    pkgPath = launch_ros.substitutions.FindPackageShare(package="robot_sim").find(
        "robot_sim"
    )
    world_file = os.path.join(pkgPath, "worlds", "robot_sim_world.sdf")

    # Launch Ignition Gazebo
    ign_gazebo = ExecuteProcess(cmd=["gz", "sim", world_file], output="screen")

    return LaunchDescription([ign_gazebo])
