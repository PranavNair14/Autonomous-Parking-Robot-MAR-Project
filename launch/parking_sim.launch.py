import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('parking_robot')
    gazebo_share = get_package_share_directory('gazebo_ros')

    world_file = os.path.join(
        pkg_share,
        'worlds',
        'parking_lot.world'
    )

    urdf_file = os.path.join(
        pkg_share,
        'urdf',
        'robot.urdf'
    )

    with open(urdf_file, 'r') as f:
        robot_description = f.read()

    gzserver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                gazebo_share,
                'launch',
                'gzserver.launch.py'
            )
        ),
        launch_arguments={
            'world': world_file,
            'verbose': 'false',
            'extra_gazebo_args': '-s libgazebo_ros_factory.so'
        }.items()
    )

    gzclient = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                gazebo_share,
                'launch',
                'gzclient.launch.py'
            )
        )
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }]
    )

    spawn_robot = TimerAction(
        period=3.0,
        actions=[
            Node(
                package='gazebo_ros',
                executable='spawn_entity.py',
                arguments=[
                    '-entity', 'parking_bot',
                    '-file', urdf_file,
                    '-x', '-3.0',
                    '-y', '0.0',
                    '-z', '0.12',
                    '-Y', '0.0'
                ],
                output='screen'
            )
        ]
    )

    parking_node = TimerAction(
        period=5.0,
        actions=[
            Node(
                package='parking_robot',
                executable='parking_node',
                output='screen'
            )
        ]
    )

    return LaunchDescription([
        LogInfo(
            msg='========================================'
        ),
        LogInfo(
            msg=' Autonomous Parking Robot - Simulation Launch'
        ),
        LogInfo(
            msg='========================================'
        ),

        gzserver,
        gzclient,
        robot_state_publisher,

        LogInfo(
            msg='[Launch] Spawning robot into Gazebo...'
        ),
        spawn_robot,

        LogInfo(
            msg='[Launch] Starting autonomous parking node...'
        ),
        parking_node
    ])
