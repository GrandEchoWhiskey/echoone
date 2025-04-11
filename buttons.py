from gpio import *
import RPi.GPIO as GPIO
import time

# darksidesync helper library

def callback(channel: int) -> None:
    """Callback function for button press event."""
    if channel in KEY_PINS.values():
        name = [key for key, pin in KEY_PINS.items() if pin == channel][0]
        print(f"Button {name} pressed.")

def setup_buttons() -> None:
    """Set up GPIO buttons."""
    for pin in KEY_PINS.values():
        GPIO.add_event_detect(pin, GPIO.FALLING, bouncetime=200)
        GPIO.add_event_callback(pin, callback=callback)
