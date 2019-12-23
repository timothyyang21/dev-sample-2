
# The Maze Challenge Graphics

![alt text](https://github.com/timothyyang21/dev-sample-2/demo_pic.png)

Author: Timothy Yang
Date: October 2019

## Game Instructions

This game is designed to teach people how to perform linear algebra's row reduction and reducing a matrix to its row reduced echelon form. In short, one needs to add and swap rows in order to reduce the rows so that each row's leading entry is the only one in its column.

### Start Game

Once the environment is set up, type the following in terminal to startup the game:
``` $ python3 start_game.py 2 ```
Below is the build instructions.

## Build Instructions

### Build Maze Graphics Program
To build and run the linear algebra game Game.py program, one needs to first download python 3.6 and the download pygame module

#### Windows
To see which version of Python 3 you have installed, open a command prompt and run

$ python3 --version
One can install python3.6 through Ubuntu

``` $ sudo apt-get update ```
``` $ sudo apt-get install python3.6 ```
If installation can't be done through the above command, go to python.org and install the appropriate version https://www.python.org/downloads/release/python-360/

After installing python, ones need to install the pygame module through pip

First, update the pip installer

``` $ python -m pip install --upgrade pip ```
If one does not have the pip installer installed (when installing python 3.6), one can install pip using the following command:

``` $ sudo apt update ```
``` $ sudo apt install python3-pip ```
Once the installation is complete, verify the installation by checking the pip version:

``` $ pip3 --version ```
Then, install pygame with

``` $ python -m pip install pygame ```
Pygame should be installed and now, import pygame should work.

Make sure that your python environment is using python 3.6 and that your pygame is installed for python 3.6. One easy way to check if pygame is installed for your python 3.6 is through

"Default Preferences" -> "Project Interpreter" 
If for some reason pygame isn't there, you can simply go to the lower left corner's + sign and install pygame package there.

One would also need to install pathlib2 for the game.py program.

``` $ python -m pip install pathlib2 ```

#### Mac OS
Install brew , using these instructions in this website:

https://brew.sh/index.html

This is a package manager capable of installing all sorts of programs.

If you need Python 3 installed:

``` $ brew install python3 ```
Link applications to Python3:

``` $ brew linkapps python3 ```
Install pygame Dependencies:

``` $ brew install --with-python3 sdl sdl_image sdl_mixer sdl_ttf portmidi ```
Install pygame:

``` $ pip3 install pygame ```
Install pathlib2:

``` $ pip3 install pathlib2 ```

## Run Instructions

### Run Game Program
Run the following command:

``` $ python3 start_game.py x ```
x is required and should be any number between 2 to 9
For example:

``` $ python3 start_game.py 2 ```

## Assumptions

The game.py assumes one has the log file that's been produced by the maze-solving program, and it assumes one has the right python environment to run the code.


