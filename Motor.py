from ev3dev2 import motor
from ev3dev2.sensor.lego import GyroSensor
import threading


class Motor:
    def __init__(self, speed=25):
        self.speed = motor.SpeedPercent(speed)

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = speed
  

class LargeMotor(Motor):
    def __init__(self, output, speed=None):
        Motor.__init__(self)
        self.engine = motor.LargeMotor(output)
        if (speed):
            self.setSpeed(speed)

    def movementDeg(self, degree):
        self.engine.on_for_degrees(self.speed, degree)

    def movementRot(self, rotation):
        self.engine.on_for_rotations(self.speed, rotation)
        
    def movementSec(self, seconds):
        self.engine.on_for_seconds(self.speed, seconds)
    
    def moveDirection(self, direction):
        self.engine.run_forever()
    
    def motorReset(self):
        self.engine.reset
        

class MediumMotor(Motor):
    def __init__(self, output, speed=None):
        self.engine = motor.MediumMotor(output)
        Motor.__init__(self)
        if (speed):
            self.setSpeed(speed)

    def movementDeg(self, degree):
        self.engine.on_for_degrees(self.speed, degree)

    def movementRot(self, rotation):
        self.engine.on_for_rotations(self.speed, rotation)

    def movementSec(self, seconds):
        self.engine.on_for_seconds(self.speed, seconds)

class MoveTank():
    def __init__(self, speed=25):
        self.engine = motor.MoveTank(motor.OUTPUT_A, motor.OUTPUT_B)
        self.speed = speed
        self.gyro = GyroSensor()   
        self.gyro.mode = self.gyro.modes[1]
        while self.gyro.rate != 0:
            pass
        self.gyro.mode = self.gyro.modes[0]
        self.gyroAngle = 0 

    
    def movementDeg(self, degree, speed=0):
        targetSpeed = self.getSpeed(speed)
        self.engine.on_for_degrees(targetSpeed, targetSpeed, degree, brake=False)
        self.engine.wait_until_not_moving()
        #self.fixPosition(self.gyroAngle)


    def movementRot(self, rotation, speed=0):
        targetSpeed = self.getSpeed(speed)
        self.engine.on_for_rotations(targetSpeed, targetSpeed, rotation)
        self.engine.wait_until_not_moving()
        #self.fixPosition(self.gyroAngle)

    def movementSec(self, seconds, speed=0):
        targetSpeed = self.getSpeed(speed)
        self.engine.on_for_seconds(targetSpeed, targetSpeed, seconds)
        self.engine.wait_until_not_moving()
        #self.fixPosition(self.gyroAngle)

    def getSpeed(self, speed):
        if speed != 0:
            targetSpeed = speed
        else:
            targetSpeed = self.speed
        return targetSpeed
        

    def fixPosition(self, angle):
        gyro = GyroSensor()
        while gyro.angle != angle:
            """ print('gyro: '+str(gyro.angle))
            print('angle: '+str(angle)) """
            if self.gyro.angle > angle:
                self.engine.on(-1, 1)
            else:
                self.engine.on(1, -1)
        self.engine.off()
        self.engine.wait_until_not_moving()


    def turnRight(self):
        self.engine.on(self.speed/3, -self.speed/3)        
        while self.gyro.angle < abs(self.gyroAngle) + 70:
            pass
        self.engine.on(self.speed/5, -self.speed/5)
        while self.gyro.angle < abs(self.gyroAngle) + 89:
            pass
        self.engine.off()
        self.engine.wait_until_not_moving()
        self.gyroAngle += 90
        print(str(self.gyroAngle))
        #self.fixPosition(self.gyroAngle)
    
    def turnLeft(self):
        self.engine.on(-self.speed/2, self.speed/2)        
        while self.gyro.angle > self.gyroAngle - 70:
            pass
        self.engine.on(-self.speed/5, self.speed/5)
        while self.gyro.angle > self.gyroAngle - 89:
            pass
        self.engine.off()
        self.engine.wait_until_not_moving()
        self.gyroAngle -= 90
        print(str(self.gyroAngle))

        #self.fixPosition(self.gyroAngle)
