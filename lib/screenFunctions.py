from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import board
from adafruit_st7789 import ST7789
from fourwire import FourWire
import displayio
import microcontroller

class ECEG201screen:
    def __init__(self, width=320, height=240, rotation=270):
        '''
        Initialize screen connection for ST7789 display
        Args:
            none
        '''
        # ESP32 pins used to control the screen
        self._spi = board.SPI()
        self._CS = microcontroller.pin.GPIO42
        self._DC = microcontroller.pin.GPIO40
        self._RST = microcontroller.pin.GPIO41
        # properties of the specific ST7789 display
        self._width = width
        self._height = height
        self._rotation = rotation
        # create the display bus and display
        self._display_bus, self._display = self.setup()

    @property
    def display(self):
        '''Get display object'''
        return self._display
    
    def setup(self):
        '''
        Connect to the screen
        '''
        # Release any resources currently in use for the displays
        displayio.release_displays()
        #create a display object and return it
        display_bus = FourWire(self._spi, command=self._DC, chip_select=self._CS, reset=self._RST)
        return display_bus, ST7789(display_bus, width=self._width, height=self._height, rotation=self._rotation)
    
    def displayTime(self, dispTime='12:00\nam', font="oldschool_wyse700b-2y-32.pcf", fontColor=0x0000FF, fontScale=3):
        '''
        Show the provided time on the screen
        '''
        font = bitmap_font.load_font("/lib/" + font)
        color = fontColor
        scale = fontScale
        
        text_area = label.Label(font, text=dispTime, color=color, scale=scale)
        text_area.x = 0
        text_area.y = 50
        self._display.root_group = text_area