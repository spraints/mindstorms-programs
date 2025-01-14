from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math

left_motor_port = 'B'
right_motor_port = 'A'
light_sensor_port = 'C'

dark_color = 30
light_color = 100

drive_duration = 15000 # milliseconds
interval = 50 # milliseconds

drive_pair = MotorPair(left_motor_port, right_motor_port)
l = ColorSensor(light_sensor_port)

steps = drive_duration / interval
mid = (dark_color + light_color) / 2
interval_seconds = interval * 0.001

for i in range(steps):
    lightness = l.get_reflected_light()
    steering = lightness - mid
    drive_pair.start(steering, 50)
    wait_for_seconds(interval_seconds)
drive_pair.stop()


drive_pair = MotorPair('A', 'B')
velocity = 50
steering = 0
drive_pair.move(2, 'seconds', steering, velocity)
