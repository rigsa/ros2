---
title: Installing ROS 2 Using Docker (Linux & Mac)
---

**Applicable to**: Linux and Mac Users

## Acknowledgments

This solution has been put together by Atri Hegde, a COM2009 student from 2024 (and a course demonstrator in 2025!)

**Thanks Atri**!!

## Setup

See here for the `docker-ros2` repo and the instructions on how to install it: 

<center>[https://github.com/hegde-atri/ros2-docker](https://github.com/hegde-atri/ros2-docker){target="_blank"}</center>

## Launching the ROS Environment {#launch}

### Mac & Linux

Instructions on how to launch the ROS2 docker container are provided [in the README](https://github.com/hegde-atri/ros2-docker?tab=readme-ov-file#ros2-humble-development-container){target="_blank"}, so please consult this for all the details. Essentially though (*if you're on a Mac or Linux machine*) then you first need to fire up the docker container using:

```bash
ros_start
```

... and once that's done, you need to run the following command to enter the ROS2 environment:

```bash
ros_shell
```

The above assumes that you have already set up your shell appropriately (again [see the README](https://github.com/hegde-atri/ros2-docker?tab=readme-ov-file#ros2-humble-development-container){target="_blank"}).
