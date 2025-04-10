from gpio import *
import RPi.GPIO as GPIO
import time

# darksidesync helper library

__all__ = ['KEY1', 'KEY2', 'KEY3', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'OK']

class Button:
    def __init__(self, pin: int, *, hold_ms: int = 500, debug: bool = False) -> None:
        self.pin = pin
        self.start_time = 0
        self.elapsed_time = 0
        self.debug = debug

    def start_timer(self) -> None:
        """Start the stopwatch"""
        if self.debug:
            print(f"Button {self.pin} pressed.")
        self.start_time = time.time_ns()
    
    def select_callback(self) -> int:
        """Stop the stopwatch and return the elapsed time"""
        if self.debug:
            print(f"Button {self.pin} released.")
        self.elapsed_time = time.time_ns() - self.start_time
        self.start_time = 0
        if self.debug:
            print(f"Elapsed time: {self.elapsed_time:.2f} seconds")

    def set_press_event(self) -> None:
        """Set a callback function to be called when the button is pressed"""
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.start_timer, bouncetime=200)

    def set_release_event(self) -> None:
        """Set a callback function to be called when the button is released"""
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.select_callback, bouncetime=200)


KEY1 = Button(KEY_PINS['KEY1'])
KEY2 = Button(KEY_PINS['KEY2'])
KEY3 = Button(KEY_PINS['KEY3'])
UP = Button(KEY_PINS['UP'])
DOWN = Button(KEY_PINS['DOWN'])
LEFT = Button(KEY_PINS['LEFT'])
RIGHT = Button(KEY_PINS['RIGHT'])
OK = Button(KEY_PINS['OK'])