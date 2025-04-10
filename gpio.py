import spidev
import RPi.GPIO as GPIO
import time

__all__ = ['delay', 'GPIO_Init', 'LCD_PINS', 'KEY_PINS', 'SPI']

# BCM GPIO pin numbers
LCD_PINS = {
    'RST': 27,
    'DC': 25,
    'CS': 8,
    'BL': 24
}

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


SPI = spidev.SpiDev(0, 0) # SPI device (bus, device)

def delay(ms: int | float) -> None:
    """Delay in milliseconds."""
    time.sleep(ms / 1000.0)

def GPIO_Init() -> int:
    """Initialize GPIO pins."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LCD_PINS, GPIO.OUT)
    GPIO.setup(KEY_PINS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    SPI.max_speed_hz = 9000000
    SPI.mode = 0b00
    return 0