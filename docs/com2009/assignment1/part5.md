---  
title: "Part 5: ROS Actions"  
description: Building on what we understand about ROS Services now, here we will look at ROS Actions, which are similar to Services, but with a few key benefits.
---

<!-- 

launching tmux with a config file (for a four pane window):

tmux new-session -s SESSION "tmux source-file ~/tmux.conf"

- change SESSION name accordingly
- tmux.conf:

new
neww
splitw -v
splitw -h
select-pane -t 0
splitw -h
select-pane -t 0
set -g mouse

 -->

## Introduction

:material-pen: **Exercises**: 4 essential (plus 2 *advanced* exercises)  
:material-timer: **Estimated Completion Time**: 3 hours (for the essential exercises only)

### Aims

In this part of the course we'll learn about a third method of communication available in ROS: *Actions*.  Actions are essentially an advanced version of Services, and we'll look at exactly how these two differ and why you might choose to employ an action over a service for certain tasks. 

### Intended Learning Outcomes

By the end of this session you will be able to:

1. Recognise how ROS Actions differ from ROS Services and explain where this method might be useful in robot applications.
1. Explain the structure of Action messages and identify the relevant information within them, enabling you to build Action Servers and Clients.
1. Implement Python Action *Client* nodes that utilise *concurrency* and *preemption*.
1. Develop Action Server & Client nodes that could be used as the basis for a robotic search strategy.

### Quick Links

<!-- * [Exercise 1: Launching an Action Server and calling it from the command-line](#ex1)
* [Exercise 2: Building a Python Action Client Node with concurrency](#ex2)
* [Exercise 3: Building a Preemptive Python Action Client Node](#ex3)
* [Exercise 4: Developing an "Obstacle Avoidance" behaviour using an Action Server](#ex4)
* **Advanced (optional) exercises**:
    * [Advanced Exercise 1: Implementing a Search strategy](#adv_ex1)
    * [Advanced Exercise 2: Autonomous Navigation using waypoint markers](#adv_ex2) -->

### Additional Resources

<!-- * [The Action Client Code (for Exercise 2)](./part5/action_client.md)
* [The Preemptive Action Client Code (for Exercise 3)](./part5/preemptive_action_client.md) -->

## Getting Started

**Step 1: Launch your ROS Environment**

Launch your ROS environment now so that you have access to a Linux terminal instance (aka **TERMINAL 1**).

**Step 2: Restore your work (WSL-ROS Managed Desktop Users ONLY)**

Remember that any work that you do within the WSL-ROS Environment will not be preserved between sessions or across different University computers, and so you should be backing up your work to your `U:\` drive regularly. When prompted (on first launch of WSL-ROS in **TERMINAL 1**) enter `Y` to restore this[^1].

[^1]: Remember: you can also use the `wsl_ros restore` command at any time.

**Step 3: Launch VS Code**  

*WSL users* [remember to check for this (TODO)](). <!-- (../../software/on-campus/vscode.md#verify) -->

**Step 4: Make Sure The Course Repo is Up-To-Date**

Check that the Course Repo is up-to-date before you start on these exercises. [See here for how to install and/or update (TODO)](). <!-- (../../extras/tuos-ros.md).-->

## Calling an Action Server

Before we talk about what actions actually are, we're going to dive straight in and see one in *action* (excuse the pun). 

<!-- As you may remember from Part 3, you actually used a ROS Action to make your robot navigate autonomously in [Exercise 3](./part3.md#ex3), by calling an action server from the command-line. We will do a similar thing now, in a different context, and this time we'll also look at what's going on in a bit more detail. -->

#### :material-pen: Exercise 1: Launching an Action Server and calling it from the command-line {#ex1}

We'll play a little game here. We're going to launch our TurtleBot3 Waffle in a *mystery environment* now, and we're going to do this by launching Gazebo *headless* i.e. Gazebo will be running behind the scenes, but there'll be no Graphical User Interface (GUI) to show us what the environment actually looks like.  Then, we'll use an *action server* to make our robot scan the environment and take pictures for us, to reveal its surroundings!

1. To launch the TurtleBot3 Waffle in this *mystery environment*, use the following `ros2 launch` command:

    ***
    **TERMINAL 1:**
    ```bash
    ros2 launch tuos_simulations mystery_world.launch.py
    ```
    ***

    Messages in the terminal should indicate that *something* has happened, but that's about all you will see!

1. Next, open up a new terminal (**TERMINAL 2**), and have a look at all the topics that are currently active on the ROS network (you should know exactly how to do this by now!)

    The output of this should confirm that ROS and our robot are indeed active...

    ??? question "How?"
        When the robot is active, the output of the `ros2 topic list` command should provide a long list of topics, a number of which we've been working with throughout this course so far, such as `cmd_vel`, `odom`, `scan`, and so on. If the Waffle simulation *isn't* active then we would be presented with a much smaller list, containing only the core ROS topics:

        ***
        **TERMINAL 2:**
        ``` { .bash .no-copy }
        $ ros2 topic list
        /parameter_events
        /rosout
        ```
        ***

1. Next, run the following command to launch an *Action Server* on the network:

    ***
    **TERMINAL 2:**
    ```bash
    ros2 run tuos_examples camera_sweep_action_server.py
    ```
    ***

1. Now, open up *another* new terminal instance (**TERMINAL 3**), but so that you can view this and **TERMINAL 2** side-by-side. Enter the following command to *list* all actions that are active on the ROS network:

    ***
    **TERMINAL 3:**
    ```bash
    ros2 action list
    ```

    There should be an item here called `/camera_sweep`, use the `info` command to find out more about this:

    ```bash
    ros2 action info /camera_sweep
    ```

    This tells us the *name* of the action: `Action: /camera_sweep`, as well as the number of client and server nodes this action has. Currently, the action should have 0 *clients* and 1 *server*, and the node acting as the server here should be listed as `/camera_sweep_action_server_node` (the node that we just launched with the `ros2 run` command in **TERMINAL 2**).
    
    Finally, call the `ros2 action info` command again, but this time providing an additional argument:
    
    ```
    ros2 action info -t /camera_sweep
    ```

    ```
    Action: /camera_sweep
    Action clients: 0
    Action servers: 1
        /camera_sweep_action_server [tuos_interfaces/action/CameraSweep]
    ```

    The `-t` argument additionally shows the action *type* against the server node, indicating to us the type of *interface* used by the server.
    ***

1. Let's now find out more about the interface itself. As with any interface (message, service or action) we can use the `ros2 interface` command to do this.

    ***
    **TERMINAL 3:**
    ```bash
    ros2 interface show tuos_interfaces/action/CameraSweep
    ```
    
    Which should present us with the following:

    ``` { .txt .no-copy }
    #goal
    float32 sweep_angle    # the angular sweep (in degrees) over which to capture images
    int32 image_count      # the number of images to capture during the sweep
    ---
    #result
    string image_path      # The filesystem location of the captured images
    ---
    #feedback
    int32 current_image    # the number of images taken
    float32 current_angle  # the current angular position of the robot (in degrees)
    ```
    ***

    There are three parts to an action interface, and we'll talk about these in a bit more detail later on, but for now, all we need to know is that in order to *call* an action, we need to send the action server a **Goal**.

    ??? info "Comparing with ROS Services"
        This is a bit like sending a **Request** to a ROS Service Server, like we did in the previous session.
    
1. We can issue a goal to an action server from the command-line using the `ros2 action` command again. Let's give this a go in **TERMINAL 3**.
    
    First, let's identify the right `ros2 action` sub-command:

    ***
    **TERMINAL 3:**
    ```bash
    ros2 action --help
    ```

    ``` { .txt .no-copy}
    Commands:
      info       Print information about an action
      list       Output a list of action names
      send_goal  Send an action goal
    ```

    As above, there are three sub-commands to choose from, and we've already used the first two! Clearly, the `send_goal` command is the one we want now.

    Let's get some help on this one:

    ```bash
    ros2 action send_goal --help
    ```
    
    From this, we learn that there are three *positional arguments*, which must be supplied in the correct order:
    
    ``` { .bash .no-copy }
    ros2 action send_goal action_name action_type goal
    ```

    We know from our earlier interrogation with the `ros2 action list`, `info` and `ros2 interface show` commands how to provide the right data here:
    
    1. `action_name`: `/camera_sweep`
    1. `action_type`: `tuos_interfaces/action/CameraSweep`
    1. `goal`: a data packet (in YAML format) containing two parameters:
        1. `sweep_angle`: the angle (in degrees) that the robot will rotate on the spot (i.e. 'sweep')
        1. `image_count`: the number of images it will capture from its front-facing camera while 'sweeping'
    
    ***

1. Now, again in **TERMINAL 3**, have a go at using the `ros2 action send_goal` command, but keep an eye on **TERMINAL 2** as you do this:

    ***
    **TERMINAL 3:**
    ``` { .bash .no-copy }
    ros2 action send_goal /camera_sweep tuos_interfaces/action/CameraSweep "{sweep_angle: 0, image_count: 0}"
    ```
    ***

    Having called the action, you should then be presented with a message (in **TERMINAL 3**) that the `Goal was rejected.` In **TERMINAL 2** (where the action server is running), we should see some additional information about why this was the case. Read this, and then head back to **TERMINAL 3** and have another go at sending a goal to the action server, by supplying valid inputs this time!

    Once valid goal parameters have been supplied, the action server (in **TERMINAL 2**), will respond to inform you of what it's going to do. You'll then need to wait for it to do its job...

1. Once the action has completed (it could up to 20 seconds), a message should appear in **TERMINAL 3** to inform us of the outcome:
        
    ***
    **TERMINAL 3:**
    ``` { .txt .no-copy }
    Result:
        image_path: ~/myrosdata/action_examples/YYYYMMDD_hhmmss

    Goal finished with status: SUCCEEDED
    ```
    ***

    Additionally, we should see some further text in **TERMINAL 2** as well:

    ***
    **TERMINAL 2:**
    ``` { .txt .no-copy }
    [INFO] [#####] [camera_sweep_action_server]: camera_sweep_action_server completed successfully:
      - Angular sweep = # degrees
      - Images captured = #
      - Time taken = # seconds
    ```
    ***

    1. The *result* of the action (presented to us in **TERMINAL 3**) is a file path. Navigate to this directory in **TERMINAL 3** (using `cd`) and have a look at the content using `ll` (a handy alias for the `ls` command):
            
        You should see the same number of image files in there as was requested with the `image_count` parameter.
    
    1. Launch `eog` in this directory and click through all the images to reveal your robot's *mystery environment*:

        ***
        **TERMINAL 3:**
        ```bash
        eog .
        ```
        ***

1. Let's do this one more time. Close down the `eog` window, head back to **TERMINAL 3** and issue the `ros2 action send_goal` command again, but this time use the optional `-f` flag:

    ***
    **TERMINAL 3:**
    ```bash
    ros2 action send_goal -f /camera_sweep tuos_interfaces/action/CameraSweep "{sweep_angle: 0, image_count: 0}" 
    ```
    ***

    !!! tip
        Don't forget to supply valid goal parameters again!

    *Now*, as well as being provided with a result once the action has completed, we're *also* provided with some regular updates while the action is in progress (aka *"feedback"*)! 

1. To finish off, close down the action server in **TERMINAL 2** and the headless Gazebo process in **TERMINAL 1** by entering ++ctrl+c++ in each terminal. 

## What is a ROS Action?

In this Exercise we launched an action server and then called it from the command-line using the `ros2 action send_goal` sub-command. Using the `-f` flag we were able to ask the server to provide us with *real-time feedback* on how it was getting on (in **TERMINAL 3**). In the same way as a ROS Service, the action also provided us with a **result** once the task had been completed. **Feedback** is one of the key features that differentiates a ROS Action from a ROS Service: An Action Server provides **feedback** messages at regular intervals whilst performing an action and working towards its **goal**. Another feature of ROS Actions is that they can be *cancelled* part-way through (which we'll play around with shortly).

Ultimately, Actions use a combination of both Topic- *and* Service-based communication, to create a more advanced messaging protocol. Due to the provision of *feedback* and the ability to *cancel* a process part-way through, Actions are designed to be used for **longer running tasks**. You can read more about Actions in [the official ROS 2 documentation here](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html) (which also includes a nice animation to explain how they work).

### The Format of Action Interfaces

Like Services, Action Interfaces have multiple parts to them, and we need to know what format these action messages take in order to be able to use them.

We ran `ros2 interface show` in the previous exercise, to interrogate the action interface used by the `/camera_sweep` action server:

``` { .txt .no-copy }
$ ros2 interface show tuos_interfaces/action/CameraSweep

#goal
float32 sweep_angle    # the angular sweep (in degrees) over which to capture images
int32 image_count      # the number of images to capture during the sweep
---
#result
string image_path      # The filesystem location of the captured images
---
#feedback
int32 current_image    # the number of images taken
float32 current_angle  # the current angular position of the robot (in degrees)
```

As we know from Exercise 1, in order to call this action server, we need to send a **goal**, and (as we know from Exercise 1) there are **two** goal parameters that must be provided:

1. `sweep_angle`: a 32-bit floating-point value
1. `image_count`: a 32-bit integer

!!! question "Questions"
    * What are the names of the **result** and **feedback** interface parameters? (There are three in total.)
    * What data types do these parameters use?

You'll learn how we use this information to develop Python Action Server & Client nodes in the following exercises.

### Creating Python Action Clients

In the previous exercise we *called* a pre-existing Action Server from the command-line, by sending a goal to it. Let's look at how we can do this from within a Python ROS node now.

#### :material-pen: Exercise 2: Building a Python Action Client Node {#ex2}

1. In **TERMINAL 1** launch the *mystery world* simulation again, but this time with an additional argument:

    ***
    **TERMINAL 1:**
    ```bash
    ros2 launch tuos_simulations mystery_world.launch.py with_gui:=true
    ```
    ***

    Which will launch Gazebo in full now, with the GUI attached.

1. Then, in **TERMINAL 2**, launch the Camera Sweep Action Server again: 

    ***
    **TERMINAL 2:**
    ```bash
    ros2 run tuos_examples camera_sweep_action_server.py
    ```
    ***

##### Part 1: A Minimal Action Client

1. Now, in **TERMINAL 3**, create a new package called `part5_actions` using the `create_pkg.sh` helper script from the `tuos_ros` course repo ([return here for a reminder on how to do this](part1.md#ex4)).

1. Navigate into the `scripts` folder of your package using the `cd` command:

    ```bash
    cd ~/ros2_ws/src/part5_actions/scripts/
    ```

1. In here, create a new Python file called `camera_sweep_action_client.py` (using the `touch` command) and make it executable ([using `chmod`](./part1.md#chmod)). 

1. Then, declare this as an executable in the package's `CMakeLists.txt`:

    ```txt title="CMakeLists.txt"
    # Install Python executables
    install(PROGRAMS
      scripts/camera_sweep_action_client.py
      DESTINATION lib/${PROJECT_NAME}
    )
    ```

1. At an *absolute minimum*, the Action Client can be constructed as follows:

    ```py title="camera_sweep_action_client.py"
    --8<-- "code_templates/camera_sweep_action_client.py"
    ```

    1. As you know by now, in order to develop ROS nodes using Python we need to import the `rclpy` client library, and the `Node` class to base our node upon. In addition, here we're also importing an `ActionClient` class too.  

    2. We know that the `/camera_sweep` Action server uses the `CameraSweep` `action` interface from the `tuos_interfaces` package, so we import that here too (which we use to make a call to the server). 

    3. Standard practice when we initialise ROS nodes: *we must give them a name*
    
    4. Here, we instantiate an `ActionClient` class object. In doing this we define the `node` to add the action client too (in our case `self`, i.e. our `CameraSweepActionClient` class). We then also define the interface type used by the server (`CameraSweep`), and the name of the action that we want to call (`action_name="camera_sweep"`).

    5. Here we define a class method to construct and deliver a goal to the server. 

        As we know from earlier, a `CameraSweep.Goal()` contains two parameters that we can assign values to: `sweep_angle` and `image_count`.

        The goal is sent to the server using the `send_goal_async()` method, which returns a *future*: i.e. something that will happen in the future, that we can wait on.

        !!! tip
            Both goal parameters are set to `0` by default!

    6. In our `main` method we initialise `rclpy` and our `CameraSweepActionClient` class (nothing new here), but then we call the `send_goal()` method of our class (as discussed above), which returns a *future*. We can then use the `rclpy.spin_until_future_complete()` method to spin up our node *only* until this future object has finished.

        !!! warning 
            When the `send_goal()` method is called, no additional arguments are provided, which means *default values* will be applied... which were defined above!

1. Let's build the Node now, so that we can run it. Head back to **TERMINAL 3** and use Colcon to build the package: <a name="colcon"></a>

    ```bash
    cd ~/ros2_ws/ && colcon build --packages-select part5_actions --symlink-install
    ```

1. Re-source the `.bashrc`:

    ```bash
    source ~/.bashrc
    ```

1. Run your node with `ros2 run`...

    As you have hopefully just observed, the node that we've created here makes a call to the action server, waits for the action to take place and then stops. The only way that you'd know what was happening however, is if you keep an eye on **TERMINAL 2**, to see the action *server* respond to the goal that it was sent... The client itself provides no feedback during the action, nor the result at the end. Let's look to incorporate that now...

##### Part 2: Handling a Result

1. Go back to the `camera_sweep_action_client.py` file in VS Code.

1. In order to be able to handle the result that is sent from an action server, we first need to handle the response that the server sends to the goal itself.

    Within the `send_goal()` method of the `CameraSweepActionClient()` class, find the line that reads:

    ```py
    return self.actionclient.send_goal_async(goal)
    ```

    and change this to:

    ```py
    self.send_goal_future = self.actionclient.send_goal_async(goal)
    self.send_goal_future.add_done_callback(self.goal_response_callback)
    ```

    This method is no longer returning the *future* that is sent from `send_goal_async()`, but is now handling this and adding a callback to it: `goal_response_callback`. This callback will be executed to inform the client of whether the server has *accepted* the goal or not.

1. Define this as a *new* class method of the `CameraSweepActionClient()` class (i.e. underneath the `send_goal()` class method that has already been defined)...

    ```py
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn("The goal was rejected by the server.")
            return

        self.get_logger().info("The goal was accepted by the server.")

        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.get_result_callback)
    ```

    The *input* to this method will be the *future* that is created by the `send_goal_async()` call. We assign this to `goal_handle` here, and can then use this for two purposes:

    1. To check whether the goal that we sent was accepted by the server
    1. If it *was* accepted, then we can get the result (using `get_result_async()`) and we can attach another callback to this to actually process that result: `get_result_callback`.

1. Now, define *this* as another new method of the `CameraSweepActionClient()` class (i.e. underneath the `goal_response_callback()` class method that we have just defined)...

    ```py
    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(
            f"The action has completed.\n"
            f"Result:\n"
            f"  - Image Path = {result.image_path}"
        )
        rclpy.shutdown()
    ``` 

    The input to *this* class method is another future object which contains the actual result sent from the server. We assign this to `result` and use a `get_logger().info()` call to print this to the terminal when the action has finished.

    As we know from our work earlier, the `CameraSweep` interface contains one `result` parameter called `image_path`.

1. Finally, in the `main` method, change this:

    ```py
    rclpy.spin_until_future_complete(action_client, future)
    ```

    to this:

    ```py
    rclpy.spin(action_client)
    ```

1. Save all your changes!

1. Run this node again now (with the `ros2 run` command) and observe the changes in action.

    Our client node now presents us with the *result* that is sent by the server on completion of the action, but wouldn't it be nice if we could see the real-time *feedback* as the action takes place? Let's add this in now...

##### Part 3: Handling Feedback

1. Go back to the `camera_sweep_action_client.py` file in VS Code.

1. In order to be able to handle the feedback that is sent from an action server, we need to add yet another callback! Go back to the `send_goal()` method and the line where we are actually sending the goal to the server:

    ```py
    self.send_goal_future = self.actionclient.send_goal_async(goal)
    ```

    As it stands, all we're doing here is sending the goal, but we can also add a *feedback callback* to this too:

    ```py
    self.send_goal_future = self.actionclient.send_goal_async(
            goal=goal, 
            feedback_callback=self.feedback_callback
        )
    ```

    The `feedback_callback` will be executed every time a new feedback message is received from the server.

1. In order to define what we want to do with these feedback messages we need to define this *yet another* new method of the `CameraSweepActionClient()` class. Underneath the `get_result_callback()` class method that we defined earlier, add this new one as well:

    ```py
    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        fdbk_current_angle = feedback.current_angle
        fdbk_current_image = feedback.current_image
        self.get_logger().info(
            f"\nFEEDBACK:\n"
            f"  - Current angular position = {fdbk_current_angle:.1f} degrees.\n"
            f"  - Image(s) captured so far = {fdbk_current_image}."
        )
    ``` 

    As we know from our work earlier, the `CameraSweep` interface contains two *feedback* parameters: `fdbk_current_angle` and `fdbk_current_image`.

1. Save all your changes once again, run the node again with the `ros2 run` command and observe the changes in action.

    The node we've now built can send a *goal* to an action server, process the *feedback* sent form the server as the action is in progress, and present the *result* to us once everything is complete.
    
    As discussed earlier though, the *other* key feature of Actions is the ability to *cancel* them part-way through. So let's look at how to incorporate this now as well.

##### Part 4: Cancelling an Action

1. First, create a copy of your `camera_sweep_action_client.py` node and call it `camera_sweep_action_client_cancel.py` (make sure you're still in the `scripts` directory of your `part5_actions` package before you run this command):

    ***
    **TERMINAL 3:**
    ```bash
    cp camera_sweep_action_client.py camera_sweep_action_client_cancel.py
    ```
    ***

1. Don't forget to declare this as an *additional* executable in the package's `CMakeLists.txt`. You'll then also need to re-build the package with `colcon build` ([go back for a reminder](#colcon)).

1. Open the `camera_sweep_action_client_cancel.py` file in VS Code.

1. We want this client to be able to cancel the goal under two different circumstances:

    1. The client itself is shutdown by the user (via a ++ctrl+c++ in the terminal)
    1. A conditional event that happens as the action is underway.

    In order to address item 1 first, we need to draw upon some of the work we did in Part 2 in [the implementation of *safe shutdown procedures*](part2.md#ex5)...

1. As you hopefully recall, we first need to import `SignalHandlerOptions` into our node, so add this as an additional import at the start of the code:

    ```py
    from rclpy.signals import SignalHandlerOptions
    ```

    Then, in the `main()` node function, modify the `#!py rclpy.init()` call:

    ```py
    rclpy.init(
        args=args,
        signal_handler_options=SignalHandlerOptions.NO
    )
    ```

1. Inside the `#!py __init__()` method of our `CameraSweepActionClient()` class we now need to add some additional flags:

    ```py
    self.goal_succeeded = False
    self.goal_cancelled = False
    self.stop = False
    ```

    In the `get_result_callback()` class method, we can then ensure that the `self.goal_succeeded` flag is sent to `True` when a result is received. In this class methods, locate the `#!py rclpy.shutdown()` line and add the following *additional* line just above it:

    ```py
    self.goal_succeeded = True
    ```

1. Actions can be cancelled using a `cancel_goal_async()` method of the `goal_handle` that is obtained from the `goal_response_callback()`. As such, we need to make this accessible across our entire `CameraSweepActionClient()` class. Locate the `goal_response_callback()` class method, and add this line at the bottom as the last line of the `goal_response_callback()` method:

    ```py
    self._goal_handle = goal_handle
    ```

    This makes `goal_handle` accessible across the entire `CameraSweepActionClient()` class as `#!py self._goal_handle`. 

1. We can only attempt to cancel an Action when it's in progress, therefore the *feedback callback* is the best place to trigger this. Locate the `feedback_callback()` class method and place the following at the end of it:

    ```py
    if self.stop:
        future = self._goal_handle.cancel_goal_async()
        future.add_done_callback(self.cancel_goal)
    ```

    Here, we call the `cancel_goal_async()` method from `self._goal_handle`, and add another new callback (`cancel_goal()`) to it (i.e. to encapsulate what we want to happen when the action is cancelled).

1. Now, let's define this as another new (and final!) class method:

    ```py
    def cancel_goal(self, future):
        cancel_response = future.result()
        if len(cancel_response.goals_canceling) > 0:
            self.get_logger().info('Goal successfully canceled')
            self.goal_cancelled = True
        else:
            self.get_logger().info('Goal failed to cancel')
    ```

    The input to this callback is another *future*, which we can use to determine if the goal has been cancelled (as shown above). If it *has*, then we set our `self.goal_cancelled` flag to `True`.

1. **Finally**, go back the `main()` function of the node. We're going to replace the `#!py rclpy.spin(action_client)` line now, with a `#!py rclpy.spin_once()`, wrapped inside a `#!py try` - `#!py except`, wrapped inside a `#!py while` loop!
    
    ```py
    while not action_client.goal_succeeded:
        try:
            rclpy.spin_once(action_client)
            if action_client.goal_cancelled:
                break
        except KeyboardInterrupt:
            print("Ctrl+C")
            action_client.stop = True
    ```

    The `#!py while` loop will execute until the action completes successfully, *or* until the goal is *cancelled*, *or* we shutdown the node with a ++ctrl+c++ interrupt.

    Look back through the node to see how all this will flow through your class.

1. We may wish to cancel a goal *conditionally* if - say - too much time has elapsed since the call was made, or the caller has been made aware of something else that has happened in the meantime (perhaps we're running out of storage space on the robot and can't save any more images!). 

    For the purposes of this exercise, we want to modify our node so that the action is always cancelled after a total of **5 images** have been captured. This can be done by making a fairly small modification to the `feedback_callback()`. **Have a go at implementing this now**. 

    * Have a go now at introducing a conditional call to the `cancel_goal()` method once a total of **5 images** have been captured.
    * You could use the `captured_images` attribute from the `CameraSweepFeedback` message to trigger this.

### A Summary of ROS Actions

ROS Actions work a lot like ROS Services, but they have the following key differences:

1. They can be **cancelled**: If something is taking too long, or if something else has happened, then an Action Client can cancel an Action whenever it needs to.
1. They provide **feedback**: so that a client can monitor what is happening and act accordingly (i.e. cancel the action, if necessary).

This mechanism is therefore useful for operations that may take a long time to execute, and where intervention might be necessary.

## Creating Action Servers in Python {#cam_swp_act_srv}

!!! info "Important"
    Cancel *all* active processes that you may have running before moving on.

So far we have looked at how to call an action server, but what about if we actually want to set up our own? We've been working with a pre-made action server in the previous exercises, but so far we haven't really considered how it actually works. First, let's do some detective work... We launched the Action Server using `roslaunch` in Exercise 1:

```bash
roslaunch tuos_examples camera_sweep.launch
```

!!! question "Questions"
    * What does this tell us about the *package* that the action server node belongs to?
    * Where, in the package directory, is this node likely to be located?
    * How might we find out the name of the Python node from the `camera_sweep.launch` file?

Once you've identified the name and the location of the source code, open it up in VS Code and have a look through it to see how it all works.

Don't worry too much about all the content associated with obtaining and manipulating camera images in there, we'll learn more about this in the next session. Instead, focus on the general overall structure of the code and the way that the action server is implemented.

1. As a starting point, consider the way in which the action server is initialised and the way a callback function is defined to encapsulate all the code that will be executed when the action is called:

    ``` { .python .no-copy }
    self.actionserver = actionlib.SimpleActionServer(self.server_name, 
        CameraSweepAction, self.action_server_launcher, auto_start=False)
    self.actionserver.start()
    ```

1. Look at how a `/cmd_vel` publisher and an `/odom` subscriber are defined in external classes:<a name="tb3_module" ></a>

    ``` { .python .no-copy }
    self.robot_controller = Tb3Move()
    self.robot_odom = Tb3Odometry()
    ```

    These are imported (at the start of the code) from an external `tb3.py` module that also lives in the same directory as the action server itself:

    ``` { .python .no-copy }
    from tb3 import Tb3Move, Tb3Odometry
    ```

    We do this to simplify the process of obtaining odometry data and controlling the robot, whilst keeping the actual action server code itself more concise. Have a look at the `tb3.py` module to discover exactly how these Python classes work.

1. Look inside the action server callback function to see how the camera sweep operation is performed once the action has been called:

    ``` { .python .no-copy }
    def action_server_launcher(self, goal):
        ...
    ```

    1. Consider the error checking that is performed on the `goal` input variables, and how the call to the action server is aborted should any of these goal requests be invalid:

        ``` { .python .no-copy }
        success = True
        if goal.sweep_angle <= 0 or goal.sweep_angle > 180:
            print("Invalid sweep_angle! Select a value between 1 and 180 degrees.")
            success = False
            ...

        if not success:
            self.result.image_path = "None [ABORTED]"
            self.actionserver.set_aborted(self.result)
            return
        ```

    1. Consider how preemption is implemented in the server, and how the Action is stopped on receipt of a preempt request:

        ``` { .python .no-copy }    
        if self.actionserver.is_preempt_requested():
            ...
        ```

    1. Also have a look at the way a `feedback` message is constructed and published by the server:

        ``` { .python .no-copy }
        self.feedback.current_image = i
        self.feedback.current_angle = abs(self.robot_odom.yaw)
        self.actionserver.publish_feedback(self.feedback)
        ```

    1. Finally, consider how we tell the server that the action has been completed successfully, how the `result` message is published to the caller, and how we make the robot stop moving:

        ``` { .python .no-copy }
        if success:
            rospy.loginfo("Camera sweep completed successfully.")
            self.actionserver.set_succeeded(self.result)
            self.robot_controller.stop()
        ```

#### :material-pen: Exercise 4: Developing an "Obstacle Avoidance" behaviour using an Action Server {#ex4}

Knowing what you now do about ROS Actions, do you think the Service Server/Client systems that we developed in Part 4 were actually appropriate use cases for ROS Services?  Probably not!  In fact, *Action* Server/Client methods would have probably been more appropriate! 

You are now going to construct your own Action Server and Client nodes to implement a more effective obstacle avoidance behaviour that could form the basis of an effective search strategy. For this, you're going to need to build your own Search Server and Client.

**Step 1: Launch a simulation**

There's a simulation environment that you can use as you're developing your action server/client nodes for this exercise. Launch the simulation in **TERMINAL 1**, with the following `roslaunch` command: 

***
**TERMINAL 1:**
```bash
roslaunch turtlebot3_gazebo turtlebot3_stage_4.launch
```
***

**Step 2: Build the Action Server**

1. In **TERMINAL 2** navigate to the `src` folder of your `part5_actions` package, create a Python script called `search_server.py`, and make it executable.

1. The job of the Action Server node is as follows:

    * The action server should make the robot move forwards until it detects an obstacle up ahead.
    * Similarly to the *Service* Server that you created last part, your *Action* Server here should be configured to accept two **goal** parameters:
        1. The speed (in m/s) at which the robot should move forwards when the action server is called. Consider doing some error checking on this to make sure a velocity request is less than the maximum speed that the robot can actually achieve (0.26 m/s)!
        1. The distance (in meters) at which the robot should stop ahead of any objects or boundary walls that are in front of it. To do this you'll need to subscribe to the `/scan` topic. Be aware that an object won't necessarily be directly in front of the robot, so you may need to monitor a range of `LaserScan` data points (within the `ranges` array) to make the collision avoidance effective (recall the [LaserScan callback example](./part4/scan_callback.md) and also have a look at the `Tb3LaserScan` class within the `tuos_examples/tb3.py` module that might help you with this).
    * Whilst your server performs its task it should provide the following **feedback** to the Action Caller:
        1. The distance travelled (in meters) since the current action was initiated.

            To do this you'll need to subscribe to the `/odom` topic. Remember that there's a `Tb3Odometry` class within [the `tuos_examples/tb3.py` module](#tb3_module) that might help you with obtaining this data.
            
            Remember also that your robot's orientation shouldn't change over the course of a single action call, only its `linear.x` and `linear.y` positions should vary.  Bear in mind however that the robot won't necessarily be moving along the `X` or `Y` axis, so you will need to consider the total distance travelled in the `X-Y` plane.  You should have done this in the [Part 2 `move_square` exercise](./part2.md#ex5), so refer to this if you need a reminder.

    * Finally, on completion of the action, your server should provide the following *three* **result** parameters:
        1. The *total* distance travelled (in meters) over the course of the action.
        1. The distance to the obstacle that made the robot stop (this should match, or very close to, the distance that was provided by the Action Client in the **goal**).
        1. The angle (in degrees) at which this obstacle is located in front of the robot (`Tb3LaserScan` class within the `tuos_examples/tb3.py` module, which may already provide this).

1. An action message has been created for you to use for this exercise: `tuos_msgs/Search.action`.  Navigate to the `action` folder of the `tuos_msgs` package directory (or use `rosmsg info ...` in the terminal) to find out everything you need to know about this action message in order to develop your Action Server (and Client) nodes appropriately.

1. We've put together [some template code](./part5/search_server.md) to help you with this. For further guidance though, you should also refer to the code for `/camera_sweep_action_server` node, which [we talked about earlier](#cam_swp_act_srv): a lot of the techniques used by `/camera_sweep_action_server` node will be similar to what you'll need to do in this exercise. <a name="ex4_ret"></a>

1. Whenever you're ready you can launch your action server from **TERMINAL 2**, using `rosrun`, as below:

    ***
    **TERMINAL 2:**
    ```bash
    rosrun part5_actions search_server.py
    ```
    ***

**Step 3: Build the Action Client**

1. In **TERMINAL 3** navigate to the `src` folder of your `part5_actions` package, create a Python script called `search_client.py`, and make it executable.

1. The job of the Action Client node is as follows:

    * The client needs to issue a correctly formatted **goal** to the server.
    * The client should be programmed to monitor the **feedback** data from the Server.  If it detects (from the feedback) that the robot has travelled a distance *greater than 2 meters* without detecting an obstacle, then it should cancel the current action call using the `cancel_goal()` `actionlib` method.

1. Use the techniques that we used in the Client node from [Exercise 3](#ex3) as a guide to help you with this. There's also [a code template here](./part5/search_client.md) to help you get started. <a name="ex4c_ret"></a>

1. Once you have everything in place launch the action client with `rosrun` as below:

    ***
    **TERMINAL 3:**
    ```bash
    rosrun part5_actions search_client.py
    ```
    ***

    If all is good, then this client node should call the action server, which will - in turn - make the robot move forwards until it reaches a certain distance from an obstacle up ahead, at which point the robot will stop, and your client node will stop too. Once this happens, reorient your robot (using the `turtlebot3_teleop` node) and launch the client node again to make sure that it is robustly stopping in front of obstacles repeatedly, and when approaching them from a range of different angles. 

    !!! info "Important"
        Make sure that your preemption functionality works correctly too, so that the robot never moves any further than 2 meters during a given action call!

## Some advanced exercises (if you're feeling adventurous!) {#advanced}

Want to do more with the ROS skills that you have now developed?! Consider the following advanced exercises that you could try out now that you know how to use ROS Actions!

!!! note
    We've covered a lot already in this session, and the next exercises are really just suggestions for more advanced things that you may want to explore to push your knowledge further (it may also help with the further work that you will do in Assignment #2...)

#### :material-pen: Advanced Exercise 1: Implementing a Search strategy {#adv_ex1}

What you developed in [the previous exercise](#ex4) could be used as the basis for an effective robot search strategy.  Up to now, your Action Client node should have the capability to call your `Search.action` server to make the robot move forwards by 2 meters, or until it reaches an obstacle (whichever occurs first), but you could enhance this further:

* Between action calls, your *client* node could make the robot turn on the spot to face a different direction and then issue a further action call to make the robot move forwards once again.
* The turning process could be done at random, or it could be informed by the **result** of the last action call, i.e.: if (on completion) the server has informed the client that it detected an object at an angle of, say, 10&deg; *anti-clockwise* from the front of the robot, then the client might then decide to turn the robot *clockwise* in an attempt to turn away from the object before issuing its next action call to make the robot move forwards again.
* By programming your client node to repeat this process over and over again, the robot would (somewhat randomly) travel around its environment safely, stopping before it crashes into any obstacles and reorienting itself every time it stops moving forwards. *This is effectively an implementation of a basic robotic search strategy!* 

    !!! tip "Enhancing this further..."
        Imagine SLAM was running at the same time too... your robot could be building up a map of its environment in the background as it slowly explored every part of it!

!!! success "Assignment #2 Checkpoint"
    Having completed Assignment #1 up to this point, you should have everything you need to tackle [Assignment #2 Task 2](../assignment2/parta/task2.md).

#### :material-pen: Advanced Exercise 2: Autonomous Navigation using waypoint markers {#adv_ex2}

In Part 3 you used SLAM to construct a map of an environment ([Exercise 2](./part3.md#ex2)) and then issued navigation requests to the `move_base` action server, via the command-line, ([Exercise 3](./part3.md#ex3)) to make your robot move to a zone marker, based on coordinates that you had established beforehand. Now that you know how to build Action Client Nodes in Python you could return to your `part2_navigation` package and build a new node that makes the robot move sequentially between each zone marker programmatically.

* Your node could cycle through the coordinates of all four of the zone markers (or "waypoints") that you established whilst using SLAM to build a map of the environment ([as per Exercise 2](./part3.md#ex2)).
* Your node could monitor the status of the `move_base_simple` action call to know when the robot has reached a zone marker, so that it knows when to issue a further action call to move on to the next one.
* You could refer to [the launch file that you created in Part 3](./part3.md#launch_file) to launch all the navigation processes that need to be running in order to enable and configure the ROS Navigation Stack appropriately for the TurtleBot3 robot.

## Wrapping Up

In Part 5 of this course you've learnt:

* How ROS Actions work and why they might be useful.
* How to develop Action Client Nodes in Python which can perform other tasks *concurrently* to the action they have requested, and which can also *cancel* the requested action, if required.
* How to use standard ROS tools to interrogate the topic messages used by an action server, allowing you to build clients to call them, and to also allow you to build standalone action servers yourself using bespoke Action messages.
* How to harness this communication method to implement a behaviour that could be used as the basis for a genuine robotic *search strategy*. 

### Topics, Services or Actions: *Which to Choose?*

You should now have developed a good understanding of the three communication methods that are available within ROS to facilitate communication between ROS Nodes:

1. Topic-based messaging.
1. ROS Services.
1. ROS Actions.

Through this course you've gained some practical experience using all three of these, but you may still be wondering how to select the appropriate one for a certain robot task... 

[This ROS.org webpage](https://wiki.ros.org/ROS/Patterns/Communication#Communication_via_Topics_vs_Services_vs_X) summarises all of this very nicely (and briefly), so you should have a read through this to make sure you know what's what. In summary though:

* **Topics**: Are most appropriate for broadcasting continuous data-streams such as sensor data and robot state information, and for publishing data that is likely to be required by a range of Nodes across a ROS network.
* **Services**: Are most appropriate for very short procedures like *quick* calculations (inverse kinematics etc.) and performing short discrete actions that are unlikely to go wrong or will not need intervention (e.g. turning on a warning LED when a battery is low).
* **Actions**: Are most appropriate for longer running tasks (like moving a robot), for longer processing calculations (processing the data from a camera stream) or for operations where we *might* need to change our mind and do something different or cancel an invoked behaviour part way through.
    
### WSL-ROS Managed Desktop Users: Save your work! {#backup}

Remember, to save the work you have done in WSL-ROS during this session so that you can restore it on a different machine at a later date. Run the following script in any idle WSL-ROS Terminal Instance now:

```bash
wsl_ros backup
```

You'll then be able to restore it to a fresh WSL-ROS environment next time you fire one up (`wsl_ros restore`).  