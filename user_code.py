import controller_callbacks as cb
import utils
import time
import random

from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor
from pybricks.parameters import (Port, Stop)
from pybricks.hubs import EV3Brick
from pybricks.iodevices import I2CDevice
from pybricks.media.ev3dev import SoundFile, ImageFile
from _thread import start_new_thread, allocate_lock

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
#yeet_motor_port: Port = Port.D
laser_sensor = LaserSensor(Port.S1)

# Objects
ev3 = EV3Brick()
speaker_lock = allocate_lock()


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
#yeet_forward_button: int = utils.ButtonCode.LEFT_BUMPER
#yeet_back_button: int = utils.ButtonCode.RIGHT_BUMPER


# Misc options
reverse_motor_direction: bool = False
disable_arm_motor: bool = False
use_tank_drive: bool = False
controller_deadzone: float = 0.0




# Declare important variables
left_motor: Motor = None # type: ignore
right_motor: Motor = None  # type: ignore
arm_motor: Motor = None  # type: ignore
drivebase: DriveBase = None  # type: ignore
#yeetMotor: Motor = None

a: int = 1

# Other setup
ev3.speaker.set_volume(100)

# Example controller callback
# This makes a function called example that prints 'Hello, world!'
# and will be run every time the triangle button is pressed
def example():
    ev3.speaker.set_volume(random.randint(70,100))
    background_beep(random.randint(240,880),random.randint(100,500))
    
    

cb.register_on_press_callback(utils.ButtonCode.TRIANGLE, example)


# This function will be run once when the program starts up
def on_init() -> None:
    utils.init_motors()

    global drivebase
    drivebase = DriveBase(
        left_motor,
        right_motor,
        wheel_diameter=55,
        axle_track=121) # distance betweed wheels, make sure it is accurate
    
    ev3.speaker.set_volume(70)
    background_beep(440, 100)
    ev3.speaker.set_volume(100)

# This function will be run when you press the auto button as defined above
def auto() -> None:
    #background_play_file("/home/robot/RobotTheme3.wav")
    arm_motor.run_time(1000, 500, then=Stop.HOLD, wait=True)
    drivebase.drive(700,0)
    time.sleep(1.5)
    drivebase.stop()
    drivebase.drive(200,0)
    while laser_sensor.distance() > 200:
        print(laser_sensor.distance())
    drivebase.stop()
    arm_motor.run_time(-500, 700, then=Stop.HOLD, wait=True)   
    drivebase.drive(-700,0)
    time.sleep(3)
    drivebase.drive(-100,0)
    time.sleep(5)
    drivebase.stop()
    time.sleep(3)
    arm_motor.run_time(500, 700, then=Stop.HOLD, wait=True)

#def yeetForward() -> None:
    #yeetMotor.run_time(2000, 2000, then=Stop.HOLD, wait=False)

#def yeetBack() -> None:
    #yeetMotor.run_time(-2000, 2000, then=Stop.HOLD, wait=False)


def locked_beep(frequency, duration):
    """Call ev3.speaker.beep with speaker_lock held."""    
    with speaker_lock:
        ev3.speaker.beep(frequency, duration)

def background_beep(frequency, duration):
    """Call ev3.speaker.beep in background thread."""
    start_new_thread(locked_beep, (frequency, duration))

def locked_play_file(filename):
    """Call ev3.speaker.beep with speaker_lock held."""    
    with speaker_lock:
        ev3.speaker.play_file(filename)

def background_play_file(filename):
    """Call ev3.speaker.play_file in background thread."""
    start_new_thread(locked_play_file, (filename,))





