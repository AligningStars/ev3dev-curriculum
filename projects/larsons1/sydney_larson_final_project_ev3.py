"""
Contains the necessary code sent to the ev3 robot to make it run in the
desired manner.

Author: Sydney Larson
"""

import robot_controller as robo
import mqtt_remote_method_calls as com

def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.loop_forever()  # Calls a function that has a while True: loop
    # within it to avoid letting the program end.


main()

