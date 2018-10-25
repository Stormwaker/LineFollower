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
cs2 = ColorSensor('in1') #lewy
cs1 = ColorSensor('in4') #prawy
leds = Leds()
sound = Sound()
#tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
#steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)
left_motor = LargeMotor(OUTPUT_A); 
right_motor = LargeMotor(OUTPUT_B);
# stale dla kolorow
bialy = 19
czarny = 7
Kp=10
#Ki=0
Kd=0.05
Tp = 30
lastError=0
derivative=0
error=0
power = 30
turn=0
sound.speak('LETS GO!')

def sterowanie(course, power):
    if course < 0:
        if course<100:
            power_left = power
            power_right = 0
        else:
            power_left = power - ((power * course) /100)
            power_right = power + ((power * course) / 100)
    else:
        if course>100:
            power_right = 0
            power_left = power
        else:
            power_right = power + ((power * course)/100)
            power_left = power - ((power * course) / 100)
    print("powerleft= " + str(power_left) + "powerright= " + str(power_right))
    return (int(power_left), int(power_right))

left_motor.polarity = "inversed"
right_motor.polarity = "inversed"
while not ts.is_pressed:
    left_motor.run_direct()
    right_motor.run_direct()
    Sensorread_1=cs1.reflected_light_intensity
    Sensorread_2=cs2.reflected_light_intensity
    print("1 = " + str(Sensorread_1) + " 2 = " + str(Sensorread_2)+ "Turn  = " + str(turn))
    error=Sensorread_1 - Sensorread_2
    #integral = integral+error
    derivative= error - lastError
    lastError=error
    turn= Kp * error + Kd*derivative #+Ki*integral
    for (motor, pow) in zip((left_motor, right_motor), sterowanie(turn, power)):
        motor.duty_cycle_sp = pow
    sleep(0.01)


left_motor.stop()
right_motor.stop()

