#!/usr/bin/env python

# Allison Creely, 2018, LGPLv3 License
# Rock 64 GPIO Library for Python

# Import modules
import __builtin__
import os.path
from array import array
from multiprocessing import Process

# Define static module variables
var_gpio_root = '/sys/class/gpio'
ROCK = 'ROCK'
BOARD = 'BOARD'
BCM = 'BCM'
HIGH = 1
LOW = 0
OUT = 'out'
IN = 'in'
PUD_UP = 0
PUD_DOWN = 1
VERSION = '0.6.3'
RPI_INFO = {'P1_REVISION': 3, 'RAM': '1024M', 'REVISION': 'a22082', 'TYPE': 'Pi 3 Model B', 'PROCESSOR': 'BCM2837', 'MANUFACTURER': 'Embest'}

# Define dynamic module variables
gpio_mode = ROCK
var_warningmode = 1


# Functions
def setmode(mode):
    if mode in ['ROCK','BOARD','BCM']:
        global gpio_mode
        gpio_mode = mode
    else:
        print("An invalid mode ({}) was passed to setmode(). Use one of the following: ROCK, BOARD, BCM").format(mode)

def getmode():
    return gpio_mode

def setwarnings(state=True):
    if state in [0,1]:
        global var_warningmode
        var_warningmode = state
    else:
        print("Error: {} is not a valid warning mode. Use one of the following: True, 1, False, 0").format(state)

def setup(channel, direction, pull_up_down=PUD_DOWN, initial=LOW):
    # Check if GPIO export already exists
    var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel) + "/value"
    var_gpio_exists = os.path.exists(var_gpio_filepath)
    if var_gpio_exists == 1:
        if var_warningmode == 1:
            print("This channel ({}) is already in use, continuing anyway.  Use GPIO.setwarnings(False) to disable warnings.").format(channel)
    # Export GPIO
    else:
        try:
            var_gpio_filepath = var_gpio_root + "/export"
            with open(var_gpio_filepath, 'w') as file:
                file.write(str(channel))
        except:
            print("Error: Unable to export GPIO")
    # Set GPIO direction (in/out)
    try:
        var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel) + "/direction"
        with open(var_gpio_filepath, 'w') as file:
            file.write(str(direction))
    except:
        print("Error: Unable to set GPIO direction")
        return
    # If GPIO direction is out, set initial value of the GPIO (high/low)
    if direction == 'out':
        try:
            var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel) + "/value"
            with open(var_gpio_filepath, 'w') as file:
                file.write(str(initial))
        except:
            print("Error: Unable to set GPIO initial state")
    # If GPIO direction is in, set the state of internal pullup (high/low)
    if direction == 'in':
        try:
            var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel) + "/active_low"
            with open(var_gpio_filepath, 'w') as file:
                file.write(str(pull_up_down))
        except:
            print("Error: Unable to set internal pullup resistor state")

def output(channel, var_state):
    # Get direction of requested GPIO
    try:
        var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel) + "/direction"
        with open(var_gpio_filepath, 'r') as file:
            direction = file.read(1)
    except:
        print("Error: Unable to get GPIO direction")
        return
    # Perform sanity checks
    if (direction != 'o') and (direction != 'i'):
        print("You must setup() the GPIO channel first")
        return
    if direction != 'o':
        print("The GPIO channel has not been set up as an OUTPUT")
        return
    # Set the value of the GPIO (high/low)
    try:
        var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel) + "/value"
        with open(var_gpio_filepath, 'w') as file:
            file.write(str(var_state))
    except:
        print("Error: Unable to set GPIO output state")

def input(channel):
    # Get direction of requested GPIO
    try:
        var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel) + "/direction"
        with open(var_gpio_filepath, 'r') as file:
            direction = file.read(1)
    except:
        print("Error: Unable to get GPIO direction")
        return
    # Perform sanity checks
    if (direction != 'o') and (direction != 'i'):
        print("You must setup() the GPIO channel first")
        return
    # Get the value of the GPIO
    try:
        var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel) + "/value"
        with open(var_gpio_filepath, 'r') as file:
            return file.read(1)
    except:
        print("Error: Unable to get GPIO value")

def PWM(self, channel, frequency):
    # Get direction of requested GPIO
    try:
        var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel) + "/direction"
        with open(var_gpio_filepath, 'r') as file:
            direction = file.read(1)
    except:
        print("Error: Unable to get GPIO direction")
        return
    # Perform sanity checks
    if (direction != 'o') and (direction != 'i'):
        print("You must setup() the GPIO channel first")
        return
    if direction != 'o':
        print("The GPIO channel has not been set up as an OUTPUT")
        return
    if frequency == '0.0':
        print("frequency must be greater than 0.0")
        return
    # Not implemented
    print("Error: Not implemented")
    #p = Process(target=PWM_process, args=(channel, frequency,))
    #return p

def wait_for_edge(channel, var_edge, var_timeout):
    print("Error: Not implemented")

def event_detected(channel, var_edge):
    print("Error: Not implemented")

def add_event_detect(channel, var_edge, callback, bouncetime):
    print("Error: Not implemented")

def add_event_callback(channel, callback):
    print("Error: Not implemented")

def remove_event_detect(channel):
    print("Error: Not implemented")

def cleanup(channel='none'):
    if channel == 'none':
        for var_gpio_all in range(105):
            try:
                var_gpio_filepath = var_gpio_root + "/unexport"
                with open(var_gpio_filepath, 'w') as file:
                    file.write(str(var_gpio_all))
            except:
                pass
    elif channel in range(105):
        try:
            var_gpio_filepath = var_gpio_root + "/unexport"
            with open(var_gpio_filepath, 'w') as file:
                file.write(str(channel))
        except:
            print("Error: Unknown Failure")
    else:
        print("Error: Invalid GPIO specified")
