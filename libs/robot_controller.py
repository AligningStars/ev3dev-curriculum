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


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        """Construct the left and right motors"""
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        # Check that the motors are actually connected
        assert self.left_motor.connected
        assert self.right_motor.connected

    def drive_inches(self, inches_target, motor_dps):
        """Drive the desired number of inches as inputed by the user"""
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
        assert self.left_motor.connected
        assert self.right_motor.connected

        degrees = degrees_to_turn * 4.44
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
