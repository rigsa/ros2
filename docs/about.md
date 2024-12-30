---
title: "About this Site"
---
 
## Welcome

This is the home of some *practical robotics courses* at the University of Sheffield, designed to teach students how to use ROS2 (The Robot Operating System, Version 2) with TurtleBot3 Waffle robots, using a mix of simulation-based learning and real robot hardware. Most of the initial learning is done in simulation, after which students are able to apply their new-found ROS knowledge to our [real TurtleBot3 Waffle Robots](#robots) in The Diamond.

The materials here are developed by [Dr Tom Howard](https://www.sheffield.ac.uk/engineering/diamond-engineering/our-staff/tom-howard), a University Teacher in the [Multidisciplinary Engineering Education Team](https://www.sheffield.ac.uk/engineering/diamond-engineering/about-us) in **The Diamond**.

These resources were primarily developed for **COM2009**: a second-year undergraduate module for [The School of Computer Science](https://www.sheffield.ac.uk/cs). These resources are *also* used to teach masters-level Mechatronic and Robotic Engineering students in [The School of Electrical and Electronic Engineering](https://www.sheffield.ac.uk/eee) (**ACS6121**). 

## License

<center><a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a></center>

This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.

## Introducing the Robots: The TurtleBot3 Waffle

### Turtlebot what?!

To teach ROS here we use the [TurtleBot3 Waffle](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/) robot, made by Robotis. This is the 3rd Generation Robot in the [TurtleBot family](http://wiki.ros.org/Robots/TurtleBot) (which has been the reference hardware platform for ROS since 2010). The TurtleBot Robot family exists to provide accessible and relatively low-cost hardware and open-source software on a robot platform, to encourage people to learn robotics and ROS and make it as easy as possible to do so.

Here in the Diamond we have a total of 50 *customised* TurtleBot3 Waffles specifically for teaching this course:

<figure markdown>
  ![](../images/waffle/cabinet.jpg){width=500px} 
</figure>

Our robots are an enhanced version of the *TurtleBot3 WafflePi* that you can buy from Robotis. We've made a few adjustments, as shown below:

<figure markdown>
  ![](../images/waffle/features.png){width=800px}
</figure>

The Waffles have the following core hardware elements:

* An OpenCR Micro-Controller Board to power and control the wheel motors, distribute power to other hardware elements and provide an interface for additional sensors.
* An [UP Squared Single-Board Computer (SBC)](https://up-board.org/upsquared/specifications/) with an Intel Processor and 32GB of on-board eMMC storage. This board acts as the "brain" of the robot.
* Independent left and right wheel motors (DYNAMIXEL XM430’s) to drive the robot using a *differential drive* configuration.

This drive configuration allows the robots to move with the following **maximum velocities**: <a name="max_vels"></a>

<center>

| Velocity Component | Upper Limit | Units |
| :--- | :---: | :--- |
| *Linear* | 0.26 | m/s |
| *Angular* | 1.82 | rad/s |

</center>

In addition to this, the robots are equipped with the following sensors:

* A Light Detection and Ranging (or *LiDAR*) sensor, which spins continuously when the robot is in operation. This uses light in the form of laser pulses to allow the robot to measure the distance to surrounding objects, providing it with a 360&deg; view of its environment.
* An [Intel RealSense D435 Camera](https://www.intelrealsense.com/depth-camera-d435/) with left and right imaging sensors, allowing depth sensing as well as standard image capture.
* A 9-Axis Inertial Measurement Unit (or *IMU*) on-board the OpenCR Micro Controller board, which uses an accelerometer, gyroscope and magnetometer to measure the robot's specific force, acceleration and orientation. 
* Encoders in each of the DYNAMIXEL wheel motors, allowing measurement of speed and rotation count for each of the wheels.

### Software

Our robots (currently) run [ROS 2 Humble Hawksbill](https://docs.ros.org/en/humble/index.html) (or *"Humble"* for short). The courses here are therefore based around this version of ROS. The easiest way to install ROS is via Deb packages for Ubuntu Jammy (22.04). This is the setup we recommend and - as such - all out robotics hardware runs with this OS/Software setup.

[You can find out more about installing ROS on your own system here (TODO)]().

## Other Tech

### Laptops

In the Diamond, we have dedicated Robot Laptops running the same OS & ROS version as above. We use these when working with the robots in the lab. [See here for more details (TODO)](). 

### Simulation Environment

To deliver the simulation-based parts of this course, we've created a custom simulation environment using the [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/). This has been developed primarily to run on University of Sheffield Managed Desktop Computers, which run Windows 10, but it's also possible to run this on other machines too. We call this simulation environment *"WSL-ROS"*. [See here for more details (TODO)]().

<!-- 
TODO:
  - Acknowledgements??
  - Version History?? -->