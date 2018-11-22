!/usr/bin/python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sound import Sound
from time import sleep

# initalizing inputs
ts = TouchSensor('in2')
cs1 = ColorSensor('in4') # left
cs2 = ColorSensor('in1') # right

# initializing outputs
td = MoveTank(OUTPUT_A, OUTPUT_B)
sound = Sound()

# initializing variables
maxSpeed = 10
power = -12

def capSpeed(motorSpeed):
    if (motorSpeed < -maxSpeed):
        motorSpeed = -maxSpeed
    elif (motorSpeed > maxSpeed):
        motorSpeed = maxSpeed
    return motorSpeed

# PID variables
Kp = 1
Ki = 0.15
Kd = 1
derivative = 0
integral = 0
error = 0
lastError = 0

# stating readiness
sound.speak('LETS GO!')

print("Calibrating")
while not ts.is_pressed:
    cs1.calibrate_white()
    cs2.calibrate_white()
print("Calibration ended")
sleep(2)

# main loop
while not ts.is_pressed:

    # reading RBG values from sensors
    r1, g1, b1 = cs1.rgb
    r2, g2, b2 = cs2.rgb

    # PID stuff
    error = r1 - r2
    error *= 50
    error /= 200
    integral = integral + error
    derivative = error - lastError
    lastError = error
    turn = Kp*error + Kd*derivative + Ki*integral
    leftMotorSpeed = capSpeed(power - turn)
    rightMotorSpeed = capSpeed(power + turn)
    td.on_for_seconds(SpeedPercent(leftMotorSpeed),SpeedPercent(rightMotorSpeed), 1, False, False)
    sleep(0.01)

td.off()
