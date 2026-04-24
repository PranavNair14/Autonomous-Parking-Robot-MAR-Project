from setuptools import setup
import os
from glob import glob

package_name = 'parking_robot'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        # Package index
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        # package.xml
        ('share/' + package_name, ['package.xml']),
        # Launch files
        (
            os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py'),
        ),
        # URDF models
        (
            os.path.join('share', package_name, 'urdf'),
            glob('urdf/*.urdf'),
        ),
        # Gazebo world files
        (
            os.path.join('share', package_name, 'worlds'),
            glob('worlds/*.world'),
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Student',
    maintainer_email='student@university.edu',
    description='Autonomous Parking Robot using ROS 2 Humble and Gazebo Classic',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # Main parking behaviour node
            'parking_node = parking_robot.parking_node:main',
        ],
    },
)
