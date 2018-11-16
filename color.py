!/usr/bin/python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MediumMotor
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import InfraredSensor
from ev3dev2.sound import Sound
from time import sleep

# initalizing inputs
ts = TouchSensor('in2')
cs1 = ColorSensor('in4') # left
cs2 = ColorSensor('in1') # right
ps = InfraredSensor('in3')

# initializing outputs
td = MoveTank(OUTPUT_A, OUTPUT_B)
mm = MediumMotor(OUTPUT_C)
sound = Sound()

# initializing variables
maxSpeed = 10
power = -12 

# PID variables
Kp=1
Ki=0.15
Kd=1
derivative=0
integral = 0
error=0
lastError=0

# initializing state variables
afterBlueTurn = False
afterRedTurn = False
hookLifted = False
returning = False

# stating readiness
sound.speak('LETS GO!')

print("Calibrating")
while not ts.is_pressed:
    cs1.calibrate_white()
    cs2.calibrate_white()
print("Calibration ended")
sleep(2)

shouldLower = raw_input("Should I lower the hook? y/n")

if shouldLower == "y":
	mm.on_for_rotations(SpeedPercent(20), 0.2)

# main loop
while not ts.is_pressed:
    
	# reading RBG values from sensors
    r1, g1, b1 = cs1.rgb
    r2, g2, b2 = cs2.rgb

	# BLUE TURN 
    if (b1 > 85 and b1 < 150 and r1 < 70 and r1 > 20 and not afterBlueTurn): 
        print("NIEBIESKI!")
        afterBlueTurn = True
        td.on_for_rotations(SpeedPercent(-20),SpeedPercent(20), 0.6, True, True)
        td.on_for_rotations(SpeedPercent(-20),SpeedPercent(-20), 0.3, True, True)

	# RED TURN
    if (b1 < 50 and r1 > 200 and not afterRedTurn):
        print("CZERWONY!")
        afterRedTurn = True
        td.on_for_rotations(SpeedPercent(-20),SpeedPercent(20), 0.6, True, True)
        td.on_for_rotations(SpeedPercent(-20),SpeedPercent(-20), 0.3, True, True)

	# GRABBING OBJECT
    if (afterBlueTurn and ps.proximity < 5  and not hookLifted):
        td.off()
        mm.on_for_rotations(SpeedPercent(20), 0.2)
        hookLifted = True
        returning = True
        td.on_for_rotations(SpeedPercent(20),SpeedPercent(20), 0.45, True, True)
        td.on_for_rotations(SpeedPercent(-20),SpeedPercent(20), 1.45, True, True)

	# RETURNING TO MAIN PATH
    if r1 < 50 and r2 < 50 and returning:
        returning = False
        td.on_for_rotations(SpeedPercent(-20),SpeedPercent(20), 0.6, True, True)

	# DROPPING OBJECT
	if r1 > 190 and r2 > 190 and b1 < 50 and b2 < 50:
		td.on_for_rotations(SpeedPercent(-20),SpeedPercent(-20), 0.2, True, True)
        mm.on_for_rotations(SpeedPercent(-20), 0.20)
        td.on_for_rotations(SpeedPercent(40),SpeedPercent(40), 1, True, True)
        
    error = r1 - r2
    error *= 50
    error /= 200
    integral = integral + error
    derivative = error - lastError
    lastError = error
    turn = Kp*error + Kd*derivative + Ki*integral
    leftMotorSpeed = power - turn
    rightMotorSpeed = power + turn
    if (leftMotorSpeed < -maxSpeed):
        leftMotorSpeed = -maxSpeed
    elif (leftMotorSpeed > maxSpeed):
        leftMotorSpeed = maxSpeed
    if (rightMotorSpeed > maxSpeed):
        rightMotorSpeed = maxSpeed
    elif (rightMotorSpeed < -maxSpeed):
        rightMotorSpeed = -maxSpeed
    
	td.on_for_seconds(SpeedPercent(leftMotorSpeed),SpeedPercent(rightMotorSpeed), 1, False, False)
	print(str(error) + " " + str(leftMotorSpeed) + " " + str(rightMotorSpeed) + " " + str(integral))
    #print(str(r1) + " " + str(g1) + " " + str(b1) + "  " + str(r2) + " " + str(g2) + " " + str(b2))
    sleep(0.01)
	
td.off()
