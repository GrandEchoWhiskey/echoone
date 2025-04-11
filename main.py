from gpio import *
import lcd
from buttons import *
import RPi.GPIO as GPIO

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

#try:
def main():
    GPIO_Init()
    
    LCD = lcd.LCD()

    print("**********Init LCD**********")
    Lcd_ScanDir = lcd.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
    LCD.init(Lcd_ScanDir)

    setup_buttons()

    image = Image.new("RGB", (LCD.width, LCD.height), "WHITE")
    draw = ImageDraw.Draw(image)
    #font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
    print("***draw line")
    draw.line([(0,0),(127,0)], fill = "BLUE",width = 5)
    draw.line([(127,0),(127,127)], fill = "BLUE",width = 5)
    draw.line([(127,127),(0,127)], fill = "BLUE",width = 5)
    draw.line([(0,127),(0,0)], fill = "BLUE",width = 5)
    print("***draw rectangle")
    draw.rectangle([(18,10),(110,20)],fill = "RED")

    print("***draw text")
    draw.text((33, 22), 'WaveShare ', fill = "BLUE")
    draw.text((32, 36), 'Electronic ', fill = "BLUE")
    draw.text((28, 48), '1.44inch LCD ', fill = "BLUE")

    LCD.showImage(image)
    delay(500)

    image = Image.open('time.bmp')
    LCD.showImage(image)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()

#except:
#	print("except")
#	GPIO.cleanup()
