from gpio import *
import RPi.GPIO as GPIO
import time

# BCM button pin numbers
KEY_PINS = {
    'KEY1': 21,
    'KEY2': 20,
    'KEY3': 16,
    'UP': 6,
    'DOWN': 19,
    'LEFT': 5,
    'RIGHT': 26,
    'OK': 13
}

class ButtonHandler:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.last_pressed = None
        for pin in KEY_PINS.values():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_pressed(self):
        for name, pin in KEY_PINS.items():
            if GPIO.input(pin) == GPIO.LOW:
                if self.last_pressed != name:
                    self.last_pressed = name
                    return name
        self.last_pressed = None
        return None

    def cleanup(self):
        GPIO.cleanup()