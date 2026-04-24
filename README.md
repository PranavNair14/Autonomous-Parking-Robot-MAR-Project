# Autonomous-Parking-Robot-MAR-Project

# Autonomous Parking Detection System using ROS 2 and Gazebo

## Project Overview

This project focuses on designing and simulating an Autonomous Parking Detection System using ROS 2 Humble and Gazebo. The system is capable of detecting available parking slots in a structured parking environment and identifying empty spaces for vehicles.

The system is developed and tested in Ubuntu using ROS 2, Gazebo simulation, URDF modeling, and Python-based detection logic.

---

## Objective

The main objective of this project is to develop a smart parking detection system capable of:

- Detecting available parking spaces
- Identifying empty parking slots in real time
- Assisting in efficient parking management
- Reducing time spent searching for parking spaces

---

## Technologies Used

- ROS 2 Humble
- Gazebo Simulator
- Ubuntu 22.04
- Python
- URDF (Unified Robot Description Format)
- RViz2
- Linux Terminal / WSL

---

## Project Structure

- `launch/` → Launch files for simulation
- `urdf/` → Robot model and configuration files
- `worlds/` → Gazebo simulation world files
- `resource/` → ROS package resource files
- `parking_robot/` → Python source files for detection logic
- `package.xml` → ROS package configuration
- `setup.py` → Python package setup
- `setup.cfg` → Setup configuration

---

## Implementation Details

1. Designed the robot model using URDF
2. Configured wheels, sensors, and LiDAR setup
3. Created the parking environment in Gazebo
4. Implemented parking slot detection logic using Python
5. Integrated ROS 2 nodes for environment scanning and slot identification
6. Tested the system in simulation for accurate empty slot detection

---

## How to Run

### Step 1: Open Terminal

cd ~/ros2_ws
colcon build
source install/setup.bash

## Step 2: Launch Gazebo Simulation

ros2 launch parking_robot parking.launch.py

Step 3: Observe Parking Slot Detection
The robot scans the environment and detects available empty parking slots inside the Gazebo simulation.


cd ~/ros2_ws
colcon build
source install/setup.bash
