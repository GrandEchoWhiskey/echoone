from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 128, 128

class Display:
    def __init__(self, lcd):
        self.lcd = lcd
        self.image = Image.new("RGB", (WIDTH, HEIGHT), "black")
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()  # or use truetype if you like

    def clear(self):
        self.draw.rectangle((0, 0, WIDTH, HEIGHT), fill="black")

    def show(self):
        self.lcd.showImage(self.image)

    def draw_menu(self, title, options, selected):
        self.clear()

        self.draw.text((5, 0), title, font=self.font, fill="white")

        for i, option in enumerate(options):
            y = 15 + i * 12
            if y < HEIGHT - 10:  # Avoid bottom overflow
                prefix = ">" if i == selected else " "
                color = "cyan" if i == selected else "white"
                self.draw.text((10, y), f"{prefix} {option}", font=self.font, fill=color)

        self.show()