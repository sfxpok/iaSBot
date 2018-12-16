###
# Definição de classes relativamente aos motores e sensores do rôbo. Também tem a listagem das ligações a cada cabo
###

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedRPM, MoveTank, MoveJoystick, MediumMotor, LargeMotor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, ColorSensor, GyroSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

# INPUT_1: Sensor toque
# INPUT_2: Sensor ultrasom
# INPUT_3: Sensor cor
# INPUT_4: Sensor giroscópio

# OUTPUT_A: Motor esquerdo
# OUTPUT_B: Motor direito
# OUTPUT_C: Motor empilhadora
# OUTPUT_D: Motor ataque (Positivo=Bala/Negativo=Soco)

class Motor:
    def __init__(self):
        self.leftLeg = LargeMotor(OUTPUT_A)
        self.rightLeg = LargeMotor(OUTPUT_B)
        self.forklift = LargeMotor(OUTPUT_C)
        self.doubleWalk = MoveTank(OUTPUT_A, OUTPUT_B)
        self.doubleJoystick = MoveJoystick(OUTPUT_A, OUTPUT_B)
        self.attack = MediumMotor(OUTPUT_D)

class Sensor:
    def __init__(self):
        self.touch = TouchSensor(INPUT_1)
        #touch.cor()

class Forklift:
    def __init__(self):
        self.height = 0
        self.maximumHeight = 500