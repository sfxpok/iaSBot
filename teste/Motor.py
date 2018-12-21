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
    
    def movementDeg(self, degree):
        gyro = GyroSensor()
        gyro.mode = gyro.modes[1]
        while gyro.rate != 0:
            pass
        gyro.mode = gyro.modes[0]
        self.engine.on_for_degrees(self.speed, self.speed, degree)

    def movementRot(self, rotation):
        gyro = GyroSensor()
        gyro.mode = gyro.modes[1]
        while gyro.rate != 0:
            pass
        gyro.mode = gyro.modes[0]
        self.engine.on_for_rotations(self.speed, self.speed, rotation)

    def movementSec(self, seconds):
        gyro = GyroSensor()
        gyro.mode = gyro.modes[1]
        while gyro.rate != 0:
            pass
        gyro.mode = gyro.modes[0]
        self.engine.on_for_seconds(self.speed, self.speed, seconds)
    
    def fixPosition(self, gyro):
        if abs(gyro.angle) > 0:
            self.engine.on_for_rotations(5, -5, abs(gyro.angle))
        else:
            self.engine.on_for_rotations(-5, 5, abs(gyro.angle))

    def turnRight(self):
        gyro = GyroSensor()
        gyro.mode = gyro.modes[1]
        while gyro.rate != 0:
            pass
        gyro.mode = gyro.modes[0]
        self.engine.on(self.speed, -self.speed)        
        while abs(gyro.angle) < 70:
            pass
        self.engine.on(self.speed/4, -self.speed/4)
        while abs(gyro.angle) < 90:
            pass
        self.engine.off()
    
    def turnLeft(self):
        gyro = GyroSensor()
        gyro.mode = gyro.modes[1]
        while gyro.rate != 0:
            pass
        gyro.mode = gyro.modes[0]
        self.engine.on(-self.speed, self.speed)        
        while abs(gyro.angle) < 70:
            pass
        self.engine.on(-self.speed/4, self.speed/4)
        while abs(gyro.angle) < 90:
            pass
        self.engine.off()



