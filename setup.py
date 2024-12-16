from setuptools import find_packages, setup
import os
from glob import glob

package_name = "robot_sim"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (
            os.path.join("share", package_name, "launch"),
            glob(os.path.join("launch", "*launch.[pxy][yma]*")),
        ),
        (
            os.path.join("share", package_name, "urdf"),
            glob(os.path.join("urdf", "*.urdf*")),
        ),
        (
            os.path.join("share", package_name, "rviz"),
            glob(os.path.join("rviz", "*.rviz*")),
        ),
        (
            os.path.join("share", package_name, "worlds"),
            glob(os.path.join("*", "*.sdf*")),
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="kira",
    maintainer_email="kirubel.s.tadesse@gmail.com",
    description="robot simulation package",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "move_robot=robot_sim.robot:main",
            "opencv_node=robot_sim.opencv:main",
        ],
    },
)
