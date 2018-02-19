"""
Contains the necessary code sent to the ev3 robot to make it run in the
desired manner.

Author: Sydney Larson
"""

import ev3dev.ev3 as ev3
import time

import robot_controller as robo
import mqtt_remote_method_calls as com

robot = robo.Snatch3r()

def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
    robot.loop_forever()  # Calls a function that has a while True: loop within it to avoid letting the program end.

main()

#def follow_the_line(robot,color_to_seek):
 #   white_level = robot.color_sensor.reflected_light_intensity
  #  black_level = robot.color_sensor.reflected_light_intensity
#
 #   while not robot.color_sensor.color == color_to_seek:
  #      if robot.color_sensor.reflected_light_intensity > white_level - 70:
   #         robot.turn_degrees(20, 600)
    #        time.sleep(0.05)
     #   elif robot.color_sensor.reflected_light_intensity < black_level + 30:
      #      robot.drive_forward(600, 600)
       # time.sleep(0.01)
