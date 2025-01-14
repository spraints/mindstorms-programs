from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math

# Make this match the program number that you download this to.
PROGRAM = 1

LARGE_BLUE_WHEEL_DIAMETER = 8.8 # cm
WHEEL_BASE = 12 # cm (estimate)

LEFT_MOTOR = "A
RIGHT_MOTOR = "B"

LEFT_ATTACHMENT = "C"
RIGHT_ATTACHMENT = "D"

CORR_SCALE = 5
CORR_MAX = 50

def main():
    ace = AdvancedBase()
    left_motor = Drawer(LEFT_ATTACHMENT)
    right_motor = Gate(RIGHT_ATTACHMENT)

    if PROGRAM == 1:
        ace.drive_forward(57) # till we hit the wall
        ace.reset_angle_goal()
        ace.drive_backward(10)
        ace.turn(90)
        ace.drive_forward(170) # drive across board.
        ace.turn(45)
        ace.drive_forward(50) # drive home.
    elif PROGRAM == 2:
        ace.drive_forward(50)
        ace.turn(45)
        ace.drive_forward(10) # hit whale
        ace.drive_backward(10)
        ace.turn(-45)
        ace.drive_backward(50)
    elif PROGRAM == 3:
        ace.drive_forward(5)
        ace.turn(-90)
        ace.drive_forward(40) # arrive at artificial habitat.
        ace.turn(45)
        ace.drive_forward(40)
        ace.turn(-80)
        ace.drive_forward(70)
    elif PROGRAM == 4:
        ace.drive_forward(40)
        ace.turn(90)
        ace.drive_forward(20) # raise the mast.
        ace.drive_backward(20)
        ace.turn(-90)
        ace.drive_backward(40)
    elif PROGRAM == 5:
        ace.drive_forward(50)
        ace.turn(-45)
        ace.drive_forward(20) # deliver shark and squid.
        ace.drive_backward(30) # get behind the boat.
        ace.turn(45)
        ace.drive_forward(50) # boat is delivered

class Gate:
    # Clockwise (positive) closes the gate.
    # The motor:gate gear ratio is 8:16.
    # Gate has a little more than 180 degrees of motion.

    def __init__(self, port):
        self.motor = Motor(port)
        self.travel = 2 * 180

    # Close the gate. This is different from 'close'
    # because it runs for seconds, so it won't get bound.
    def reset(self):
        self.motor.run_for_seconds(5, 10)

    def open(self):
        self.motor.run_for_degrees(self.travel, 100)

    def close(self):
        self.motor.run_for_degrees(-self.travel, 100)

class Drawer:
    # Clockwise (positive) extends the drawer (maybe?).

    def __init__(self, port):
        self.motor = Motor(port)
        self.travel = 720 # guess!

    def reset(self):
        self.motor.run_for_seconds(5, -10)

    def open(self):
        self.motor.run_for_degrees(-self.travel, 100)

    def close(self):
        self.motor.run_for_degrees(self.travel, 100)


class AdvancedBase:
    def __init__(self, leftmotor=LEFT_MOTOR, rightmotor=RIGHT_MOTOR, wheel_diameter_cm=LARGE_BLUE_WHEEL_DIAMETER, wheel_base_cm=WHEEL_BASE):
        self.hub = MSHub()
        self.mp = MotorPair(leftmotor, rightmotor)
        self.lm = Motor(leftmotor)
        self.lm.set_degrees_counted(0)
        self.wc = wheel_diameter_cm * math.pi # Calculate circumference, this is what we need in most cases.
        self.spin_circ = wheel_base_cm * math.pi # Circumference of the circle that the wheels trace when the robot spins.
        self.reset_angle_goal()

    def reset_angle_goal(self):
        self.angle_goal = 0
        self.hub.motion_sensor.reset_yaw_angle()

    def drive_forward(self, cm, accel = 10, max_speed = 100, min_speed = 10):
        cur_speed = min_speed
        cur_pos = last_pos = self.lm.get_degrees_counted()
        goal_position = cur_pos + 360 * cm / self.wc
        while cur_pos < goal_position:
            new_speed = goal_position - cur_pos
            if new_speed > max_speed:
                new_speed = max_speed # don't go over the limit.
            if new_speed - cur_speed > accel:
                new_speed = cur_speed + accel # don't speed up too quickly.
            if new_speed < min_speed:
                new_speed = min_speed # don't go too slowly.
            self.mp.start(self.correction(), new_speed)
            last_pos = cur_pos
            cur_speed = new_speed
            cur_pos = self.lm.get_degrees_counted()
        self.mp.stop()

    def drive_backward(self, cm, accel = 10, max_speed = 100, min_speed = 10):
        cur_speed = min_speed
        cur_pos = last_pos = self.lm.get_degrees_counted()
        goal_position = last_pos - 360 * cm / self.wc
        while cur_pos > goal_position:
            new_speed = cur_pos - goal_position
            if new_speed > max_speed:
                new_speed = max_speed # don't go over the limit.
            if new_speed - cur_speed > accel:
                new_speed = cur_speed + accel # don't speed up too quickly.
            if new_speed < min_speed:
                new_speed = min_speed # don't go too slowly.
            self.mp.start(-self.correction(), -new_speed)
            last_pos = cur_pos
            cur_speed = new_speed
            cur_pos = self.lm.get_degrees_counted()
        self.mp.stop()

    def turn(self, degrees, motor_speed=50):
        motor_degrees = int((self.spin_circ/self.wc) * abs(degrees))
        if degrees > 0:
            self.mp.move(motor_degrees, 'degrees', 100, motor_speed)
        else:
            self.mp.move(motor_degrees, 'degrees', -100, motor_speed)
        self.reset_angle_goal()

    def debug(self):
        print("[{}] current angle goal: {}, actual: {}".format(device_uuid(), self.angle_goal, self.get_yaw()))

    def get_yaw(self):
        # yaw gets larger when turning right.
        return self.hub.motion_sensor.get_yaw_angle()

    def correction(self):
        # Negative is a left turn, positive is a right turn.
        c = CORR_SCALE * (self.angle_goal - self.get_yaw())
        if c > CORR_MAX:
            return CORR_MAX
        elif c < -CORR_MAX:
            return -CORR_MAX
        else:
            return int(c)

runloop.run(main())
