#!/usr/bin/python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MediumMotor
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import InfraredSensor
from ev3dev2.sound import Sound
from time import sleep

terminate = False
ts = TouchSensor('in2')
cs1 = ColorSensor('in4') #lewy
cs2 = ColorSensor('in1') #prawy
ps = InfraredSensor('in3')
mm = MediumMotor(OUTPUT_C)

sound = Sound()
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
#steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)
# left_motor = LargeMotor(OUTPUT_B); 
# right_motor = LargeMotor(OUTPUT_A);
# stale dla kolorow
max_speed = 12
bialy = 19
czarny = 7
Kp=1.5
Ki=0.1 #rozwaz zmniejszenie
Kd=3
derivative=0
integral = 0
error1=0
error2=0
lastError=0
power =-15 #rozwaz zmniejszenie
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
print("Start kalibracji")
while not ts.is_pressed:
    cs1.calibrate_white()
    cs2.calibrate_white()

print("Koniec kalibracji")

sleep(2)



poZakrecie = True
poCzerwonym = False
podniesiony = True
powrot = False

while not ts.is_pressed:
    #tank_drive_on(power,power)
    # left_motor.run_direct()
    # right_motor.run_direct()
    
    r1, g1, b1 = cs1.rgb
    r2, g2, b2 = cs2.rgb

    if (b1 > 60 and b1 < 150 and r1 < 70 and r1 > 20 and not poZakrecie):
        print("NIEBIESKI!")
        poZakrecie = True
        tank_drive.on_for_rotations(SpeedPercent(-20),SpeedPercent(20), 0.6, True, True)
        tank_drive.on_for_rotations(SpeedPercent(-20),SpeedPercent(-20), 0.3, True, True)

    if (b1 < 50 and r1 > 200 and not poCzerwonym): #and poZakrecie bezpieczniej
        print("CZERWONY!")
        poCzerwonym = True
        tank_drive.on_for_rotations(SpeedPercent(-20),SpeedPercent(20), 0.6, True, True)
        tank_drive.on_for_rotations(SpeedPercent(-20),SpeedPercent(-20), 0.3, True, True)

    if (poZakrecie and ps.proximity < 5  and not podniesiony):
        tank_drive.off()
        mm.on_for_rotations(SpeedPercent(20), 0.2)
        podniesiony = True
        powrot = True
        tank_drive.on_for_rotations(SpeedPercent(20),SpeedPercent(20), 0.45, True, True)
        tank_drive.on_for_rotations(SpeedPercent(-20),SpeedPercent(20), 1.45, True, True)



        
    Sensorread_1=r1
    Sensorread_2=r2
    error1= 19 - Sensorread_1
    error2= 19 - Sensorread_2
    error = error1-error2
    error *= 50
    error /= 200
    integral = integral+error
    derivative= error - lastError
    lastError=error
    turn= Kp * error + Kd*derivative + Ki*integral
    minus = power - turn
    plus = power + turn
    """print("left r= " + str(r1) + "right r= " + str(r2))
    print("left g= " + str(g1) + "right g= " + str(g2))
    print("left b= " + str(b1) + "right b= " + str(b2))"""
    #print(str(r1) + " " + str(g1) + " " + str(b1) + "  " + str(r2) + " " + str(g2) + " " + str(b2))
    #print(ps.proximity)
    if (minus < -max_speed):
        minus = -max_speed
    elif (minus > max_speed):
        minus = max_speed
    if (plus > max_speed):
        plus = max_speed
    elif (plus < -max_speed):
        plus = -max_speed
    
    if r1 < 50 and r2 < 50 and powrot:
        powrot = False
        tank_drive.on_for_rotations(SpeedPercent(-20),SpeedPercent(20), 0.6, True, True)
    elif integral > 200:
        print("W LEWO")
        tank_drive.on_for_rotations(SpeedPercent(0),SpeedPercent(20), 0.8, True, True)
        integral = 50
    elif integral < -200:
        print("W PRWO")
        tank_drive.on_for_rotations(SpeedPercent(20),SpeedPercent(0), 0.8, True, True)
        integral = -50

    else:
        tank_drive.on_for_seconds(SpeedPercent(minus),SpeedPercent(plus), 1, False, False)

    if r1 > 190 and r2 > 190 and b1 < 50 and b2 < 50:
        tank_drive.on_for_rotations(SpeedPercent(-20),SpeedPercent(-20), 0.2, True, True)
        mm.on_for_rotations(SpeedPercent(-20), 0.20)
        tank_drive.on_for_rotations(SpeedPercent(40),SpeedPercent(40), 1, True, True)

    #else:
        #tank_drive.on_for_seconds(SpeedPercent(-10),SpeedPercent(-10), 1, False, False)

    print(str(error) + " " + str(minus) + " " + str(plus) + " " + str(integral))
    # for (motor, pow) in zip((left_motor, right_motor), sterowanie(turn, power)):
    # motor.duty_cycle_sp = pow
    sleep(0.01)
	
#left_motor.stop()
#right_motor.stop()
tank_drive.off()


