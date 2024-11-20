# DTMF Controlled Robot Protocol Group 6 ROBTEK Semester 3 SDU

## Setup of VSCode

To run the code you need to have the following packages
sounddevice
pyaudio
numpy
scipy
matplotlib
curses (If linux) Should be installed by default
windows-curses (if windows)
libscrc

### For Linux

```
pip install numpy
pip install sounddevice
pip install scipy
pip install pyaudio
pip install matplotlib
pip install libscrc
```

### For Windows

```
pip install numpy
pip install sounddevice
pip install scipy
pip install pyaudio
pip install matplotlib (or use: py -m pip install matplotlib)
pip install windows-curses
pip install libscrc
```

## Setup of Raspberry Pi DONE TO THE PART OF SSH MORE TO COME!

Install TB3_2024.IMG from ITSL.

Install Raspberry Pi imager loader on ubuntu machine from Raspberry Pi website.

In Raspberry Pi imager select Raspberry Pi 3 for operating system scrool down and choose custom now select the downloaded image from ITSL and select SD card to write to.

After installtion on sd card is done open the writeable folder from the sd card and cd into correct folder. This can also be done manually by navigating to the correct folder.

```
cd /media/\$USER/writeable/etc/netplan/
```

Open the .yaml file using

```
sudo nano 50-cloud-init.yaml
```

In this file add the wifi or hotspot the file should now look something like this

```
network:
    version: 2
    wifis:
        renderer: networkd
        wlan0:
            access-points:
                <WIFI SSID>:
                password: <PASSWORD>
            dhcp4: true
            optional: true
```

Now save and close the file. Eject the sd card and input in the RaspberryPi and boot it to a screen.
If this is run directly on the Pi make sure to run this command afterwards:

```
sudo netplan apply
```

Now login to the RaspberryPi using a screen

```
Username: pi
Password: password123
```

Verify that it has wifi by running

```
ip a
```

here you can see the ip of the Raspberry Pi under the wlan0
or
on an Ubuntu machine run

```
sudo arp-scan -l
```

Check for the RaspberryPi IP
We can now ssh into it in a new terminal by typing

```
ssh pi@<ip of pi>
```

Inside of the pi we need to setup ROS and know where our files are.
Trying to setup with mqtt interface first

```
screen
```

Then

```
ros2 launch mqtt_2_cmd_pkg mqtt_interface.launch.py
```

Then hit ctrl + a + c

Then run this

```
python3 main.py
```

MORE DETAILS ABOUT THIS TO FOLLOW.

## Code explanation
