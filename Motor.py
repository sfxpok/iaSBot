from ev3dev2 import motor
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
        #self.position = motor.LargeMotor.position_sp
        if (speed):
            self.setSpeed(speed)

    def movementDeg(self, degree):
        self.engine.on_for_degrees(self.speed, degree)

    def movementRot(self, rotation):
        self.engine.on_for_rotations(self.speed, rotation)
        
    def movementSec(self, seconds):
        self.engine.on_for_seconds(self.speed, seconds)

    #def getPosition(self):
        #return self.position
    
    #def setPosition(self, position):
        #self.position = position
    

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
    def __init__(self, output1, output2, speed=35):
        """ self.engine1 = LargeMotor(output1)
        self.engine2 = LargeMotor(output2) """
        self.engine = motor.MoveTank(output1, output2)
        self.speed = speed
    
    def movementDeg(self, degree):
        self.engine.on_for_degrees(self.speed, self.speed, degree)

    def movementRot(self, rotation):
        self.engine.on_for_rotations(self.speed, self.speed, rotation)

    def movementSec(self, seconds):
        self.engine.on_for_seconds(self.speed, self.speed, seconds)

    def turnRight(self):
        self.engine.on_for_degrees(self.speed, -self.speed, 389.25)
    
    def turnLeft(self):
        self.engine.on_for_degrees(-self.speed, self.speed, 389.25)

def teste(teste):
    MoveTank(motor.OUTPUT_A, motor.OUTPUT_B).movementDeg(teste)
a = MoveTank(motor.OUTPUT_A, motor.OUTPUT_B)
#teste()