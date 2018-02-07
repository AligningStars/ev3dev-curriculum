"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        """Construct the left, right, and arm motors as well as the touch sensor, and sets the maximum speed"""
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor
        self.MAX_SPEED = 900

        # Check that the motors are actually connected
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor
        assert self.touch_sensor
        assert self.color_sensor
        assert self.ir_sensor

    def drive_inches(self, inches_target, motor_dps):
        """Drive the desired number of inches as inputed by the user,
        when positive moves in a positive direction, when input is negative
        moves in negative direction. motor_dps stands for the speed of the
        motor in degrees per second."""
        assert self.left_motor.connected
        assert self.right_motor.connected

        degrees_per_inch = 90
        motor_turns_needed_in_degrees = inches_target * degrees_per_inch
        self.left_motor.run_to_rel_pos(
            position_sp=motor_turns_needed_in_degrees, speed_sp=motor_dps,
            stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(
            position_sp=motor_turns_needed_in_degrees, speed_sp=motor_dps,
            stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        """Turn desired number of degrees. If positive turn_speed robot
        should turn left, if negative turn_speed motor should turn right.
        turn_speed_sp is the speed of the robot turning"""
        assert self.left_motor.connected
        assert self.right_motor.connected

        degrees = degrees_to_turn * 4.44        # TODO match comment and code
        if turn_speed_sp > 0:
            self.left_motor.run_to_rel_pos(position_sp=-degrees,
                                           speed_sp=turn_speed_sp,
                                           stop_action=ev3.Motor.STOP_ACTION_BRAKE)
            self.right_motor.run_to_rel_pos(position_sp=degrees,
                                            speed_sp=turn_speed_sp,
                                            stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        else:
            self.left_motor.run_to_rel_pos(position_sp=degrees,
                                           speed_sp=turn_speed_sp,
                                           stop_action=ev3.Motor.STOP_ACTION_BRAKE)
            self.right_motor.run_to_rel_pos(position_sp=-degrees,
                                            speed_sp=turn_speed_sp,
                                            stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_calibration(self):
        """Calibrate the robots arm motor for motion"""
        assert self.arm_motor
        assert self.touch_sensor
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while True:
            time.sleep(0.01)
            if self.touch_sensor.is_pressed:
                break

        self.arm_motor.run_forever(stop_action=ev3.MediumMotor.STOP_ACTION_BRAKE)
        ev3.Sound.beep().wait()

        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(
            position_sp=-arm_revolutions_for_full_range)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

        self.arm_motor.position = 0

    def arm_up(self):
        """Move robot arm in the positive y-direction relative to rested
        position"""     # TODO conflict test
        assert self.touch_sensor
        assert self.arm_motor
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        # arm_revolutions_for_full_range = 14.2 * 360
        # self.arm_motor.run_to_rel_pos(
        #     position_sp=arm_revolutions_for_full_range,
        #     speed_sp=self.MAX_SPEED)
        while True:
            time.sleep(0.01)
            if self.touch_sensor.is_pressed:
                break
        self.arm_motor.stop_action = ev3.MediumMotor(ev3.OUTPUT_A).STOP_ACTION_BRAKE
        ev3.Sound.beep().wait()

    def arm_down(self):
        """Move robot arm in negative y-direction relative to max extended
        position"""
        assert self.touch_sensor
        assert self.arm_motor
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=self.MAX_SPEED)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def drive_left(self, left_speed):
        """Make only left motor run to turn robot right"""
        assert self.left_motor
        self.left_motor.run_forever(speed_sp=left_speed)

    def drive_right(self, right_speed):
        """Make only right motor run to turn robot left"""
        assert self.right_motor
        self.right_motor.run_forever(speed_sp=right_speed)

    def drive_forward(self, left_speed, right_speed):
        """Make both motors run to drive robot forward"""
        assert self.left_motor
        assert self.right_motor
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def drive_backward(self, left_speed, right_speed):
        """Make both motors run to drive robot forward"""
        assert self.left_motor
        assert self.right_motor
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def shutdown(self):
        """Shutdown both motors to completely stop movement"""  # TODO stop motion arm
        self.left_motor.run_forever(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_forever(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.arm_motor.run_forever(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.running = False

    def loop_forever(self):
        self.running = True
        while self.running:
            time.sleep(0.1)  # Do nothing (except receive MQTT messages) until an MQTT message calls shutdown.

