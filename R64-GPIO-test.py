#!/usr/bin/env python

# Allison Creely, 2018, LGPLv3 License
# Rock 64 GPIO Library for Python

import R64.GPIO as GPIO
from time import sleep

print("Testing R64.GPIO Module...")

# Test Variables
print("")
print("Module Variables:")
print("Name           Value")
print("----           -----")
print("GPIO.ROCK      " + str(GPIO.ROCK))
print("GPIO.BOARD     " + str(GPIO.BOARD))
print("GPIO.BCM       " + str(GPIO.BCM))
print("GPIO.OUT       " + str(GPIO.OUT))
print("GPIO.IN        " + str(GPIO.IN))
print("GPIO.HIGH      " + str(GPIO.HIGH))
print("GPIO.LOW       " + str(GPIO.LOW))
print("GPIO.PUD_UP    " + str(GPIO.PUD_UP))
print("GPIO.PUD_DOWN  " + str(GPIO.PUD_DOWN))
print("GPIO.VERSION   " + str(GPIO.VERSION))
print("GPIO.RPI_INFO  " + str(GPIO.RPI_INFO))

# Set Variables
var_gpio_out1 = 16
var_gpio_in1 = 18

# GPIO Setup
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(var_gpio_out1, GPIO.OUT, initial=GPIO.HIGH)       # Set up GPIO as an output, with an initial state of HIGH
GPIO.setup(var_gpio_in1, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up GPIO as an input, pullup enabled

# Test Output
print("")
print("Testing GPIO Input/Output:")

var_gpio_state = GPIO.input(var_gpio_out1)                   # Return state of GPIO
print("Output State : " + str(var_gpio_state))               # Print results
sleep(1)
GPIO.output(var_gpio_out1, GPIO.LOW)                         # Set GPIO to LOW

# Test Input
var_gpio_state = GPIO.input(var_gpio_in1)                    # Return state of GPIO
print("Input State  : " + str(var_gpio_state))               # Print results
sleep(0.5)

# Test PWM Output
p=GPIO.PWM(var_gpio_out1, 60)

print("")
print("Testing PWM Output - DutyCycle - High Precision:")
print("PWM Output: 60Hz at 50% duty cycle for 1 second")
p.start(50)
sleep(1)
print("PWM Output: 60Hz at 25% duty cycle for 1 second")
p.ChangeDutyCycle(25)
sleep(1)
print("PWM Output: 60Hz at 10% duty cycle for 1 second")
p.ChangeDutyCycle(10)
sleep(1)
print("PWM Output: 60Hz at 1% duty cycle for 1 second")
p.ChangeDutyCycle(1)
sleep(1)
p.stop()

print("")
print("Testing PWM Output - DutyCycle - Low Precision:")
print("PWM Output: 60Hz at 50% duty cycle for 1 second")
p.start(50, pwm_precision=GPIO.LOW)
sleep(1)
print("PWM Output: 60Hz at 25% duty cycle for 1 second")
p.ChangeDutyCycle(25)
sleep(1)
print("PWM Output: 60Hz at 10% duty cycle for 1 second")
p.ChangeDutyCycle(10)
sleep(1)
print("PWM Output: 60Hz at 1% duty cycle for 1 second")
p.ChangeDutyCycle(1)
sleep(1)
p.stop()

print("")
print("Testing PWM Output - Frequency - High Precision:")
print("PWM Output: 60Hz at 50% duty cycle for 1 second")
p.start(50)
sleep(1)
print("PWM Output: 30Hz at 50% duty cycle for 1 second")
p.ChangeFrequency(30)
sleep(1)
print("PWM Output: 20Hz at 50% duty cycle for 1 second")
p.ChangeFrequency(20)
sleep(1)
print("PWM Output: 10Hz at 50% duty cycle for 1 second")
p.ChangeFrequency(10)
sleep(1)
p.stop()

GPIO.cleanup(var_gpio_in1)
GPIO.cleanup(var_gpio_out1)

print("")
print("Test Complete")
