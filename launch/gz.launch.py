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

    # # bridge cmd_vel topic from ros2 to gazebo and vice versa
    # bridge_to_gz_twist = Node(
    #     package="ros_gz_bridge",
    #     executable="parameter_bridge",
    #     arguments=["/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist"],
    #     output="screen",
    # )

    # bridge_to_gz_key = Node(
    #     package="ros_gz_bridge",
    #     executable="parameter_bridge",
    #     arguments=["/keyboard/keypress@std_msgs/msg/Int32@gz.msgs.Int32"],
    #     output="screen",
    # )

    # Bridge
    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist",
            "/keyboard/keypress@std_msgs/msg/Int32@gz.msgs.Int32",
            "/camera@sensor_msgs/msg/Image@gz.msgs.Image",
            "/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo",
        ],
        output="screen",
    )

    return LaunchDescription([ign_gazebo, robot_state_publisher, spawn_robot, bridge])
