from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank, MoveJoystick
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

# INPUT_1: Sensor toque
# INPUT_2: Sensor ultrasom
# INPUT_3: Sensor cor
# INPUT_4: N/A

# OUTPUT_A: Motor esquerdo
# OUTPUT_B: Motor direito
# OUTPUT_C: Motor empilhadora
# OUTPUT_D: Motor ataque

class Motor:
    def __init__(self):
        self.leftLeg = LargeMotor(OUTPUT_A)
        self.rightLeg = LargeMotor(OUTPUT_B)
        self.crane = LargeMotor(OUTPUT_C)
        self.doubleWalk = MoveTank(OUTPUT_A, OUTPUT_B)
        self.doubleJoystick = MoveJoystick(OUTPUT_A, OUTPUT_B)

class Sensor:
    def __init__(self):
        self.touch = TouchSensor(INPUT_1)

class Crane:
    def __init__(self):
        self.dist = 0