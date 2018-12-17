from ev3dev2 import motor
from ev3dev2.sensor.lego import GyroSensor
import threading

from gameGenerator import Robot

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
        while abs(gyro.angle) < 75:
            pass
        self.engine.on(self.speed/2, -self.speed/4)
        while abs(gyro.angle) < 87:
            pass
        self.engine.off()
    
    def turnLeft(self):
        gyro = GyroSensor()
        gyro.mode = gyro.modes[1]
        while gyro.rate != 0:
            pass
        gyro.mode = gyro.modes[0]
        self.engine.on(-self.speed, self.speed)        
        while abs(gyro.angle) < 75:
            pass
        self.engine.on(-self.speed/2, self.speed/4)
        while abs(gyro.angle) < 87:
            pass
        self.engine.off()

    #----------------------Por esta seccao noutro ficheiro se necessario----------------------
    #Ex: turn(270,90)---> Vira para a esquerda 2 vezes
    def turn(self, currentDir, targetDir):
        if currentDir != targetDir:
            number_of_turns = (targetDir - currentDir) / 90
            if number_of_turns > 0:
                for _ in range(number_of_turns):
                    self.turnRight()
            else:
                for _ in range(abs(number_of_turns)):
                    self.turnLeft()
            Robot().orientation = targetDir


    def isPositionValid(self, targetX=0, targetY=0):
        return (targetX >= 0 and targetX < 6 and targetY >= 0 and targetY < 6)

    
    #Problemas desta funçao sao que ele faz sempre o movimento no eixo do X primeiro
    #E verifica duas vezes se a posicaotarget é válida
    def moveTo(self, currentDir, currentX, currentY, targetX, targetY):
        if not self.isPositionValid(targetX,targetY):
            print('Not possible to move to that position')
        else:
            self.moveToX(currentDir, currentX, targetX)
            self.moveToY(currentDir, currentY, targetY)
            

    def moveToX(self, currentDir, currentX, targetX):
        if not self.isPositionValid(targetX):
            print('Not possible to move to that position')
        else:
            valueX = targetX - currentX
            if valueX != 0:
                if valueX > 0:
                    self.turn(currentDir, 90)
                else:
                    self.turn(currentDir, 270)
                    valueX = abs(valueX)
                for _ in range(valueX):
                    None #(Inserir codigo de andar para a frente 1 casa)
                Robot().coordX = targetX


    def moveToY(self, currentDir, currentY, targetY):
        if not self.isPositionValid(targetY):
            print('Not possible to move to that position')
        else:
            valueY = targetY - currentY
            if valueY != 0:
                if valueY > 0:
                    self.turn(currentDir, 0)
                else:
                    self.turn(currentDir, 180)
                    valueY = abs(valueY)
                for _ in range(valueY):
                    None #(Inserir codigo de andar para a frente 1 casa)
                Robot().coordY = targetY

    #-----------------------------------------------------------------------------------------
            

def teste(teste):
    MoveTank().movementDeg(teste)
#a = MoveTank(motor.OUTPUT_A, motor.OUTPUT_B)
#teste()

