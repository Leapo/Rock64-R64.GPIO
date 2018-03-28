# Rock64-R64.GPIO
A Python GPIO library for the Rock64 single-board computer ([RPi.GPIO](https://sourceforge.net/projects/raspberry-gpio-python/) clone).

## Python Libraries and Scripts

**R64.GPIO**<br>
A re-implementation of the RPi.GPIO library for the Rock64. Currently under development.

Function                   | Status
:------------------------- | :---
`GPIO.setmode`             | Implemented
`GPIO.setwarnings`         | Implemented
`GPIO.setup`               | Implemented
`GPIO.output`              | Implemented
`GPIO.input`               | Implemented
`GPIO.PWM`                 | Not yet implemented
`GPIO.wait_for_edge`       | Not yet implemented
`GPIO.event_detected`      | Not yet implemented
`GPIO.add_event_detect`    | Not yet implemented
`GPIO.add_event_callback`  | Not yet implemented
`GPIO.remove_event_detect` | Not yet implemented
`GPIO.cleanup`             | Implemented

**R64-GPIO-test.py**<br>
A simple test script. Outputs a list of internal vars, sets the GPIO mode to "BOARD", sets up a GPIO output (blinks an LED if connected to pin 16), sets up a GPIO input (pulls-up and reports the state of pin 18), then cleans up all GPIO exports and exits.

# Resources
List of resources and reference material used while building the scripts and libraries in this repository
* [Sourceforge - RPi.GPIO](https://sourceforge.net/projects/raspberry-gpio-python/)
* [Kernel.org - GPIO/SYSFS Documentation](https://www.kernel.org/doc/Documentation/gpio/sysfs.txt)
* [Pine64 Forum - GPIO LED blinker using SYSFS on the Rock64](https://forum.pine64.org/showthread.php?tid=4695)
