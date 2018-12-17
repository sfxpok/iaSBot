# 🤖 Survivor Bot 🤖

Developed with Visual Studio Code along with the extension [ev3dev-browser](https://marketplace.visualstudio.com/items?itemName=dlech.ev3dev-browser) on several systems: 

- Linux Mint 19 x86_64

- Ubuntu 18.10 x86_64

- Windows 7 64-bit

The [ev3dev](https://www.ev3dev.org/) firmware was used for the development of this project with a memory card. Usually our computers were always connected to the Brickman with Bluetooth.

### Sensors

- INPUT_1: Touch sensor
- INPUT_2: Ultrasonic sensor
- INPUT_3: Color sensor
- INPUT_4: Gyro sensor

### Motors

- OUTPUT_A: Left motor (LargeMotor)
- OUTPUT_B: Right motor (LargeMotor)
- OUTPUT_C: Forklift motor (LargeMotor)
- OUTPUT_D: Attack motor (MediumMotor)

Dependency: [python-ev3dev2](https://pypi.org/project/python-ev3dev2/)

[ev3dev2 API documentation](https://media.readthedocs.org/pdf/python-ev3dev/ev3dev-stretch/python-ev3dev.pdf?fbclid=IwAR1HmBFEMNMhJSpXuWfiDfa1OAkgJ6_GLlFFeymIgzuSS3MQebvAMik4uUg)