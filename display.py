from PIL import Image, ImageDraw, ImageFont
import lcd

class Display:
    def __init__(self):
        self.lcd = lcd.LCD()
        self.image = Image.new("RGB", (self.lcd.width, self.lcd.height), "black")
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()  # or use truetype if you like

    def clear(self):
        self.draw.rectangle((0, 0, self.lcd.width, self.lcd.height), fill="black")

    def show(self):
        self.lcd.showImage(self.image)

    def draw_menu(self, title, options, selected):
        self.clear()

        self.draw.text((5, 0), title, font=self.font, fill="white")

        for i, option in enumerate(options):
            y = 15 + i * 12
            if y < self.lcd.height - 10:  # Avoid bottom overflow
                prefix = ">" if i == selected else " "
                color = "cyan" if i == selected else "white"
                self.draw.text((10, y), f"{prefix} {option}", font=self.font, fill=color)
        self.draw_icons()
        self.show()

    def draw_icons(self):
        self.icons = {
            'KEY1': Image.open("326688_save_floppy_guardar.png").convert("RGB"),
            'KEY2': Image.open("326704_store.png").convert("RGB"),
            'KEY3': Image.open("326709_tab.png").convert("RGB")
        }
        icon_w = self.icons['KEY1'].width
        icon_h = self.icons['KEY1'].height

        x = self.lcd.width - icon_w - 5

        positions = {
            'KEY1': (x, 5),
            'KEY2': (x, 5 + icon_h + 5),
            'KEY3': (x, 5 + 2 * (icon_h + 5))
        }
        for name, icon in self.icons.items():
            self.image.paste(icon, positions[name])