# display.py
from PIL import Image, ImageDraw, ImageFont
import lcd

WIDTH, HEIGHT = 160, 128

class Display:
    def __init__(self):
        self.lcd = lcd.LCD()
        self.image = Image.new('RGB', (WIDTH, HEIGHT), 'black')
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()

    def draw_menu(self, title, options, selected):
        self.draw.rectangle((0, 0, WIDTH, HEIGHT), fill='black')
        self.draw.text((5, 0), title, font=self.font, fill='white')

        for i, option in enumerate(options):
            y = 15 + i * 12
            color = 'white' if i != selected else 'cyan'
            self.draw.text((10, y), f"{'>' if i == selected else ' '} {option}", font=self.font, fill=color)

        self.lcd.showImage(self.image)

    def clear(self):
        self.draw.rectangle((0, 0, WIDTH, HEIGHT), fill='black')
        self.lcd.showImage(self.image)