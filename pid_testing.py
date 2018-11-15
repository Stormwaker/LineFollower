#!/usr/bin/python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import _thread
import time
from time import sleep

terminate = False
ts = TouchSensor('in2')
cs1 = ColorSensor('in4') #lewy
cs2 = ColorSensor('in1') #prawy
leds = Leds()
sound = Sound()
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
#steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)
# left_motor = LargeMotor(OUTPUT_B); 
# right_motor = LargeMotor(OUTPUT_A);
# stale dla kolorow
max_speed = 30
bialy = 19
czarny = 7
Kp=1
Ki=0.01
Kd=0.2
derivative=0
integral = 0
error1=0
error2=0
lastError=0
power =-20
error=0
sound.speak('LETS GO!')

# def sterowanie(course, power):
# 		if course >= 0:
# 		if course > 100:
# 			power_right = 0
# 			power_left = power
# 		else:	
# 			power_left = power
# 			power_right = powe,r - ((power * course) / 100)
# 	else:
# 		if course < -100:
# 			power_left = 0
# 			power_right = power
# 		else:
# 			power_right = power
# 			power_left = power + ((power * course) / 100)
# return (int(power_left), int(power_right))

while not ts.is_pressed:
    #tank_drive_on(power,power)
    # left_motor.run_direct()
    # right_motor.run_direct()
    Sensorread_1=cs1.reflected_light_intensity
    Sensorread_2=cs2.reflected_light_intensity
    error1=19 - Sensorread_1
    error2= 19 - Sensorread_2
    error = error1-error2
    integral = integral+error
    derivative= error - lastError
    lastError=error
    turn= Kp * error + Kd*derivative + Ki*integral
    minus = power - turn
    plus = power + turn
    print("minus = " + str(minus) + "plus = " + str(plus))
    if (minus < -max_speed):
        minus = -max_speed
    elif (minus > max_speed):
        minus = max_speed
    if (plus > max_speed):
        plus = max_speed
    elif (plus < -max_speed):
        plus = -max_speed
    
    tank_drive.on_for_seconds(SpeedPercent(minus),SpeedPercent(plus), 0.1, True, False)
    # for (motor, pow) in zip((left_motor, right_motor), sterowanie(turn, power)):
    # motor.duty_cycle_sp = pow
    sleep(0.01)
	
#left_motor.stop()
#right_motor.stop()

