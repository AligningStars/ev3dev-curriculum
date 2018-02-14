"""
File Name: ev3_Final_Project_Cheryl_He
Date Created: Feb 14, 2018
Author: Cheryl He
Introduction:

"""

import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import mqtt_remote_method_calls as com


def main():
    """main"""

    print("--------------------------------------------")
    print(" Hangman")
    print(" Press the touch sensor to exit")
    print("--------------------------------------------")
    ev3.Sound.speak("Hangman").wait()
    print("Press the touch sensor to exit this program.")

    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_pc()


