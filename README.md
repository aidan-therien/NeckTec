# NeckTec
This is the repository for the BME Design NeckTec project. The contributors to this repository are [Aidan Therien](https://github.com/aidan-therien) and [James Allen](https://github.com/jamesallen123).

## Git Status
[![Build Status](https://travis-ci.com/BME547-Summer2020/final-project-duncan-therien.svg?token=RLd1CpbXx8eP2MxfSyyp&branch=master)](https://travis-ci.com/BME547-Summer2020/final-project-duncan-therien)

## Using This Software
This software consists of a graphical user interface (GUI) used by someone monitoring the physician use of the NeckTec device (the monitoring client). The GUI is capable of retrieving patient data  through the use of a cloud server. The client GUI can only receive data when the cloud server is running, so it is important to make sure that the server is running either locally or on a virtual machine.


#### Running The Server Locally
Perhaps the easiest way to use the client GUI is to use them while running on a local server.
To do this, open up a terminal and navigate to the folder containing `cloud_server.py`.
On the command line type `python server.py` and press `Enter` or `Return`.
The server is now running. To run either the patient-side client or monitoring-side client using this local server, make use the server name that each module is using is called `http://127.0.0.1:5000`.
When the modules for the client GUIs now make POST and GET requests, they will be using this local server.

#### Running The Server Using A Duke Virtual Machine
This section of the README discusses running the server on a Duke Virtual Machine, if you are not part of Duke, follow instructions [here](https://www.howtogeek.com/196060/beginner-geek-how-to-create-and-use-virtual-machines/) on using non-Duke virtual vachines.
If you are a member of the Duke Community and do not yet have a virtual machine set up, click [here](https://github.com/dward2/BME547/blob/master/Resources/virtual_machines.md) for information on setting up both a Duke Virtual Machine and software to use your machine.
As described in the link above, software like MobaXterm or PuTTY must be used to access your virtual machine.
This README will use MobaXterm as an example software for running the server on a Duke Virtual Machine. 

Make sure that your Duke Virtual Machine is on and open up MobaXterm. Log onto your virtual machine using your netid and password.
Once you are logged onto your virtual machine, you will have to clone the GitHub repository containing the modules for this software onto the virtual machine.
Copy the link of the repository in GitHub and type into the command line of your virtual machine `git clone <link>` where `<link>` is where you paste the copied link of the GitHub repository.
The modules for the server, as well as both of the GUIs should now be in your virtual machine.

Create a virtual environment by typing into the command line `python -m venv venv` and activate it by typing `source venv/bin/activate`.
To run the server on the virtual machine you must install any necessary python modules into your virtual environment. To do so, type into the command line `pip install -r requirements.txt`. Now create a new branch by typing `git branch <branch_name>` and switch to that branch by typing `git checkout <branch_name`. Once you are in this new branch, open your server code by typing `nano cloud_server.py` and scroll down to the bottom of the module where your see the command `app.run()`. Inside of the parentheses, insert the line `host="0.0.0.0"`. You can now save and exit the module.

Now, if you type into the command line `python server.py`, your server will run on the Duke Virtual Machine, and can be accessed from anywhere by using the server address (see the section in this README on accessing a server already running this code).


#### Using The Monitoring-Station Client
To use the monitoring-station client, open up a terminal and navigate using the command line to the folder containing the python module `monitoring_gui.py`.
On the command line type `python mpnitoring_gui.py` and hit `Enter` or `Return`.
You will now see window open up on the screen of your computer that looks like:

![alt text](https://github.com/aidan-therien/NeckTec/blob/master/Monitoring_GUI.JPG)

This monitoring-station graphical user interface enables a user to select a physician ID from a drop-down menu and load recent data.
Click the down arrow on the drop-down box at the top of the GUI window and select the ID of the physician that you are interested in monitoring.
Once you have selected a physician, click the button that says `Confirm`. Once this button has been clicked, the `Select Date` field will  be populated with the dates where the physician recorded data. Upon selecting a date the user can either click `Download Data` to download a `.csv` file of the session data, or click `Load Plot` to generate an image of the selected dataset plotted using `matplotlib` with the date and time of the selected dataset displayed below.

If at any time you wish to reset all of data on the scren to it's cleared appearence before any data was loaded, press the `Reset Data` button, and all of the patient data on the screen will disappear.
If at any time you wish to exit the monitoring-station GUI, you can click the `Exit` button, which will close the program.

 
## Access This Server

The code is running on the following server:
http://vcm-15220.vm.duke.edu:5000


## Software License 
MIT License

Copyright (c) 2020 Aidan Therien, James Allen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
