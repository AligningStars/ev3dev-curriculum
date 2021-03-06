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
import math

class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        """Construct the left, right, and arm motors as well as the touch sensor, and sets the maximum speed"""
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        self.MAX_SPEED = 900

        # Check that the motors are actually connected
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor
        assert self.touch_sensor
        assert self.color_sensor
        assert self.ir_sensor
        assert self.pixy

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
        """Make only left motor run to turn robot left"""
        assert self.left_motor
        assert self.right_motor
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=left_speed)

    def drive_right(self, right_speed):
        """Make only right motor run to turn robot right"""
        assert self.right_motor
        assert self.left_motor
        self.right_motor.run_forever(speed_sp=-right_speed)
        self.left_motor.run_forever(right_speed=right_speed)

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
        self.left_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)

    def loop_forever(self):
        self.running = True
        while self.running:
            time.sleep(0.1)  # Do nothing (except receive MQTT messages) until an MQTT message calls shutdown.

    def seek_beacon(self):
        """ Uses the IR Sensor in BeaconSeeker mode to find the beacon.  If
        the beacon is found this return True.
        If the beacon is not found and the attempt is cancelled by hitting the touch sensor, return False."""
        beacon_seeker = ev3.BeaconSeeker(channel=1)
        assert beacon_seeker
        forward_speed = 300
        turn_speed = 100

        while not self.touch_sensor.is_pressed:
            current_heading = beacon_seeker.heading
            current_distance = beacon_seeker.distance

            if current_distance == -128:
                print("IR Remote not found. Distance is -128")
                self.shutdown()
            else:
                if math.fabs(current_heading) < 2:
                    print("On the right heading. Distance: ",
                          current_distance)
                    if current_distance == 1:
                        self.shutdown()
                        return True
                    elif current_distance > 0:
                        self.drive_forward(forward_speed, forward_speed)

                elif math.fabs(current_heading) > 2 and math.fabs(
                        current_heading) < 10:
                    if current_heading < 0:
                        self.left_motor.run_forever(speed_sp=-turn_speed)
                        self.right_motor.run_forever(speed_sp=turn_speed)
                        print("On the left heading. Distance: ",
                              current_distance)
                    elif current_heading > 0:
                        print("On the right heading. Distance: ",
                              current_distance)
                        self.left_motor.run_forever(speed_sp=turn_speed)
                        self.right_motor.run_forever(speed_sp=-turn_speed)

                elif math.fabs(current_heading) > 10:
                    self.shutdown()
                    print('Heading too far off')
                    print("Heading is too far off to fix: ", current_heading)

            time.sleep(0.2)
        # The touch_sensor was pressed to abort the attempt if this code runs.
        print("Abandon ship!")
        self.shutdown()
        return False

    def drive_to_color(self,color_to_seek):
        """Make the robot motors run in a forward direction until the
        robot's color sensor sees the desired color as specified by the
        input"""
        self.drive_forward(400, 400)
        while True:
            c = self.color_sensor.color
            if c == color_to_seek:
                self.shutdown()
                break
            time.sleep(0.1)
