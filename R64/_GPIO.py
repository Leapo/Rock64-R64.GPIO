#!/usr/bin/env python

# Allison Creely, 2018, LGPLv3 License
# Rock 64 GPIO Library for Python

# Import modules
import os.path
from multiprocessing import Process, Value
from time import time
from time import sleep

# Define static module variables
var_gpio_root = '/sys/class/gpio'
ROCK = 'ROCK'
BOARD = 'BOARD'
BCM = 'BCM'
HIGH = 1
LOW = 0
OUT = 'out'
IN = 'in'
RISING = 'rising'
FALLING = 'falling'
BOTH = 'both'
PUD_UP = 0
PUD_DOWN = 1
VERSION = '0.6.3'
RPI_INFO = {'P1_REVISION': 3, 'RAM': '1024M', 'REVISION': 'a22082', 'TYPE': 'Pi 3 Model B', 'PROCESSOR': 'BCM2837', 'MANUFACTURER': 'Embest'}

# Define GPIO arrays
ROCK_valid_channels = [27, 32, 33, 34, 35, 36, 37, 38, 64, 65, 67, 68, 69, 76, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 96, 97, 98, 100, 101, 102, 103, 104]
BOARD_to_ROCK = [0, 0, 0, 89, 0, 88, 0, 0, 64, 0, 65, 0, 67, 0, 0, 100, 101, 0, 102, 97, 0, 98, 103, 96, 104, 0, 76, 68, 69, 0, 0, 0, 38, 32, 0, 33, 37, 34, 36, 0, 35, 0, 0, 81, 82, 87, 83, 0, 0, 80, 79, 85, 84, 27, 86, 0, 0, 0, 0, 0, 0, 89, 88]
BCM_to_ROCK = [68, 69, 89, 88, 81, 87, 83, 76, 104, 98, 97, 96, 38, 32, 64, 65, 37, 80, 67, 33, 36, 35, 100, 101, 102, 103, 34, 82]

# Define dynamic module variables
gpio_mode = None
warningmode = 1

# GPIO Functions
def setmode(mode):
    if mode in ['ROCK','BOARD','BCM']:
        global gpio_mode
        gpio_mode = mode
    else:
        print("An invalid mode ({}) was passed to setmode(). Use one of the following: ROCK, BOARD, BCM").format(mode)

def getmode():
    if gpio_mode in ['ROCK','BOARD','BCM']:
        return gpio_mode
    else:
        print("Error: An invalid mode ({}) is currently set").format(gpio_mode)

def get_gpio_number(channel):
    if gpio_mode in ['ROCK','BOARD','BCM']:
        # Convert to ROCK GPIO
        if gpio_mode == BOARD:
            channel_new = BOARD_to_ROCK[channel]
        if gpio_mode == BCM:
            channel_new = BCM_to_ROCK[channel]
        if gpio_mode == ROCK:
            channel_new = channel
        # Check that the GPIO is valid
        if channel_new in ROCK_valid_channels:
            return channel_new
        else:
            print("Error: GPIO not supported on {0} {1}").format(gpio_mode, channel)
            return None
    else:
        print("RuntimeError: Please set pin numbering mode using GPIO.setmode(GPIO.ROCK), GPIO.setmode(GPIO.BOARD), or GPIO.setmode(GPIO.BCM)")
        return None

def gpio_function(channel):
    # Translate the GPIO based on the current gpio_mode
    channel_int = get_gpio_number(channel)
    if channel_int == None:
        return
    # Get direction of requested GPIO
    try:
        var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel_int) + "/direction"
        with open(var_gpio_filepath, 'r') as file:
            direction = file.read(1)
    except:
        return "GPIO.UNKNOWN"
    if direction == 'i':
        return "GPIO.INPUT"
    elif direction == 'o':
        return "GPIO.OUTPUT"
    else:
        return "GPIO.UNKNOWN"

def setwarnings(state=True):
    if state in [0,1]:
        global warningmode
        warningmode = state
    else:
        print("Error: {} is not a valid warning mode. Use one of the following: True, 1, False, 0").format(state)

def validate_direction(channel, validation_type='both'):
    # Translate the GPIO based on the current gpio_mode
    channel_int = get_gpio_number(channel)
    if channel_int == None:
        return
    # Get direction of requested GPIO
    if validation_type in ['input', 'output', 'both']:
        try:
            var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel_int) + "/direction"
            with open(var_gpio_filepath, 'r') as file:
                direction = file.read(1)
        except:
            direction = 'none'
        # Perform sanity checks
        if (validation_type == 'input') and (direction != 'i'):
            print("You must setup() the GPIO channel ({0} {1}) as an input first").format(gpio_mode, channel)
            return 0
        elif (validation_type == 'output') and (direction != 'o'):
            print("You must setup() the GPIO channel ({0} {1}) as an output first").format(gpio_mode, channel)
            return 0
        elif ((validation_type == 'both') and (direction not in ['i', 'o'])) or (direction == 'none'):
            print("You must setup() the GPIO channel ({0} {1}) first").format(gpio_mode, channel)
            return 0
        else:
            return 1
    else:
        print("Error: {} is not a valid direction. use one of the following: input, output, both")
        return

def setup(channel, direction, pull_up_down=PUD_DOWN, initial=LOW):
    # If channel is an intiger, convert intiger to list
    if isinstance(channel, int) == True:
        channel = [channel]
    # Itterate through channel list
    for index in range(len(channel)):
        # Translate the GPIO based on the current gpio_mode
        channel_int = get_gpio_number(channel[index])
        if channel_int == None:
            return
        # Check if GPIO export already exists
        var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel_int) + "/value"
        var_gpio_exists = os.path.exists(var_gpio_filepath)
        if var_gpio_exists == 1:
            if warningmode == 1:
                print("This channel ({0} {1}) is already in use, continuing anyway.  Use GPIO.setwarnings(False) to disable warnings.").format(gpio_mode, channel[index])
        # Export GPIO if an export doesn't already exist
        else:
            try:
                var_gpio_filepath = var_gpio_root + "/export"
                with open(var_gpio_filepath, 'w') as file:
                    file.write(str(channel_int))
            except:
                print("Error: Unable to export GPIO")
        # Set GPIO direction (in/out)
        try:
            var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel_int) + "/direction"
            with open(var_gpio_filepath, 'w') as file:
                file.write(str(direction))
        except:
            print("Error: Unable to set GPIO direction")
            return
        # If GPIO direction is out, set initial value of the GPIO (high/low)
        if direction == 'out':
            try:
                var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel_int) + "/value"
                with open(var_gpio_filepath, 'w') as file:
                    # If multiple initial values, itterate through initial values
                    if isinstance(initial, int) == False:
                        file.write(str(initial[index]))
                    else:
                        file.write(str(initial))
            except:
                print("Error: Unable to set GPIO initial state")
        # If GPIO direction is in, set the state of internal pullup (high/low)
        if direction == 'in':
            try:
                var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel_int) + "/active_low"
                with open(var_gpio_filepath, 'w') as file:
                    file.write(str(pull_up_down))
            except:
                print("Error: Unable to set internal pullup resistor state")

def output(channel, value):
    # If channel is an intiger, convert intiger to list
    if isinstance(channel, int) == True:
        channel = [channel]
    # Itterate through channel list
    for index in range(len(channel)):
        # Translate the GPIO based on the current gpio_mode
        channel_int = get_gpio_number(channel[index])
        # Perform sanity checks
        if channel_int == None:
            return
        if validate_direction(channel[index], 'output') == 0:
            return
        # Set the value of the GPIO (high/low)
        try:
            var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel_int) + "/value"
            with open(var_gpio_filepath, 'w') as file:
                # If multiple states, itterate through states
                if isinstance(value, int) == False:
                    file.write(str(value[index]))
                else:
                    file.write(str(value))
        except:
            print("Error: Unable to set GPIO output state")

def input(channel):
    # Translate the GPIO based on the current gpio_mode
    channel_int = get_gpio_number(channel)
    # Perform sanity checks
    if channel_int == None:
        return
    if validate_direction(channel, 'both') == 0:
        return
    # Get the value of the GPIO
    try:
        var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel_int) + "/value"
        with open(var_gpio_filepath, 'r') as file:
            return file.read(1)
    except:
        print("Error: Unable to get GPIO value")

def wait_for_edge(channel, edge, bouncetime='none', timeout='none'):
    # Translate the GPIO based on the current gpio_mode
    channel_int = get_gpio_number(channel)
    # Perform sanity checks
    if channel_int == None:
        return
    if validate_direction(channel, 'input') == 0:
        return
    if edge not in [RISING, FALLING, BOTH]:
        print("The edge must be set to GPIO.RISING, GPIO.FALLING or GPIO.BOTH")
        return
    if (bouncetime != 'none') and (bouncetime <= 0):
        print("Bouncetime must be greater than 0")
        return
    if (timeout != 'none') and (timeout <= 0):
        print("timeout must be greater than 0")
        return
    # Set the edge state to trigger on
    try:
        var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel_int) + "/edge"
        with open(var_gpio_filepath, 'w') as file:
            file.write(str(edge))
    except:
        print("Error: Unable to set GPIO edge state")
        return
    # Get current state of the input
    try:
        var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel_int) + "/value"
        with open(var_gpio_filepath, 'r') as file:
            original_value = file.read(1)
    except:
        print("Error: Unable to get GPIO value")
        return
    # convert times from  ms to fractions of a second
    if timeout != 'none':
        timeout = timeout / 1000.0
    if bouncetime != 'none':
        bouncetime = bouncetime / 1000.0
    # Wait for interrupt (10ms resolution)
    while True:
        var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel_int) + "/value"
        with open(var_gpio_filepath, 'r') as file:
            new_value = file.read(1)
        if new_value != original_value:
            if bouncetime != 'none':
                sleep(bouncetime)
            return True
        sleep(0.01)
        if timeout != 'none':
            timeout -= 0.01
            if timeout <= 0.0:
                return None

def event_detected(channel):
    print("Error: GPIO.event_detected() Not implemented")

def add_event_detect(gpio, edge, callback='none', bouncetime='none'):
    print("Error: GPIO.add_event_detect() Not implemented")
    #p = Process(target=wait_for_edge, args=(gpio, edge), name='eventdetect_process')
    #p.start()

def add_event_callback(gpio, callback):
    print("Error: GPIO.add_event_callback() Not implemented")

def remove_event_detect(gpio):
    print("Error: GPIO.remove_event_detect() Not implemented")

def cleanup(channel='none'):
    # If no channel is specified...
    if channel == 'none':
        # Cleanup all GPIOs
        var_gpio_cleared = 0
        for gpio_index in range(105):
            var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(gpio_index) + "/value"
            var_gpio_exists = os.path.exists(var_gpio_filepath)
            if var_gpio_exists == 1:
                try:
                    var_gpio_filepath = var_gpio_root + "/unexport"
                    with open(var_gpio_filepath, 'w') as file:
                        file.write(str(gpio_index))
                    var_gpio_cleared = 1
                except:
                    print("Error: Unknown failure while performing cleanup")
        if (var_gpio_cleared == 0) and (warningmode == 1):
            print("No channels have been set up yet - nothing to clean up!  Try cleaning up at the end of your program instead!")
    # If a channel is specified...
    else:
        # If channel is an intiger, convert intiger to list
        if isinstance(channel, int) == True:
            channel = [channel]
        # Itterate through channel list
        for index in range(len(channel)):
            # Translate the GPIO based on the current gpio_mode
            channel_int = get_gpio_number(channel[index])
            if channel_int == None:
                return
            # Cleanup specified GPIO
            var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel_int) + "/value"
            var_gpio_exists = os.path.exists(var_gpio_filepath)
            if var_gpio_exists == 1:
                try:
                    var_gpio_filepath = var_gpio_root + "/unexport"
                    with open(var_gpio_filepath, 'w') as file:
                        file.write(str(channel_int))
                except:
                    print("Error: Unknown failure while performing cleanup")

# PWM Class
class PWM:
    def __init__(self, channel, frequency):
        # Translate the GPIO based on the current gpio_mode
        channel_int = get_gpio_number(channel)
        # Perform sanity checks
        if channel_int == None:
            return
        if validate_direction(channel, 'output') == 0:
            return
        if frequency <= 0.0:
            print("frequency must be greater than 0.0")
            return
        self.freq = frequency
        self.gpio = channel_int
        self.state = 0
        return

    def start(self, dutycycle, pwm_precision=HIGH):
        if (dutycycle < 0.0) or (dutycycle > 100.0):
            print("dutycycle must have a value from 0.0 to 100.0")
            return
        self.precision = pwm_precision
        self.dutycycle = dutycycle
        self.pwm_calc()
        self.p = Process(target=self.pwm_process, args=(self.gpio, self.sleep_high, self.sleep_low, self.precision), name='pwm_process')
        self.p.start()
        self.state = 1

    def stop(self):
        self.p.terminate()
        self.p.join()
        self.state = 0

    @staticmethod
    def pwm_busywait(wait_time):
        current_time = time()
        while (time() < current_time+wait_time):
            pass

    def pwm_calc(self):
        self.sleep_low = (1.0 / self.freq) * ((100 - self.dutycycle) / 100.0)
        self.sleep_high = (1.0 / self.freq) * ((100 - (100 - self.dutycycle)) / 100.0)

    @staticmethod
    def pwm_process(channel, sleep_high, sleep_low, precision=HIGH):
        var_gpio_filepath = str(var_gpio_root) + "/gpio" + str(channel) + "/value"
        # Note: Low precision mode greatly reduces CPU usage, but accuracy will depend upon your kernel.
        # p.start(dutycycle, pwm_precision=GPIO.LOW)
        try:
            if precision == HIGH:
                while True:
                    with open(var_gpio_filepath, 'w') as file:
                        file.write('1')
                    PWM.pwm_busywait(sleep_high)
                    with open(var_gpio_filepath, 'w') as file:
                        file.write('0')
                    PWM.pwm_busywait(sleep_low)
            else:
                while True:
                    with open(var_gpio_filepath, 'w') as file:
                        file.write('1')
                    sleep(sleep_high)
                    with open(var_gpio_filepath, 'w') as file:
                        file.write('0')
                    sleep(sleep_low)
        except:
            try:
                with open(var_gpio_filepath, 'w') as file:
                    file.write('0')
            except:
                pass
            print("Warning: PWM process ended prematurely")

    def ChangeFrequency(self, frequency):
        self.freq = frequency
        if self.state == 1:
            self.stop()
            self.start(self.dutycycle)

    def ChangeDutyCycle(self, dutycycle):
        self.dutycycle = dutycycle
        if self.state == 1:
            self.stop()
            self.start(self.dutycycle)
