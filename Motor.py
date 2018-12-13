from ev3dev2 import motor

class Motor:
    def __init__(self, speed=25):
        self.speed = motor.SpeedPercent(speed)

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = speed
  
class LargeMotor(Motor):
    def __init__(self, output, speed=None):
        self.engine = motor.LargeMotor(output)
        if (speed):
            self.setSpeed(speed)

    def movementDeg(self, degree):
        self.engine.on_for_degrees(self.speed, degree)

    def movementRot(self, rotation):
        self.engine.on_for_rotations(self.speed, rotation)
        
    def movementSec(self, seconds):
        self.engine.on_for_seconds(self.speed, seconds)
    
    def getPosition(self):
        self.engine.get_attr_int

class MediumMotor(Motor):
    def __init__(self, output, speed=None):
        self.engine = motor.MediumMotor(output)
        if (speed):
            self.setSpeed(speed)

    def movementDeg(self, degree):
        self.engine.on_for_degrees(self.speed, degree)

    def movementRot(self, rotation):
        self.engine.on_for_rotations(self.speed, rotation)

    def movementSec(self, seconds):
        self.engine.on_for_seconds(self.speed, seconds)