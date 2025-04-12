from gpio import *
import RPi.GPIO as GPIO
import numpy as np
import spidev

LCD_TYPES = {
    'LCD_1IN44': {'width': 128, 'height': 128, 'x_adjust': 2, 'y_adjust': 1},
    'LCD_1IN8': {'width': 160, 'height': 128, 'x_adjust': 1, 'y_adjust': 2}
}

LCD_TYPE = 'LCD_1IN44'

# BCM GPIO pin numbers
LCD_PINS = {
    'RST': 27,
    'DC': 25,
    'BL': 24
}

SCAN_DIR_DFT = 'U2D_R2L' # D2U_L2R, D2U_R2L, U2D_L2R, U2D_R2L, L2R_U2D, L2R_D2U, R2L_U2D, R2L_D2U

SPI = spidev.SpiDev(0, 0) # SPI device (bus, device)

class LCD:
    def __init__(self) -> None:
        self.__setup__()
        self.pins = LCD_PINS
        self.width = LCD_TYPES[LCD_TYPE]['width']
        self.height = LCD_TYPES[LCD_TYPE]['height']
        self.xadjust = LCD_TYPES[LCD_TYPE]['x_adjust']
        self.yadjust = LCD_TYPES[LCD_TYPE]['y_adjust']
        self.scandir = SCAN_DIR_DFT
        self.init(SCAN_DIR_DFT)

    def __setup__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(list(LCD_PINS.values()), GPIO.OUT)
        SPI.max_speed_hz = 9000000
        SPI.mode = 0b00

    @property
    def RST_PIN(self) -> int:
        return self.pins['RST']
    
    @property
    def DC_PIN(self) -> int:
        return self.pins['DC']
    
    @property
    def BL_PIN(self) -> int:
        return self.pins['BL']

    def reset(self) -> None:
        """Reset the LCD display"""
        GPIO.output(self.RST_PIN, GPIO.HIGH)
        delay(100)
        GPIO.output(self.RST_PIN, GPIO.LOW)
        delay(100)
        GPIO.output(self.RST_PIN, GPIO.HIGH)
        delay(100)

    def writeReg(self, reg:int) -> None:
        """Write a register to the LCD display"""
        GPIO.output(LCD_PINS['DC'], GPIO.LOW)
        SPI.writebytes([reg])

    def writeData(self, data:int) -> None:
        """Write data to the LCD display"""
        GPIO.output(LCD_PINS['DC'], GPIO.HIGH)
        SPI.writebytes([data])

    def writeRegData(self, reg:int, data:list) -> None:
        """Write register and data to the LCD display"""
        self.writeReg(reg)
        for i in range(len(data)):
            self.writeData(data[i])
		
    def initReg(self) -> None:
        """Initialize the LCD display registers"""
        self.writeRegData(0xB1,[0x01,0x2C,0x2D])
        self.writeRegData(0xB2,[0x01,0x2C,0x2D])
        self.writeRegData(0xB3,[0x01,0x2C,0x2D,0x01,0x2C,0x2D])
        self.writeRegData(0xB4,[0x07])
        self.writeRegData(0xC0,[0xA2,0x02,0x84])
        self.writeRegData(0xC1,[0xC5])
        self.writeRegData(0xC2,[0x0A,0x00])
        self.writeRegData(0xC3,[0x8A,0x2A])
        self.writeRegData(0xC4,[0x8A,0xEE])
        self.writeRegData(0xC5,[0x0E])
        self.writeRegData(0xE0,[0x0F,0x1A,0x0F,0x18,0x2F,0x28,0x20,0x22,0x1F,0x1B,0x23,0x37,0x00,0x07,0x02,0x10])
        self.writeRegData(0xE1,[0x0F,0x1B,0x0F,0x17,0x33,0x2C,0x29,0x2E,0x30,0x30,0x39,0x3F,0x00,0x07,0x03,0x10])
        self.writeRegData(0xF0,[0x01])
        self.writeRegData(0xF6,[0x00])
        self.writeRegData(0x3A,[0x05])

    def setGramScanWay(self, scandir: str) -> None: 
        """Set the scan direction of the LCD display"""
        self.scandir = scandir
        MemoryAccessReg_Data = 0x00

        if scandir.startswith('L2R_') or scandir.startswith('R2L_'):
            self.width	= LCD_TYPES[LCD_TYPE]['height'] 
            self.height = LCD_TYPES[LCD_TYPE]['width']
        else:
            self.width	= LCD_TYPES[LCD_TYPE]['width']
            self.height = LCD_TYPES[LCD_TYPE]['height']
            MemoryAccessReg_Data |= 0x20

        if 'R2L' in scandir:
            MemoryAccessReg_Data |= 0x40

        if 'D2U' in scandir:
            MemoryAccessReg_Data |= 0x80
        
        if (MemoryAccessReg_Data & 0x10) != 1:
            self.xadjust = LCD_TYPES[LCD_TYPE]['y_adjust']
            self.yadjust = LCD_TYPES[LCD_TYPE]['x_adjust']
        else:
            self.xadjust = LCD_TYPES[LCD_TYPE]['x_adjust']
            self.yadjust = LCD_TYPES[LCD_TYPE]['y_adjust']
        
        self.writeRegData(0x36,[{
            'LCD_1IN44': MemoryAccessReg_Data | 0x08,
            'LCD_1IN8': MemoryAccessReg_Data & 0xf7
        }[LCD_TYPE]])

    def init(self, scandir) -> int:
        """Initialize the LCD display"""
        GPIO.output(self.BL_PIN, GPIO.HIGH)
        self.reset()
        self.initReg()
        self.setGramScanWay(scandir)
        delay(200)
        self.writeReg(0x11)
        delay(120)
        self.writeReg(0x29)
		
    def setArea(self, Xstart: int, Ystart: int, Xend: int, Yend: int) -> None:
        """Set the display area"""
        self.writeRegData(0x2A,[0x00, (Xstart & 0xff) + self.xadjust, 0x00, ((Xend - 1) & 0xff) + self.xadjust])
        self.writeRegData(0x2B,[0x00, (Ystart & 0xff) + self.yadjust, 0x00, ((Yend - 1) & 0xff) + self.yadjust])
        self.writeReg(0x2C)

    def clear(self) -> None:
        """Clear the display"""
        _buffer = [0xff]*(self.width * self.height * 2)
        self.setArea(0, 0, self.width, self.height)
        GPIO.output(self.DC_PIN, GPIO.HIGH)
        for i in range(0,len(_buffer),4096):
            SPI.writebytes(_buffer[i:i+4096])

    def showImage(self, image) -> None:
        if (image == None): return
        imwidth, imheight = image.size
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display \
                ({0}x{1}).' .format(self.width, self.height))
        img = np.asarray(image)
        pix = np.zeros((self.width,self.height,2), dtype = np.uint8)
        pix[...,[0]] = np.add(np.bitwise_and(img[...,[0]],0xF8),np.right_shift(img[...,[1]],5))
        pix[...,[1]] = np.add(np.bitwise_and(np.left_shift(img[...,[1]],3),0xE0),np.right_shift(img[...,[2]],3))
        pix = pix.flatten().tolist()
        self.setArea(0, 0, self.width , self.height)
        GPIO.output(self.DC_PIN, GPIO.HIGH)
        for i in range(0,len(pix),4096):
            SPI.writebytes(pix[i:i+4096])