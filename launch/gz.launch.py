import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
import launch_ros
from launch_ros.actions import Node


def generate_launch_description():
    pkgPath = launch_ros.substitutions.FindPackageShare(package="robot_sim").find(
        "robot_sim"
    )
    urdfPath = os.path.join(pkgPath, "urdf/robot.urdf")
    world_file = os.path.join(pkgPath, "worlds", "robot_sim_world.sdf")

    with open(urdfPath, "r") as model_file:
        robot_desc = model_file.read()

    params = {"robot_description": robot_desc}

    ign_gazebo = ExecuteProcess(cmd=["gz", "sim", world_file], output="screen")

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[params],
        output="screen",
    )

    # spawn robot urdf
    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-name",
            "my_robot",
            "-topic",
            "/robot_description",
        ],
        output="screen",
    )
    # Bridge
    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist",
            # "/keyboard/keypress@std_msgs/msg/Int32@gz.msgs.Int32",
            "/camera/image_raw@sensor_msgs/msg/Image@gz.msgs.Image",
            "/camera/depth/image_raw@sensor_msgs/msg/Image@gz.msgs.Image",
            # "/camera/depth/image_raw/points@sensor_msgs/msg/PointCloud2@gz.msgs.PointCloudPacked",
        ],
        output="screen",
    )

    return LaunchDescription([ign_gazebo, robot_state_publisher, bridge, spawn_robot])
