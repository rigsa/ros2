---  
title: "Task 2: Avoiding Obstacles" 
---  

Develop the ROS node(s) to allow a real TurtleBot3 Waffle to autonomously explore an environment containing various obstacles. The robot must explore as much of the environment as possible in 90 seconds without crashing into anything!

!!! success "Assignment #1 Checkpoints"
    
    The following parts of [The ROS 2 Course](../../assignment1.md) to support your work on this task (in addition to the suggestions for Task 1): 

    * [ ] **Part 3**: in full.
    * [ ] **Part 5**: in full.

    <!-- TODO: **See Also**:     -->
    <!-- * Real Waffle Out of Range LiDAR Data? -->

## Summary

Assignment #1 Part 3 introduces [the Waffle's LiDAR sensor](../../../course/part3.md#lidar). This sensor is very useful, as it tells us the distance to any objects that are present in the robot's environment. In [Assignment #1 Part 5](../../../course/part5.md#explore) we look at how this data, in combination with the *ROS Action framework*, can be used as the basis for a basic exploration strategy that would incorporate obstacle avoidance. Building on this in [Part 5 Exercise 6](../../../course/part5.md#ex6), we discuss how this could be developed further by developing an action *client* that could make successive calls to the action server to keep the robot moving randomly, and indefinitely, around an arena whilst avoiding obstacles.

This is one approach that you could use for this task, but there are other (and potentially simpler) ways that this could be achieved too. 

In COM2009 Lecture 3 ("Sensing, Actuation & Control"), for instance, you are introduced to *Cybernetic Control Principles* and some of *Braitenberg's "Vehicles,"* which are discussed and implemented on a Lego robot during the lecture! In particular, *"Vehicle 3b"* might well be relevant to consider as a simple method to achieve an obstacle avoidance behaviour.

Another aspect of this task is *exploration*: your robot will be awarded more marks for navigating around more of the environment. Consider the search strategies that are discussed in Lecture 8 ("Local Guidance Strategies"), such as *"Brownian Motion"* and *"Levy Walks."* Could something along these lines be implemented on the 
Waffle?

## Details

The Diamond Computer Room 5 Robot Arena is a square arena of 4x4m. For the task, the arena will contain a number of *"obstacles,"* i.e.: short wooden walls and coloured cylinders. Your robot will need to be able to detect these obstacles and navigate around them in order to fully explore the space.

Exploration marks will be awarded when the robot enters each of the 12 outer arena zones (each a 1x1m square), as shown below.

<a name="cr5-layout"></a>
<figure markdown>
  ![](../figures/task2_arena_layout.png){width=600px}
  <figcaption>The DIA-CR5 Robot Arena layout for Task 2.</figcaption>
</figure>

<a name="env-vars"></a>

!!! danger "Important"
    This is an *example* of what the environment *might* look like:
    
    * **ALL** objects (i.e. the four coloured cylinders and the four wall assemblies) could be in *different positions entirely*. 
    * The wooden walls *may not be touching the outer edges of the arena*!
    * The coloured cylinders *could* be inside exploration zones. 
    * The only things that will remain the same are the arena size, the presence of the outer arena walls and the floor layout (i.e. the location of all the zones).

1. The robot will start in the centre of the arena, perpendicular to one of the four outer walls.
1. It must explore the environment for 90 seconds without touching **any** of the arena walls or the obstacles within it.

    **Note**: *The 90-second timer will start as soon as the robot starts moving within the arena.*

1. If the robot makes contact with **anything** before the time has elapsed then the attempt is over, and this time will be recorded to determine a *"Run Time"* mark ([see below](#run-time)).
1. As shown above, the arena floor will be marked with 12 equal-sized (1x1m) zones and the robot must enter as many of these 12 **exploration zones** as possible during the attempt.
1. The robot must be moving for the entire duration of the task. Simply just turning on the spot for the whole time doesn't count!

    * What we want to see here is that the robot is constantly making an effort to explore.
    * It is however OK for the robot to stop moving and turn on the spot for a few seconds whenever required though.
    * If the robot explores for a while and then stops and doesn't move again for the remainder of the 90-second run, then *Run Time* marks will be awarded up to the point at which the robot ceases to be active.
    * Further details on the eligibility for *Run Time* marks are provided in [the Marking Section below](#marking).

## Executing Your Code {#launch}

When assessing your code for this task, the teaching team will use the following command to execute all the necessary functionality from within your team's ROS 2 package:

```bash
ros2 launch com2009_teamXX_2026 task2.launch.py
```

... where `XX` will be replaced with *your team number*.

As such, the ROS 2 package that your team submit must contain a launch file called `task2.launch.py`, to execute all the necessary functionality from within your package for this task.

!!! note
    ROS will already be running on the robot before we attempt to execute your launch file, and [a *Zenoh Session* will be running on the laptop, to allow nodes running on the laptop to communicate with it](../../../waffles/launching-ros.md#step4).

## Marking

There are **20 marks** available for Task 2 in total, awarded as follows:

<center>

| Criteria | Marks | Details |
| :--- | :---: | :--- |
| **A**: Run Time | 8/20 | You will be awarded marks for the amount of time that your robot spends exploring the environment before 90 seconds has elapsed, **or** until the robot makes contact with anything in its environment for the first time ([as per the table below](#run-time)). **The robot must leave the centre zone** (a 1x1m box, denoted in red [in the figure above](#cr5-layout)) in order to be eligible for any of these marks. If the robot does not explore beyond **the "partial exploration" zone** (denoted orange in the figure) then a $0.5\times$ multiplication factor will be applied to the run time marks. |
| **B**: Exploration | 12/20 | You will be awarded 1 mark for each of the 12 exploration zones that the robot manages to enter. The robot only needs to enter each of the 12 zones once, but its full body must be inside the zone marking to be awarded the mark. |

</center>

### Criterion A: Run Time {#run-time}

**Marks:** 8/20

Marks will be awarded as follows:

<center>

| Time (Seconds) | Marks |
| :---: | :---: |
| 0-9 | 0 |
| 10-19 | 1 |
| 20-29 | 2 |
| 30-39 | 3 |
| 40-49 | 4 |
| 50-59 | 5 |
| 60-89 | 6 |
| The full 90! | 8 |

</center>

## Simulation Resources

Within the `tuos_task_sims` package there is an example arena that can be used to develop and test out your team's obstacle avoidance node(s) for this task[^update-course-repo]. [As above](#env-vars) however, this is just an *example* of what the real-world environment *might* look like. 

[^update-course-repo]: Make sure you [check for updates to the Course Repo](../../../course/extras/course-repo.md#updating) to ensure that you have the most up-to-date version of these simulations.

The simulation can be launched using the following `ros2 launch` command:

```bash
ros2 launch tuos_task_sims obstacle_avoidance.launch.py
```

<figure markdown>
  ![](../figures/task2.png)
  <figcaption>A simulation environment to represent the real DIA-CR5 arena layout for Task 2.</figcaption>
</figure>

!!! warning "Real World vs. Sim"

    Remember: **just because it works in simulation ^^DOESN'T^^ mean it will work in the real world**!

    Make sure you test things out ^^thoroughly^^ on the real robots during the lab sessions.
    