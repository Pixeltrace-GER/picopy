#!/usr/bin/env python3
"""this script listenes for a shutdown command (3 second hold of power button)

it shuts down the pi if and only if there are no external drives mounted at /media/pi
when the shutdown button command is recieved.

The error LED blinks 10 times rapidly if shutdown was aborted due to mounted drives.
"""

import subprocess
from datetime import datetime
from pathlib import Path
from gpiozero import Button
from time import sleep
import os
import socket

sleep_time = 0.2 #run loop 5x/sec
button_hold_time = 3 #require 3 second hold to shut down pi
power_button = Button(3, hold_time=3)

def led_cmd(status):
    """Sendet den LED-Status über einen Socket"""
    socket_path = "/tmp/led_socket"
    with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as client_socket:
        client_socket.sendto(status.encode(), socket_path)



def shutdown():
    """attempts shutdown
    - if any external drives mounted, does not shutdown
    - returns True if shutdown happens, false otherwise """
    # if any external drives are mounted, do not shut down
    num_external_drives = len(os.listdir('/media'))
    if num_external_drives>0:
        # do not shut down. 
        # add event to the log.
        with open('/home/pi/picopy/shutdown_log.txt','a+') as f:
            f.write(f'{datetime.now()}: Shutdown blocked due to mounted drives.\n')
        
        # flash error light 10x fast as a warning
        led_cmd("error_led/blink/0.1/0.1/10/False")
        sleep(10)
        return False

    else: #shutdown
        #blink all 3 LEDs 
        led_cmd("status_led/blink/0.2/0.2")
        led_cmd("progress_led/blink/0.2/0.2")
        led_cmd("error_led/blink/0.2/0.2")
        sleep(5)

        # write to log file
        with open('/home/pi/picopy/shutdown_log.txt','a+') as f:
            f.write(f'{datetime.now()}: Shutting down.\n')
        
        # force shutdown
        subprocess.call(['sudo','shutdown', '-h', 'now'], shell=False)

        return True

shutting_down = False
while not shutting_down:
    sleep(sleep_time)
    if power_button.is_held:
        shutting_down =  shutdown()
