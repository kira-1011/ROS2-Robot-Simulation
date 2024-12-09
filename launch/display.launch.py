import launch
from launch.substitutions import LaunchConfiguration
import launch_ros
import os


def generate_launch_description():
    pkgPath = launch_ros.substitutions.FindPackageShare(package="robot_sim").find(
        "robot_sim"
    )
    urdfPath = os.path.join(pkgPath, "urdf/robot.urdf")

    with open(urdfPath, "r") as model_file:
        robot_desc = model_file.read()

    params = {"robot_description": robot_desc}

    robot_state_publisher_node = launch_ros.actions.Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[params],
    )

    joint_state_publisher_node = launch_ros.actions.Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        name="joint_state_publisher",
        parameters=[params],
        condition=launch.conditions.UnlessCondition(LaunchConfiguration("gui")),
    )
    joint_state_publisher_gui_node = launch_ros.actions.Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        parameters=[params],
        condition=launch.conditions.IfCondition(LaunchConfiguration("gui")),
    )

    rviz_node = launch_ros.actions.Node(
        package="rviz2", executable="rviz2", name="rviz2", output="screen"
    )

    return launch.LaunchDescription(
        [
            launch.actions.DeclareLaunchArgument(
                name="gui",
                default_value="True",
                description="flag for joint state publisher gui",
            ),
            launch.actions.DeclareLaunchArgument(
                name="model",
                default_value=urdfPath,
                description="path to urdf model file",
            ),
            robot_state_publisher_node,
            joint_state_publisher_node,
            joint_state_publisher_gui_node,
            rviz_node,
        ]
    )
