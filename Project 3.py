from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math

# This is new again and again.

#------
# edit

from mindstorms import ColorSensor

s = ColorSensor(‘C’)
lightness = s.get_reflected_light()
print(lightness)

#------

from mindstorms import MotorPair

# You may need to change the A and B to match the ports that your motors are connected to.
drive_pair = MotorPair('A', 'B')

distance = 180
velocity = 50
steering = 0
drive_pair.move(distance, 'degrees', steering, velocity)

#------

from mindstorms import ColorSensor, MotorPair

# You may need to change the ports below.
s = ColorSensor('C')
drive_pair = MotorPair('A', 'B')

mid = 0 # change this to be halfway between white and black.

# for is a type of loop. In this case, we're running the contents 100 times.
for i in range(100):
    lightness = s.get_reflected_light()
    if lightness < mid:
        # break skips the rest of the loop
        break
    else:
        print("keep going!")
    drive_pair.move(45, 'degrees', 0, 30)

