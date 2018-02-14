""" A Pokemon go game played with the ev3 robot
    Author: Ruien Ni"""


import ev3dev.ev3 as ev3
import time

import robot_controller as robo
import mqtt_remote_method_calls as com


class DataContainer(object):

    def __init__(self):
        self.running = True


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.loop_forever()

def pick_up_pokeball():












main()
