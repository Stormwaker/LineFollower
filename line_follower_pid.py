#!/usr/bin/python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import _thread
import time
from time import sleep
from ev3dev.auto import *

# ------Input--------
print 'Setting input values'
power = 60
target = 0 # zmienilem z 55
kp = float(0.65) # Proportional gain. Start value 1
kd = 1           # Derivative gain. Start value 0
ki = float(0.02) # Integral gain. Start value 0
direction = -1
minRef = 7 # 41
maxRef = 63

# TODO check if sensor are connected in the right manner
ts = TouchSensor('in2')
cs1 = ColorSensor('in4') #lewy
cs2 = ColorSensor('in1') #prawy
leds = Leds()
sound = Sound()
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

def steering2(course, power):
	"""
	Computes how fast each motor in a pair should turn to achieve the
	specified steering.
	Input:
		course [-100, 100]:
		* -100 means turn left as fast as possible,
		*  0   means drive in a straight line, and
		*  100  means turn right as fast as possible.
		* If >100 power_right = -power
		* If <100 power_left = power
	power: the power that should be applied to the outmost motor (the one
		rotating faster). The power of the other motor will be computed
		automatically.
	Output:
		a tuple of power values for a pair of motors.
	Example:
		for (motor, power) in zip((left_motor, right_motor), steering(50, 90)):
			motor.run_forever(speed_sp=power)
	"""
	if course >= 0:
		if course > 100:
			power_right = 0
			power_left = power
		else:
			power_left = power
			power_right = power - ((power * course) / 100)
	else:
		if course < -100:
			power_left = 0
			power_right = power
		else:
			power_right = power
			power_left = power + ((power * course) / 100)
	return (int(power_left), int(power_right))



def run(power, target, kp, kd, ki, direction, minRef, maxRef):
	"""
	PID controlled line follower algoritm used to calculate left and right motor power.
	Input:
		power. Max motor power on any of the motors
		target. Normalized target value.
		kp. Proportional gain
		ki. Integral gain
		kd. Derivative gain
		direction. 1 or -1 depending on the direction the robot should steer
		minRef. Min reflecting value of floor or line
		maxRef. Max reflecting value of floor or line
	"""
	lastError = error = integral = 0
	tank_drive.on(SpeedPercent(power), SpeedPercent(power))
    print ("NIE BLOKUJE SIE! :D") # TODO check if this works

	while not ts.is_pressed:
		refReadLeft = cs1.reflected_light_intensity
        refReadRight = cs2.reflected_light_intensity
		error = refReadLeft - refReadRight
		derivative = error - lastError
		lastError = error
		integral = float(0.5) * integral + error
		course = (kp * error + kd * derivative + ki * integral) * direction

		es1, es2 = steering2(course, power) # es - engine speed
		tank_drive.on(SpeedPercent(es1), SpeedPercent(es2)) # TODO check if this works
		sleep(0.05)

sound.speak('LETS GO!')
run(power, target, kp, kd, ki, direction, minRef, maxRef)

# Stop the motors before exiting.
print ('Stopping motors')
tank_drive.off()
