---  
title: Essential Considerations 
---

Sometimes, the real robots behave in ways that you wouldn't expect. Certain things work differently on the real hardware than they do in a simulation. On this page, we highlight a number of *key things that you should investigate at your earliest convenience*, in order to avoid any nasty surprises in the lab.

## Motion and Velocity Control

1. **What happens if you don't tell a robot explicitly to stop moving?**

    This is no different in the real-world as it is in a simulation, but consider what we had to do **[in this Exercise](./basics.md#exSimpleVelCtrl)** to make the robot stop, and why it's therefore important to [build nodes with proper shutdown procedures in place](../course/part2.md#ex5). 

1. **What are the robot's maximum velocity limits, and what happens if you exceed them?**

    Physical systems have their limits, and no motor can rotate at an unlimited speed! [Our robots therefore have maximum velocity limits](../about/robots.md#max_vels), and it is important that you know what these are. Try issuing a velocity command to a robot that is outside the maximum velocity range... what does the robot do? 

1. **What happens if you apply high angular and linear velocity to a robot instantaneously, from a standstill?**

    It is perfectly feasible for our robots to achieve their maximum velocities, however, they don't necessarily appreciate being asked to go from stationary to full speed instantaneously! Consider testing this out on a real robot to observe what happens. With the robot stationary, **[use the command line](../course/part2.md#ex3)** to publish a velocity command to the robot that contains both a *high* linear *and* angular velocity component. What would you *expect* to observe?[^hint-circle] ... What you *actually* observe might be different. How could you achieve the desired motion (assuming the velocities are within the maximum limits)

    [^hint-circle]: The robot *should* turn in a circle, but if the velocities are close to the maximum limits, does this actually happen?

## Laser Displacement Readings and the LiDAR Sensor 

1. **What are the minimum and maximum distances that the robot's LiDAR sensor can detect?**

    You can use **[the same process as in simulation](../course/part3.md#range_max_min)** to determine this.

    If our robot arena is 4x4 meters in size, *is it likely that the robot would ever encounter readings outside this range?* 

1. **What does the sensor report when these limits are exceeded, and how does this differ to a simulation?**

    The LiDAR gives us an accurate measure of the distance to obstacles within the robot's environment, provided those obstacles are within the sensor's measurement range (as above). If obstacles are beyond the sensor's measurement range, then an *out-of-range* value is returned by the sensor instead. In our code it's important that we **[detect these *out-of-range* values and discard them](../course/part3/lidar_subscriber.md)**, as if we don't deal with them correctly then this can influence our robot's ability to detect and avoid obstacles effectively. In simulation, the out-of-range value is `inf`, but is this the same on the real robots?[^hint-lidar]

    [^hint-lidar]: On the real robots, the out-of-range value is **NOT** `inf`, so you need to find out what it is! 

1. **The data from a real LiDAR sensor will be "noisy." What are the implications of this for real-world applications?**

    You may notice if you **[observe the data from a robot's LiDAR sensor in RViz](./basics.md#exViz)** that the green dots move around quite a lot, even when the robot isn't moving, or if nothing in the environment is actually changing. This is called *"measurement noise"*, and it is common to all sensors. It's important then to consider the processing that you perform on this data: say you want to determine the distance to the closest thing in your robot's environment, so perhaps you might consider applying a `min()` function to determine this? This will be very sensitive to measurement noise however: minimum values may not always represent genuine distance measurements. Are there alternative ways that you could handle this data instead?

## The Camera and Image Processing

1. **What topic is image data published to on the real robots? Is this the same as in a simulation?**

    With the real robot to hand, use ROS command-line tools such as `ros2 topic list` and `ros2 topic info` to interrogate the ROS Network and identify the name of the camera image topic used on the real robots. *Is it the same, or different?*

1. **What is the resolution of the images obtained from a real robot's camera?**

    Having confirmed the name of the camera image topic (as above), use **[the methods discussed here](../course/part6.md#camera-topics-and-data)** to identify the resolution of the images that are being published. It's important to know this, particularly when it comes to applying any cropping to your raw images: if you don't know how big (or small) the images are to begin with, you may end up chopping off more (or less) than you bargained for. 

1. **Do the same image processing techniques produce the same results in simulation and the real world?**

    In general, image detection gets a little more challenging in the real-world, where the same object might appear (to a robot's camera) to have slightly different colour tones under different light conditions, from different angles, in different levels of shade, etc. In simulation, you may **[build an extremely effective `colour_search.py` node](../course/part6.md#ex3)** to detect each of the four coloured pillars in a simulated world, but this might not perform as well in the real world without some fine-tuning. It's therefore really important to **always** test out your code in the real-world; just because it works in simulation, **doesn't** mean it will work on the real robots!!

## Summary

You will naturally do a fair bit of development work in simulation throughout this course, where it's easier to test things out and less disastrous if things go wrong! Overall, you'll be able to develop things much faster this way, and you can do this outside of your weekly lab sessions too. Whilst you're doing this though, keep in mind all the differences that we have identified above, so that there are less nasty surprises when you come to deploy your ROS applications in the real world. 
