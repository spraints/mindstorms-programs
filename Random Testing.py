from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math

# Create your objects here.
hub = MSHub()

images = [
    'ANGRY',
    'ASLEEP',
    'BUTTERFLY',
    'CHESSBOARD',
    'CONFUSED',
    'COW',
    'DIAMOND',
    'DIAMOND_SMALL',
    'DUCK',
    'FABULOUS',
]

# cycle through images so i can see if i can cancel a program.
for i in images:
    print(i)
    hub.light_matrix.show_image(i, 100)
    wait_for_seconds(1)
    if hub.left_button.was_pressed():
        break

# Write your program here.
hub.speaker.beep()
