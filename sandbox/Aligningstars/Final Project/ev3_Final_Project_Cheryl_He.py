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


class Hangman(object):

    def __init__(self):
        self.mqtt_client = None
        self.lcd = ev3.Screen()
        self.guess = ''
        self.word = ['p', 'r', 'o', 'j', 'e', 'c', 't']
        self.hp = 3
        self.index = 0
        self.running = False
        self.robot = robo.Snatch3r()
        self.touch_sensor = ev3.TouchSensor()

    def check_for_answer(self, guess):
        self.guess = guess
        if self.word == self.guess:
            self.mqtt_client.send_message("guess_response", ["You survived!"])
            ev3.Sound.speak("You survived")
            time.sleep(0.1)
            self.hp = 0

        else:
            for k in range(len(guess)):
                if self.guess[k] == '':
                    self.guess[k] = self.word[k]

            if self.word == self.guess:
                self.mqtt_client.send_message("guess_response",
                                              ["Your guess is correct! You have {} hp left.".format(self.hp)])
                ev3.Sound.speak("Correct, keep going.")

            else:
                self.hp -= 1
                if self.hp > 0:
                    ev3.Sound.speak("Wrong. Try again")
                else:
                    ev3.Sound.speak('Done')
                while not self.touch_sensor.is_pressed:
                    self.drive_and_say_hp()
                self.robot.shutdown()

                self.mqtt_client.send_message("guess_response",
                                              ["Your guess is wrong! You have {} hp left.".format(self.hp)])
            if self.hp == 0:
                self.mqtt_client.send_message("guess_response", ["You lost!"])
                ev3.Sound.speak("You lost")

    def loop_forever(self):
        while not self.hp == 0:
            # Do nothing while waiting for commands
            time.sleep(0.01)
        self.mqtt_client.close()
        print("Goodbye")
        ev3.Sound.speak("Goodbye").wait()

    def drive_and_say_hp(self):
        if self.hp == 2:
            self.robot.drive_forward(400, 400)
            while True:
                if self.robot.color_sensor.color == 'b':
                    self.robot.shutdown()
                    ev3.Sound.speak("hp is 2")
                    break
                time.sleep(0.1)
        elif self.hp == 1:
            self.robot.drive_forward(400, 400)
            while True:
                if self.robot.color_sensor.color == 'y':
                    self.robot.shutdown()
                    ev3.Sound.speak("hp is 1")
                    break
                time.sleep(0.1)
        elif self.hp == 0:
            self.robot.drive_forward(400, 400)
            while True:
                if self.robot.color_sensor.color == 'r':
                    self.robot.shutdown()
                    ev3.Sound.speak("hp is 0")
                    break
                time.sleep(0.1)

    def arm(self):
        command_to_run = input("u (for getting started)")
        if command_to_run == 'u':
                print("Move the arm to the up position")
                self.robot.arm_up()


def main():
    print("--------------------------------------------")
    print(" Hangman")
    print(" Press the touch sensor to exit")
    print("--------------------------------------------")
    ev3.Sound.speak("Hangman").wait()
    print("Press the touch sensor to exit this program.")

    my_delegate = Hangman()
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.mqtt_client = mqtt_client
    my_delegate.arm()
    mqtt_client.connect_to_pc()
    my_delegate.loop_forever()


main()



