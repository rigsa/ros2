---  
title: "Waffle (& ROS) Basics"  
---

# Waffle (& ROS) Basics

Having completed the steps on [the previous page](./launching-ros.md), your robot and laptop should now be paired, and ROS should be up and running (on the robot). The next thing to do is bring the robot to life! 

On this page you'll work through a series of exercises with the Waffle **in your teams**, exploring how the robot works. We'll also talk through some core ROS concepts and use some key ROS tools, in case you haven't had a chance to explore these in simulation already.

### Quick Links

* [Exercise 1: Making the Robot Move](#exMove)
* [Exercise 2: Seeing the Sensors in Action](#exViz)
* [Exercise 3: Visualising the ROS Network](#exNet)
* [Exercise 4: Exploring ROS Topics and Interfaces](#exTopicMsg)
* [Exercise 5: Creating Your First Python ROS Node](#exSimpleVelCtrl)
* [Exercise 6: Using SLAM to create a map of the environment](#exSlam)

## Prerequisite: Robot-Laptop 'Bridging'

The robot and laptop both communicate over the University network via [a Zenoh Bridge](https://github.com/eclipse-zenoh/zenoh-plugin-ros2dds). The bridge should already be running on the robot after having run the `tb3_bringup` command on the robot earlier. The next step is to establish a connection to this bridge from the laptop, so that all ROS nodes, topics etc. can communicate as necessary. 

Open up a new terminal instance on the laptop (either by using the ++ctrl+alt+t++ keyboard shortcut, or by clicking the Terminal App icon) and enter the following command:

```bash
waffle X bridge
```
You should now have two terminals active: 

1. A *robot* terminal where you ran the `tb3_bringup` command[^term_recover]
1. The *laptop* terminal where you've just run the `bridge` command

[^term_recover]: If you happen to have closed down the *robot* terminal, you can return to it by entering `waffle X term` from a new terminal instance on the laptop.

Leave both of these terminals alone, but **keep them running in the background at all times** while working with your robot.

## Manual Control

#### :material-pen: Exercise 1: Making the Robot Move {#exMove}

There's a very useful ready-made ROS application called `turtlebot3_teleop/teleop_keyboard` that we will use to drive a Waffle around. This node works in exactly the same way in both simulation and in the real-world!

1. Open up a new terminal instance on the laptop either by using the ++ctrl+alt+t++ keyboard shortcut, or by clicking the Terminal App icon, we'll refer to this as **TERMINAL 1**. In this terminal enter the following `ros2 run` command to launch `turtlebot3_teleop_keyboard`:

    ***
    **TERMINAL 1:**
    ```bash
    ros2 run turtlebot3_teleop teleop_keyboard
    ```
    ***

1. Follow the instructions provided in the terminal to drive the robot around using specific buttons on the keyboard:

    <figure markdown>
      ![](../images/cli/teleop_keymap.svg)
    </figure>

    !!! warning 
        Take care to avoid any obstacles or other people in the lab as you do this!

2. Once you've spent a bit of time on this, close the application down by entering ++ctrl+c++ in **TERMINAL 1**.

## Packages and Nodes

ROS applications are organised into *packages*. Packages are basically folders containing scripts, configurations and launch files (ways to launch those scripts and configurations).  

*Scripts* tell the robot what to do and how to act. In ROS, these scripts are called *nodes*. *ROS Nodes* are executable programs that perform specific robot tasks and operations. These are typically written in C++ or Python, but it's possible to write ROS Nodes using other programming languages too.

There are two key ways to launch ROS applications:

1. `ros2 launch`
1. `ros2 run`

Recall that we just used the `ros2 run` command in Exercise 1 to launch the `teleop_keyboard` node. This command has the following structure:

``` { .bash .no-copy }
ros2 run {[1] Package name} {[2] Node name}
```    

**Part [1]** specifies the name of the *ROS package* containing the functionality that we want to execute. **Part [2]** is used to specify a *single* script within that package that we want to execute. We therefore use `ros2 run` commands to launch **single** executables (aka *Nodes*) onto the ROS network (in Exercise 1 for example, we launched the `teleop_keyboard` node).

The `ros2 launch` command has a *similar* structure:

``` { .bash .no-copy }
ros2 launch {[1] Package name} {[2] Launch file}
```

Here, **Part [1]** is the same as the `ros2 run` command, but **Part [2]** is slightly different: `{[2] Launch file}`. In this case, **Part [2]** is a file within that package that specifies any number of Nodes that we want to launch onto the ROS network. We can therefore launch *multiple* nodes at the same time from a single launch file.

## Sensors & Visualisation Tools

Our Waffles have some pretty sophisticated sensors on them, allowing them to "see" the world around them. Let's now see what our robot sees, using some handy ROS tools.

#### :material-pen: Exercise 2: Seeing the Sensors in Action {#exViz}

1. There shouldn't be anything running in **TERMINAL 1** now, after you closed down the `teleop_keyboard` node (using ++ctrl+c++) at the end of the previous exercise. Return to this terminal and enter the following command:

    ***
    **TERMINAL 1:**
    ```bash
    ros2 launch tuos_tb3_tools rviz.launch.py
    ```
    ***
    
    This will launch an application called *RViz*, which is a handy tool that allows us to *visualise* the data from all the sensors on-board our robots. When RViz opens, you should see something similar to the following:

    <figure markdown>
      TODO
    </figure>

    In the bottom left-hand corner of the RViz screen there should be a Camera panel, displaying a live image feed from the robot's camera.
    
    !!! bug "No camera images?"
        TODO
    
    In the main RViz panel you should see a digital render of the robot, surrounded by lots of green dots. This is a representation of the *laser displacement data* coming from the LiDAR sensor (the black device on the top of the robot). The LiDAR sensor spins continuously, sending out laser pulses into the environment as it does so. When a pulse hits an object it is reflected back to the sensor, and the time it takes for this to happen is used to calculate how far away the object is.
    
    The LiDAR sensor spins and performs this process continuously, so a full 360&deg; scan of the environment can be generated. This data is therefore really useful for things like *obstacle avoidance* and *mapping*. <!-- We'll explore this in more detail later. -->

1. Place your hand in front of the robot and see if the position of the green dots change to match your hand's location. Move your hand up and down and consider at what height the LiDAR sensor is able to detect it.

1. Then, move your hand closer and further away and watch how the green dots move to match this. 

1. Open up a new terminal instance (**TERMINAL 2**) and launch the `teleop_keyboard` node as you did in Exercise 1. Watch how the data in the RViz screen changes as you drive the robot around a bit.

#### :material-pen: Exercise 3: Visualising the ROS Network {#exNet}

Using `ros2 run` and `ros2 launch`, as we have done so far, it's easy to end up with a lot of different processes or *ROS Nodes* running on the network, some of which we will interact with, but others may just be running in the background. It is often useful to know exactly what *is* running on the ROS network, and there are a few ways to do this.

1. Open up a new terminal instance now (**TERMINAL 3**) and from here use the `ros2 node` command to *list* the nodes that are currently running:

    ***
    **TERMINAL 3:**
    ```bash
    ros2 node list
    ```
    ***

    You may notice up to 4 items in the list.

2. We can visualise the connections between the active nodes by using a ROS node called `rqt_graph`. Launch this as follows:

    ***
    **TERMINAL 3:**
    ```bash
    rqt
    ```
    ***

    A window should then open:

    <figure markdown>
      ![](../images/rqt/main.png){width=600}
    </figure>

1. From here, we then want to load the *Node Graph* plugin. From the top menu select `Plugins` > `Introspection` > `Node Graph`.

1. In the window that opens, select `Nodes/Topics (active)` from the dropdown menu in the top left. 

    What you should then see is a map of all the nodes in the list from above (as ovals), and arrows to illustrate the flow of information between them. This is a visual representation of the ROS network!
    
    Items that have a rectangular border are *ROS Topics*. ROS Topics are essentially communication channels, and ROS Nodes can read (*subscribe*) or write (*publish*) to these topics to access sensor data, pass information around the network and make things happen.

    If the `teleop_keyboard` Node is still active (in **TERMINAL 2**) then this graph should show us that the node is publishing messages to a topic called `/cmd_vel`, which in turn is being subscribed to by the `zenoh_bridge_ros2dds` Node. The Zenoh Bridge node is what handles all communication between the robot and the laptop, so this node is tunnelling the data from `/cmd_vel` to the robot to make it move.

A ROS Robot could have hundreds of individual nodes running simultaneously to carry out all its necessary operations and actions. Each node runs independently, but uses *ROS communication methods* to communicate and share data with the other nodes on the ROS Network.

## Publishers and Subscribers: A *ROS Communication Method* 

ROS Topics are key to making things happen on a robot. Nodes can publish (*write*) and/or subscribe to (*read*) ROS Topics in order to share data around the ROS network. Data is published to topics via *message interfaces*.

Let's have a look at this in a bit more detail...

#### :material-pen: Exercise 4: Exploring ROS Topics and Interfaces {#exTopicMsg}

Much like the `ros2 node list` command, we can use `ros2 topic list` to list all the *topics* that are currently active on the ROS network.

1. Close down the RQT Graph window if you haven't done so already. This will release **TERMINAL 3** so that we can enter commands in it again. Return to this terminal window and enter the following:

    ***
    **TERMINAL 3:**
    ```bash
    ros2 topic list
    ```
    ***

    A much larger list of items should be printed to the terminal now. See if you can spot the `/cmd_vel` item in the list.
    
    This topic is used to control the velocity of the robot (*'command velocity'*).

1. Let's find out more about this using the `ros2 topic info` command.

    ***
    **TERMINAL 3:**
    ```bash
    ros2 topic info /cmd_vel
    ```
    ***

    This should provide an output similar to the following: 
    
    ``` { .txt .no-copy }
    Type: geometry_msgs/msg/Twist
    Publisher count: 1
    Subscription count: 1
    ```

    This tells us that the *type* of data being communicated on the `/cmd_vel` topic is called: `geometry_msgs/msg/Twist`. 
    
    The message type has three parts:

    1. `geometry_msgs`: The name of the ROS package that this interface belongs to.
    1. `msg`: The type of interface. In this case *message*, but there are other types too. 
    1. `Twist`: The name of the message interface. 

    We have just learnt then, that if we want to make the robot move we need to publish `Twist` messages to the `/cmd_vel` topic. 

1. We can use the `ros2 interface` command to find out more about the `Twist` message:

    ***
    **TERMINAL 3:**
    ```bash
    ros2 interface show geometry_msgs/msg/Twist
    ```
    ***

    From this, we should obtain the following:

    ``` { .txt .no-copy }
    Vector3  linear
            float64 x
            float64 y
            float64 z
    Vector3  angular
            float64 x
            float64 y
            float64 z
    ```

    Let's find out what it all means...

## Velocity Control

The motion of any mobile robot can be defined in terms of its three *principal axes*: `X`, `Y` and `Z`. In the context of our TurtleBot3 Waffle, these axes (and the motion about them) are defined as follows:

<figure markdown>
  ![](../images/waffle/principal_axes.svg){width=600}
</figure>

In theory then, a robot can move *linearly* or *angularly* about any of these three axes, as shown by the arrows in the figure. That's six *Degrees of Freedom* (DOFs) in total, achieved based on a robot's design and the actuators it is equipped with. Take a look back at the `ros2 interface show` output above. Hopefully it's a bit clearer now that these topic messages are formatted to give a ROS Programmer the ability to *ask* a robot to move in any one of its six DOFs. 

``` { .txt .no-copy }
Vector3  linear
        float64 x  <-- Forwards (or Backwards)
        float64 y  <-- Left (or Right)
        float64 z  <-- Up (or Down)
Vector3  angular
        float64 x  <-- "Roll"
        float64 y  <-- "Pitch"
        float64 z  <-- "Yaw"
```

Our TurtleBot3 robot only has two motors, so it doesn't actually have six DOFs! The two motors can be controlled independently, which gives it what is called a *"differential drive"* configuration, but this still only allows it to move with **two degrees of freedom** in total, as illustrated below.

<figure markdown>
  ![](../images/waffle/velocities.svg){width=600}
</figure>

It can therefore only move **linearly** in the **x-axis** (*Forwards/Backwards*) and **angularly** in the **z-axis** (*Yaw*). 

#### :material-pen: Exercise 5: Creating Your First Python ROS Node {#exSimpleVelCtrl}

!!! important
    Before you start this, close down RViz (click the "Close without saving" button, if asked) and stop the `teleop_keyboard` node by entering ++ctrl+c++ in **TERMINAL 2**.

Making a robot move with ROS is simply a case of publishing the right ROS Message (`Twist`) to the right ROS Topic (`/cmd_vel`). In some of the previous exercises above you used the Keyboard Teleop node to drive the robot around, a bit like a remote control car. In the background here all that was really happening was that the Teleop node was converting our keyboard button presses into velocity commands and publishing these to the `/cmd_vel` topic.

In reality, robots need to be able to navigate complex environments autonomously, which is quite a difficult task, and requires us to build bespoke applications. We can build these applications using Python, and we'll look at the core concepts behind this now by building a simple node that will allow us to make our robot a bit more "autonomous". What we will do here forms the basis of the more complex applications that you will learn about in [Assignment #1](../com2009/assignment1/README.md) and implement in [Assignment #2](../com2009/assignment2/README.md) to bring a real robot to life!

1. You will create your first ROS node inside your team's `com2009_team999` ROS package, which you should have cloned to the laptop earlier on. This package should now correctly reside within the Catkin Workspace on the laptop's filesystem. Navigate to this from **TERMINAL 1** using the `roscd` command:

    ***
    **TERMINAL 1:**
    ``` { .bash .no-copy }
    roscd com2009_team999/ 
    ```
    Replacing `com2009_team999` accordingly.
    ***

1. Then, use the `cd` command to move into the `src` directory that should already exist within your package:

    ***
    **TERMINAL 1:**
    ```bash
    cd src/ 
    ```
    ***

1. In here, create a Python file called `simple_move_square.py` using the `touch` command:

    ***
    **TERMINAL 1:**
    ```bash
    touch simple_move_square.py
    ```
    ***

1. You'll need to change the *execution permissions* for this file in order to be able to run it later on. You'll learn more about this in Assignment #1 but, for now, simply run the following command:

    ***
    **TERMINAL 1:**
    ```bash
    chmod +x simple_move_square.py
    ```
    ***

2. Now we want to edit this file, and we'll do that using *Visual Studio Code* (VS Code):

    ***
    **TERMINAL 1:** 
    ```bash
    code .
    ```
    ***

    !!! note
        Don't forget to include the `.` at the end there, it's important!!
    
3. Once VS Code launches, open up the `simple_move_square.py` file, which should be visible in the file explorer on the left-hand side of the VS Code window. Paste the following content into it:

    ```py title="simple_move_square.py"
    #!/usr/bin/env python3

    --8<-- "snippets/move_square_timed.py"
    ```

    1. `rospy` is the ROS client library for Python. We need this so that our Python node can interact with ROS.
    2. We know from earlier that in order to make a robot move we need to publish messages to the `/cmd_vel` topic, and that this topic uses `Twist` messages from the `geometry_msgs` package. This is how we import that message, from that package, in order to create velocity commands in Python (which we'll get to shortly...)
    3. Before we do anything we need to initialise our node to register it on the ROS network with a name. We're calling it "move_waffle" in this case, and we're using `anonymous=True` to ensure that there are no other nodes of the same name already registered on the network.
    4. We want our main `while` loop (when we get to that bit) to execute 10 times per second (10 Hz), so we create a `rate` object here which will be used to control the rate of the main loop later...
    5. Here we are setting up a publisher to the `/cmd_vel` topic so that the node can write `Twist` messages to make the robot move.
    6. We're instantiating a `Twist` message here and calling it `vel` (we'll assign velocity values to this in the `while` loop later on). A `Twist` message contains six different components that we can assign values to. Any idea [what these six values might represent](#velocity-control)?  
    7. What time is it right now? (This will be useful to compare against in the while loop.)
    8. We're entering the main `while` loop now. This `rospy.is_shutdown()` function will read `False` unless we request for the node to be stopped (by pressing ++ctrl+c++ in the terminal). Once it turns `True` the `while` loop stops.
    9. Here we're comparing the time now to the time the last time we checked, to tell us how much time has elapsed (in seconds) since then. We'll use that information to decide what to do...  
    10. The "transition" state is used to stop the robot (if necessary), and check the time again.
    11. In "state1" we set velocities that will make the robot move forwards (linear-X velocity only). If the elapsed time is greater than **2 seconds** however, we move on to "state2".
    12. In "state2" we set velocities that will make the robot turn on the spot (angular-Z velocity only). In this case, if the elapsed time is greater than **4 seconds**, we move back to "state1".
    13. Regardless of what happens in the `if` statements above, we always publish a velocity command to the `/cmd_vel` topic here (i.e. every loop iteration).
    14. We created a `rate` object earlier, and we use this now to make sure that each iteration of this `while` loop takes exactly the right amount of time to maintain the rate of execution that we specified earlier (10 Hz).
    15. Here we're importing some mathematical operators that might be useful... 

        | Mathematical Operation | Python Implementation |
        | :---: | :---: |
        | $\sqrt{a+b}$ | `#!python sqrt(a+b)` |
        | $a^{2}+(bc)^{3}$ | `#!python pow(a, 2) + pow(b*c, 3)` |
        | $\pi r^2$ | `#!python pi * pow(r, 2)` |

    Click on the :material-plus-circle: icons above to expand the code annotations. Read these carefully to ensure that you understand what's going on and how this code works.

4. Now, go back to **TERMINAL 1** and run the code.

    !!! note
        Make sure the robot is on the floor and has enough room to roam around before you do this!
    
    ***
    **TERMINAL 1:**
    ``` { .bash .no-copy }
    rosrun com2009_team999 simple_move_square.py
    ```
    ***
    
    Observe what the robot does. When you've seen enough, enter ++ctrl+c++ in **TERMINAL 1** to stop the node from running, which should also stop the robot from moving.
    
5. As the name may suggest, the aim here is to make the robot follow a square motion path. What you may have observed when you actually ran the code is that the robot doesn't actually do that! We're using a time-based approach to make the robot switch between two different states continuously:
    1. Moving forwards
    2. Turning on the spot
    
    Have a look at the code to work out how much time the robot will currently spend in each state.
    
6.  The aim here is to make the robot follow a **0.5m x 0.5m square** motion path.  In order to properly achieve this you'll need to adjust the timings, or the robot's velocity, or both. Edit the code so that the robot actually follows a **0.5m x 0.5m square motion path**!

## SLAM

Simultaneous Localisation and Mapping (SLAM) is a sophisticated tool that is built into ROS. Using data from the robot's LiDAR sensor, plus knowledge of how far the robot has moved[^odom] the robot is able to create a map of its environment *and* keep track of its location within that environment at the same time. IN the exercise that follows you'll see easy it is to implement SLAM on the real robot.  

[^odom]: You'll learn much more about "Robot Odometry" in [Assignment #1 Part 2](../com2009/assignment1/part2.md), and in the COM2009 Lectures.

#### :material-pen: Exercise 6: Using SLAM to create a map of the environment {#exSlam}

1. In **TERMINAL 1** enter the following command to launch all the necessary SLAM nodes on the laptop:

    ***
    **TERMINAL 1:**
    ```bash
    roslaunch turtlebot3_slam turtlebot3_slam.launch
    ```
    
    ??? tip "Robotics Laptop Tip"
        This command is also available as an alias: `tb3_slam`!

    ***

    This will launch RViz once again, where you should now be able to see a model of the Waffle from a top-down view surrounded by green dots representing the real-time LiDAR data. The SLAM tools will already have begun processing this data to start building a map of the boundaries that are currently visible to the Waffle based on its location in the environment.

    !!! note
        To begin with your robot may just appear as a white shadow (similar to the left-hand image below). It may take some time for the robot to render correctly (like the right-hand image) as the SLAM processes and data communications catch up with one another. 
        
        <figure markdown>
          ![](../images/waffle/slam.png){width=600px}
        </figure>
        
        This can sometimes take up to a minute or so, so please be patient! If (after a minute) nothing has happened, then speak to a member of the teaching team.

1. Return to **TERMINAL 2** and launch the `turtlebot3_teleop_keyboard` node again. Start to drive the robot around *slowly* and *carefully* to build up a complete map of the area.
    
    !!! tip
        It's best to do this slowly and perform multiple circuits of the whole area to build up a more accurate map.

1. Once you're happy that your robot has built up a good map of its environment, you can save this map using a node called `map_saver` from a package called `map_server`:

    1. First, create a new directory within your team's ROS package on the laptop. We'll use this to save maps in. Open up a new terminal instance (**TERMINAL 3**) and navigate to the root of your team's ROS package with `roscd` again:

        ***
        **TERMINAL 3:**
        ``` { .bash .no-copy }
        roscd com2009_team999
        ```
        ***

    1. Create a directory in here called `maps`: 
        
        ***
        **TERMINAL 3:**
        ```bash
        mkdir maps/
        ```
        ***

    2. Navigate into this directory:

        ***
        **TERMINAL 3:**
        ```bash
        cd maps/
        ```
        ***

    2. Then, use `rosrun` to run the `map_saver` node from the `map_server` package to save a copy of your map:

        ***
        **TERMINAL 3:**
        ``` { .bash .no-copy }
        rosrun map_server map_saver -f {map_name}
        ```
        
        Replacing `{map_name}` with an appropriate name for your map. This will create two files: 
        
        1. a `{map_name}.pgm` 
        2. a `{map_name}.yaml` file
        
        ...both of which contain data related to the map that you have just created.

        ***

    1. The `.pgm` file can be opened using an application called `eog` on the laptop: 
    
        ***
        **TERMINAL 3:**
        ``` { .bash .no-copy }
        eog {map_name}.pgm
        ```
        ***

1. Return to **TERMINAL 1** and close down SLAM by pressing ++ctrl+c++. The process should stop and RViz should close down.

1. Close down the Keyboard Teleop node in **TERMINAL 2** as well if that's still running.

## Wrapping Up

Continue onto the next page now for the shutdown procedures that you need to follow at the end of each lab session...
