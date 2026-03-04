---
title: "Creating your Team's ROS 2 Package"
description: "The first step is to create a ROS package for your code to live in" 
---

# Creating your Team's ROS 2 Package

You should use the same procedures as you did in the Simulation Labs to create a ROS 2 package for this assignment (described again below). You should create **one package per team**, so nominate **one** member of your team to do this bit.

You should do this from within your own local ROS installation (i.e. on your own computer), or a WSL-ROS2 terminal instance.

1. Head to the `src` folder of your ROS 2 workspace in your terminal:

    ```bash
    cd ~/ros2_ws/src/
    ```

1. Clone the *ROS 2 Package Template* from GitHub:

    ```bash
    git clone https://github.com/tom-howard/ros2_pkg_template.git
    ```
    
1. Run the `init_pkg.sh` script as follows (**pay attention to the further information below about the naming of your package**):

    ``` { .bash .no-copy }
    ./ros2_pkg_template/init_pkg.sh ele434_teamXX_2026
    ```

    Your package **must** be named as follows: `ele434_teamXX_2026`

    ... where `XX` should be replaced with *your* team number (see Blackboard if you are unsure what your team's number is).

    **If your team number is less than 10**: put a zero before it, so that the team number is **always** 2 digits long, e.g.: 
    
    * `ele434_team03_2026` for **Team 3**
    * `ele434_team08_2026` for **Team 8**
    * `ele434_team15_2026` for **Team 15**

    !!! warning "Important"
        Your repository name should match the above format **exactly**:
            
        * The name should be **18 characters long** in total.
        * All characters should be **lower case** (e.g. `ele434`, **NOT** `ELE434`)

1. Next, navigate into the **root** of your new package:

    ``` { .bash .no-copy }
    cd ./ele434_teamXX_2026/
    ```

    ...and create a new directory in there called `launch`:

    ```bash
    mkdir launch
    ```

1. Inside here create an empty file called `explore.launch.py`:

    ```bash
    touch ./launch/explore.launch.py
    ```

    ... leave this empty for now. You'll need to populate this appropriately later (more details on [the Task Brief](./task.md)).

1. Open up your package's `CMakeLists.txt` file and add the following text **just above** the `ament_package()` line at the very bottom:

    ```txt title="ele434_teamXX_2026/CMakeLists.txt"
    install(DIRECTORY
      launch
      DESTINATION share/${PROJECT_NAME}
    )
    ```

1. You can now build this using Colcon by following **the same three-step process** that you have been following throughout the Simulation Lab Course:

    1. **Step 1**, navigate to the **root** of the ROS 2 workspace:

        ```bash
        cd ~/ros2_ws/
        ```

    1. **Step 2**, build your package with Colcon:

        ``` { .bash .no-copy }
        colcon build --packages-select ele434_teamXX_2026 --symlink-install
        ```

    1. **Step 3**, re-source the `.bashrc`:

        ```bash
        source ~/.bashrc
        ```
    
    !!! tip "Don't forget"
        You'll need to follow the above **three-step** `colcon build` process whenever you do things like:

        1. Add a new node to your package (don't forget to modify the `CMakeLists.txt` file too)
        1. Add **or modify** a launch file
        1. Add **or modify** a custom interface (like in [Part 1](../../course/part1.md#ex7))
        1. Copy your package onto a different computer 

## See Also

* [Transferring Your ROS Package to the Robotics Laptops](./first-lab.md#transferring-your-ros-package-to-the-robotics-laptops)
* [Exporting Your ROS Package for Submission](./submission.md#exporting-your-ros-package-for-submission)