import controller_callbacks as cb
import utils
import time

from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor
from pybricks.parameters import (Port, Stop)
from pybricks.hubs import EV3Brick
from pybricks.iodevices import I2CDevice

class LaserSensor:
    def __init__(self, port):
        self.i2c = I2CDevice(port, 0x02 >> 1)
        self.last_time = 0
        self.last_dist = 0

    def distance(self):
        now = time.time()
        if now - self.last_time > 0.1:
            self.last_time = now
            results = self.i2c.read(0x42, 2)
            self.last_dist = results[0] + (results[1] << 8)
        return self.last_dist


# Configure motor ports
left_motor_port: Port = Port.B
right_motor_port: Port = Port.C
arm_motor_port: Port = Port.A
yeet_motor_port: Port = Port.D
laser_sensor = LaserSensor(Port.S1)

# Objects
brick = EV3Brick()
brick.speaker.beep(440,250)

# If one of your motors is faster than the other, you can slow it down a bit here
left_motor_sensitivity: float = 0.8
right_motor_sensitivity: float = 0.8
arm_motor_sensitivity: float = 0.4

# Declare which buttons to use to start auto code and stop the robot
# A full list of button codes can be found in definitions.py
auto_button: int = utils.ButtonCode.CIRCLE
stop_button: int = utils.ButtonCode.SQUARE
armUp: int = utils.ButtonCode.TRIANGLE
disable_stop_button: bool = False
yeet_forward_button: int = utils.ButtonCode.LEFT_BUMPER
yeet_back_button: int = utils.ButtonCode.RIGHT_BUMPER


# Misc options
reverse_motor_direction: bool = False
disable_arm_motor: bool = False
use_tank_drive: bool = False
controller_deadzone: float = 0.0

# Example controller callback
# This makes a function called example that prints 'Hello, world!'
# and will be run every time the triangle button is pressed
def example():
    print("Hello, world!")
    brick.speaker.beep(440,250)


cb.register_on_press_callback(utils.ButtonCode.TRIANGLE, example)

# Declare important variables
left_motor: Motor = None # type: ignore
right_motor: Motor = None  # type: ignore
arm_motor: Motor = None  # type: ignore
drivebase: DriveBase = None  # type: ignore
yeetMotor: Motor = None

# This function will be run once when the program starts up
def on_init() -> None:
    utils.init_motors()

    global drivebase
    drivebase = DriveBase(
        left_motor,
        right_motor,
        wheel_diameter=55,
        axle_track=121) # distance betweed wheels, make sure it is accurate

# This function will be run when you press the auto button as defined above
def auto() -> None:
    while laser_sensor.distance() < 400:
        drivebase.drive(100,0)
    
    drivebase.stop()
    arm_motor.run_time(-500, 700, then=Stop.HOLD, wait=True)
    drivebase.straight(-500)
    drivebase.stop()
    arm_motor.run_time(500, 700, then=Stop.HOLD, wait=True)

def yeetForward() -> None:
    yeetMotor.run_time(2000, 2000, then=Stop.HOLD, wait=False)
    
def yeetBack() -> None:
    yeetMotor.run_time(-2000, 2000, then=Stop.HOLD, wait=False)
    
