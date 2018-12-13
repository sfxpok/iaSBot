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

class MoveTank(Motor):
    def __init__(self, output1, output2, speed=None):
        self.engine1 = LargeMotor(output1)
        self.engine2 = LargeMotor(output2)
        if(speed):
            setSpeed(self.speed)
        

    def movementDeg(self, degree1, degree2):
        threading.Thread(target=self.engine1.movementDeg(degree1), name='engine1', daemon=True).start()
        threading.Thread(target=self.engine1.movementDeg(degree2), name='engine2', daemon=True).start()

    def movementRot(self, rotation1, rotation2):
        threading.Thread(target=self.engine1.movementRot(rotation1), name='engine1', daemon=True).start()
        threading.Thread(target=self.engine1.movementRot(rotation2), name='engine2', daemon=True).start()

        
    def movementSec(self, seconds1, seconds2):
        threading.Thread(target=self.engine1.movementSec(seconds1), name='engine1', daemon=True).start()
        threading.Thread(target=self.engine1.movementSec(seconds2), name='engine2', daemon=True).start()


MoveTank(motor.OUTPUT_A, motor.OUTPUT_B).movementRot(2,2)