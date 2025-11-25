# ROS 2 Labs at The University of Sheffield

## With the TurtleBot3 Waffle and ROS 2 Jazzy

Teaching material for Tom's ROS 2 Labs at The University of Sheffield.

Access the site here: https://tom-howard.github.io/ros2/

## Contributing

### Setting up a Python Environment

Site is built using [Material for MKDocs](https://squidfunk.github.io/mkdocs-material/)

First, create a Python virtual environment (ideally 3.9 or higher):

```
python3 -m venv venv
```

**[Activate the environment](https://realpython.com/what-is-pip/#using-pip-in-a-python-virtual-environment)** and install from [`requirements.txt`](./requirements.txt):

```
pip install -r requirements.txt 
```

### Editing

Site content is located in the "docs" directory. See here for guidance on how to write site content:

* General Guidance on Writing in Markdown: [A Markdown Cheatsheet](https://www.markdownguide.org/cheat-sheet/)
* Material for MkDocs Documentation: https://squidfunk.github.io/mkdocs-material/reference/

To preview the site as you write use the following command (make sure the Python environment is active!):

```
mkdocs serve
```

Then go to http://localhost:8000/ros2/ in a browser.
