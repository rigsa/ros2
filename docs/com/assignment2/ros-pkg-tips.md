---  
title: Working with your ROS Package (in the Lab)
---  

Having followed [the instructions on the Getting Started page](./getting-started.md) (in Week 1), your team's ROS package will be hosted on GitHub, which makes it much easier to collaborate and transfer your work to the real hardware during the lab sessions[^rse].

[^rse]: **Remember**: If you're not already familiar with how to use tools like Git and GitHub, we would strongly recommend that you have a look at [This Course by the University of Sheffield's Research Software Engineering (RSE) Team](https://srse-git-github-zero2hero.netlify.app/){target="_blank"}. 

You'll need to transfer your ROS package to a robot laptop whenever you want to work on a real robot during the labs. 

## Getting Started in Each Lab Session {#getting-started}

Your team should be provided with the same laptop for every lab session. Having completed all the steps to set up SSH Keys (as described in the sections below), you should be able to return to the laptop, re-clone your package and continue working with relative ease at the start of each and every lab session.

1. **Check if you already have an SSH Key**: You'll save a private SSH Key (private to you and the rest of your team) on the laptop that has been designated to you for each lab session. The first step is to check whether this exists on your laptop:

    ``` { .txt .no-copy }
    ls -al ~/.ssh | grep com2009_teamXX_2026
    ```

    Replace `XX` with your team number.

    If your team's ssh key is presented then you're good to go, continue to Step 2. If not, go to the **[Setting up SSH Keys](#setting-up-ssh-keys)** section below.

1. **If your team's SSH Key exists**: start the laptop's ssh-agent and activate your key:

    ```bash
    eval "$(ssh-agent -s)"
    ```
    
    ``` { .bash .no-copy }
    ssh-add ~/.ssh/com2009_teamXX_2026
    ```

    Replacing `XX` with your team number.

1. Then, [clone your package onto the laptop](#ssh-clone).

    You'll be asked for your secret passphrase, hopefully you remember it!

    !!! warning
        We strongly recommend that you [delete your team's package from the laptop](#deleting-your-ros-package-after-a-lab-session) at the end of each lab session.

## Setting Up SSH Keys

Using *SSH keys*, you can clone your team's ROS package to the robot laptops, make commits and push these back up to GitHub during the labs, without needing to provide your GitHub username and a personal access token every time. This makes life a lot easier! The following steps describe the process you should follow to achieve this[^github-docs].

[^github-docs]: Adapted from [GitHub Docs](https://docs.github.com/en/authentication/connecting-to-github-with-ssh){target="_blank"}

### Step 1: Generating an SSH key (on the Laptop) {#ssh-keygen}

1. From a terminal instance on the laptop navigate to the `~/.ssh` folder:

    ```bash
    cd ~/.ssh
    ```

1. Create a new SSH key on the laptop, using your GitHub email address:

    ``` { .txt .no-copy }
    ssh-keygen -t ed25519 -C "your.email@sheffield.ac.uk"
    ```

    Replacing `your.email@sheffield.ac.uk` with **your GitHub email address**.

    <a name="ssh-key-name"></a>

1. You'll then be asked to `Enter a file in which to save the key`. This needs to be unique, so enter the name of your ROS package, e.g.: `com2009_teamXX_2026` (where `XX` is replaced with your team number).

1. You'll then be asked to `enter a passphrase`. This is how you make your SSH key secure, so that no other teams using the same laptop can access and make changes to your team's package/GitHub repo. You'll be asked to enter this whenever you try to commit/push new changes to your ROS package on GitHub. Decide on a passphrase and share this **ONLY** with your fellow team members. 

1. Next, start the laptop's ssh-agent:

    ```bash
    eval "$(ssh-agent -s)"
    ```

1. Add your SSH private key to the laptop's ssh-agent. You'll need to enter the name of the SSH key file that you created in the earlier step (e.g.: `com2009_teamXX_2026`)

    ``` { .txt .no-copy }
    ssh-add ~/.ssh/com2009_teamXX_2026
    ```

    Replacing `XX` with your team number of course!

1. Then, you'll need to add the SSH key to your account on GitHub...

### Step 2: Adding an SSH key to your GitHub account

*These instructions are replicated from [this GitHub Docs page](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account?platform=linux){target="_blank"}*.

1. On the laptop, copy the SSH public key that you created in the previous steps to your clipboard.
    
    Do this from a terminal on the laptop, using `cat`:

    ``` { .txt .no-copy }
    cat ~/.ssh/com2009_teamXX_2026.pub
    ```

    Replacing `XX` with your team number once again.

    The content of the file will then be displayed in the terminal... copy it from here.

    !!! tip "Tips"
        1. To copy text from inside a terminal window use ++ctrl+shift+c++
        2. You could also open the file in VS Code and copy it from there:

            ``` { .txt .no-copy }
            code ~/.ssh/com2009_teamXX_2026.pub
            ```

2. Go to your GitHub account in a web browser. In the upper-right corner of any page, click your profile photo, then click **Settings**.

3. In the "Access" section of the sidebar, click **SSH and GPG keys**.

4. Click **New SSH key**.

5. Enter a descriptive name for the key in the "Title" field, e.g. `com2009_dia_laptop1`.

6. Select `Authentication Key` as the "Key Type."

7. Paste the text from your SSH Public Key file into the "Key" field.

8. Finally, click the "Add SSH Key" button.

## Cloning your ROS package onto the Laptop {#ssh-clone}

With your SSH keys all set up, you'll be able to clone your ROS package onto the laptop. 

There's a ROS 2 Workspace on each of the robot laptops and (much the same as in your own local ROS environment) your package **must** reside within this workspace!

1. From a terminal on the laptop, navigate to the ROS 2 Workspace `src` directory:

    ```bash
    cd ~/ros2_ws/src/
    ```

1. Go to your ROS package on GitHub. Click the Code button and then select the SSH option to reveal the SSH address of your repo. Copy this. 

1. Head back to the terminal instance on the laptop to then clone your package into the `ros2_ws/src/` directory using `git`:

    ```bash
    git clone REMOTE_SSH_ADDRESS
    ```

    Where `REMOTE_SSH_ADDRESS` is the SSH address that you have just copied from GitHub.

1. Run Colcon to build your package, which is a **three-step process**:
	
    1. Navigate into the **root** of the ROS Workspace:

        ```bash
        cd ~/ros2_ws
        ```
    
    1. Run the `colcon build` command, targetting your package only:
    
        ``` { .txt .no-copy }
        colcon build --packages-select com2009_teamXX_2026 --symlink-install
        ```
        (Again, replacing `XX` with *your* team number.)
        
    1. Then, re-source your environment:
	
        ```bash
        source ~/.bashrc
        ```

1. Navigate into your package: 

    ``` { .txt .no-copy }
    cd ~/ros2_ws/src/com2009_teamXX_2026/
    ```

    ... and then run the following commands to set your identity (which will allow you to make commits to your package repo):

    ``` { .txt .no-copy }
    git config user.name "your name"
    ```
    ``` { .txt .no-copy }
    git config user.email "your email address"
    ```

You should then be able to commit and push any updates that you make to your ROS package while working on the laptop, back to your remote repository using the secret passphrase that you defined earlier!

## Deleting your ROS package after a lab session

Remember that the Robotics Laptops use an account that everyone in the class has access to. You might therefore want to delete your package from the laptop at the end of each lab session. It's very easy to clone it back onto the laptop again by following [the steps above](#getting-started) at the start of each lab session. Deleting your package (by following the instructions below) **won't** delete your SSH key from the laptop though, so you won't need to do all that again, and your SSH key will still be protected with the secret passphrase that you set up when generating the SSH Key to begin with (assuming that you are working on the same laptop, of course!) 

!!! warning
    Make sure you've pushed any changes to GitHub before deleting your package!

Delete your package by simply running the following command from any terminal on the laptop:

```bash
rm -rf ~/ros2_ws/src/com2009_teamXX_2026
```

... replacing `XX` with your own team's number!
