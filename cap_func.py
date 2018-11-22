maxSpeed = 30

def capSpeed(motorSpeed):
    if (motorSpeed < -maxSpeed):
        motorSpeed = -maxSpeed
    elif (motorSpeed > maxSpeed):
        motorSpeed = maxSpeed
    return motorSpeed

leftMotorSpeed = 120
rightMotorSpeed = -300

print (capSpeed(leftMotorSpeed))
print (capSpeed(rightMotorSpeed))
