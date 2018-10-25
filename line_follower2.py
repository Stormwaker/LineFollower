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

ts = TouchSensor('in2'
cs1 = ColorSensor('in4') #lewy
cs2 = ColorSensor('in1') #prawy
leds = Leds()
sound = Sound()
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

# stale dla kolorow
bialy = 19
czarny = 7

sound.speak('LETS GO!')

#while not ts.is_pressed:
    #sleep(0.1)

lewo = 0
prosto = 1
prawo = 2

kierunek = prosto
zmiana_predkosci = 5
predkosc_podstawowa = 15
licznik_petli = 0

while not ts.is_pressed:
    licznik_petli += 1
	print("1 = " + str(cs1.reflected_light_intensity) + "2 = " str(cs2.reflected_light_intenisty))
	
    
    if (cs1.reflected_light_intensity < czarny):
        kierunek = lewo
        zmiana_predkosci = 0
    if (cs2.reflected_light_intensity < czarny):
        kierunek = prawo
        zmiana_predkosci = 0
    #if (cs1.reflected_light_intensity < 18 and cs1.reflected_light_intensity > 10) and (cs1.reflected_light_intensity < 18 and cs1.reflected_light_intensity > 10):"""
     
    if (kierunek == lewo):
        tank_drive.on_for_seconds(SpeedPercent(15 + zmiana_predkosci), SpeedPercent(15 - zmiana_predkosci * 0.5), 0.1, True, False)
    elif (kierunek == prawo):
        tank_drive.on_for_seconds(SpeedPercent(15 - zmiana_predkosci * 0.5), SpeedPercent(15 + zmiana_predkosci), 0.1, True, False)
    else:
        tank_drive.on_for_seconds(SpeedPercent(20), SpeedPercent(20), 0.1, True, False)
    if (not (licznik_petli % 4) and zmiana_predkosci < 15):
        zmiana_predkosci += 5

    

                
                

