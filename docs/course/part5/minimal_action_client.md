---  
title: A Minimal Action Client
---

## The Code

Review the code (including the annotations) and then take a copy of it.

```py title="camera_sweep_action_client.py"
--8<-- "code_templates/camera_sweep_action_client.py"
```

1. As you know by now, in order to develop ROS nodes using Python we need to import the `rclpy` client library, and the `Node` class to base our node upon. In addition, here we're also importing an `ActionClient` class too.  

2. We know that the `/camera_sweep` Action server uses the `CameraSweep` `action` interface from the `tuos_interfaces` package, so we import that here too (which we use to make a call to the server). 

3. Standard practice when we initialise ROS nodes: *we must give them a name*

4. Here, we instantiate an `ActionClient` class object. In doing this we define the `node` to add the action client too (in our case `self`, i.e. our `CameraSweepActionClient` class). We then also define the interface type used by the server (`CameraSweep`), and the name of the action that we want to call (`action_name="camera_sweep"`).

5. Here we define a class method to construct and deliver a goal to the server. 

    As we know from earlier, a `CameraSweep.Goal()` contains two parameters that we can assign values to: `sweep_angle` and `image_count`.

    The goal is sent to the server using the `send_goal_async()` method, which returns a *future*: i.e. something that will happen in the future, that we can wait on. This future is returned once the goal parameters have been accepted by the server, *not* when the action server has actually completed its job.

    !!! tip
        Both goal parameters are set to `0` by default!

6. In our `main` method we initialise `rclpy` and our `CameraSweepActionClient` class (nothing new here), but then we call the `send_goal()` method of our class (as discussed above), which returns a *future*. We can then use the `rclpy.spin_until_future_complete()` method to spin up our node *only* until this future object has finished.

    !!! warning 
        When the `send_goal()` method is called, no additional arguments are provided, which means *default values* will be applied... which were defined above!


!!! warning "Fill in the blanks!"
    You need to adapt the code so that a valid goal is actually sent to the server! 

## Package Dependencies

The action client has *two key dependencies*, so we need to modify the `package.xml` file (below the `#!xml <exec_depend>rclpy</exec_depend>` line) to include these:

```xml title="package.xml"
<exec_depend>action_msgs</exec_depend>
<exec_depend>tuos_interfaces</exec_depend>
``` 
