# portions of the screen test code were borrowed from Adafruit
# https://learn.adafruit.com/2-0-inch-320-x-240-color-ips-tft-display/circuitpython-displayio-quickstart
# button testing is primarily from
# https://circuitpython-button-handler.readthedocs.io/en/stable/
# the button test code was greatly improved thanks to the help of Ben Cowan

import time
import board
import adafruit_dotstar
import microcontroller
import wifiFunctions as wf
import displayio
import terminalio
from adafruit_display_text import label
from fourwire import FourWire
import cp_mcp3x21 as ADClib
from adafruit_st7789 import ST7789
from keypad import Keys
from button_handler import ButtonHandler, ButtonInput

'''
==========================================================
Set up variables and configure device to work with all
of the tests
==========================================================
'''
# create an SPI communication bus and set the appropriate
# ESP32 pins to control the screen
spi = board.SPI()
LCD_cs = microcontroller.pin.GPIO42
LCD_dc = microcontroller.pin.GPIO40
LCD_rst = microcontroller.pin.GPIO41

# Release any resources currently in use for the displays
displayio.release_displays()

# create the I2C communication bus
i2c = board.I2C()
# initialize the ADC on the I2C bus
ADC = ADClib.MCP3221(i2c)

# create the DotStars object and reset any previous display
LEDs = adafruit_dotstar.DotStar(board.D17, board.D18, 20)
blank = [0,0,0,0.8]
LEDs.fill(blank)

# keeps track of which buttons have been tested
buttons_pressed = set()

'''
==========================================================
Define lots of helper functions, one for each module to be
tested.
==========================================================
'''

# function to print some blankspace on the screen
def printBlank(numLines):
    for x in range(0,numLines):
        print('\n')
    return

# count down function used to provide time in between
# module tests so the user can discern the pause
# between tests and differentiate results
def countDown(numCounts,pauseLen):
    for x in range(0,numCounts):
        print(numCounts-x,'...')
        time.sleep(pauseLen)
    return


def screenTestMinimal(textToDisplay=None):
    displayio.release_displays()
    # create the display bus which utilizes the SPI bus
    display_bus = FourWire(spi, command=LCD_dc, chip_select=LCD_cs, reset=LCD_rst)

    # create the display and set the resolution
    # if your output appears rotated you can adjust the rotation parameter here
    display = ST7789(display_bus, width=320, height=240, rotation=270)
    if textToDisplay is not None:
        print(textToDisplay)
    return 

def screenTestFull():
    displayio.release_displays()
    # create the display bus which utilizes the SPI bus
    display_bus = FourWire(spi, command=LCD_dc, chip_select=LCD_cs, reset=LCD_rst)

    # create the display and set the resolution
    # if your output appears rotated you can adjust the rotation parameter here
    display = ST7789(display_bus, width=320, height=240, rotation=270)
    # Make the display context
    splash = displayio.Group()
    display.root_group = splash

    color_bitmap = displayio.Bitmap(320, 240, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x00FF00  # Bright Green

    # set a green backgroun on the display
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(280, 200, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0xAA0088  # Purple
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=20, y=20)
    splash.append(inner_sprite)

    # Draw a label
    text_group = displayio.Group(scale=3, x=57, y=120)
    text = "Hello, World!"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)
    # pause so the user can see the display update
    time.sleep(2)
    displayio.release_displays()
    return

def ADCtest():
    # read the ADC value print it to the screen with a precision
    # of two decimal places
    print("The ADC is currently measuring ", round((ADC.value  / 4095) * 3.3,2), " V")
    return 

def DotStarTest():
    # create variables used to send colors to LEDs
    blank = [0,0,0,0.8]
    LEDs.fill(blank)
    fillColor = blank[:]
    
    # cycle through each of the 20 LEDs individually and
    # change color for each LED
    for y in range (0,3):
        for x in range (0,20):
            fillColor[x%3] = 255
            LEDs[x] = fillColor
            time.sleep(0.01)
            LEDs[x] = blank
            fillColor = blank[:]
        for z in range (0,20):
            fillColor[z%3] = 255
            LEDs[19-z] = fillColor
            time.sleep(0.01)
            LEDs[19-z] = blank
            fillColor = blank[:]
    # cycle through LEDs in columns from left to right
    for y in range (0,5):
        for x in range (0,10):
            fillColor[x%3] = 255
            LEDs[x:20:10] = [fillColor,fillColor]
            time.sleep(0.03)
            LEDs[x:20:10] = [blank,blank]
            fillColor = blank[:]
    return

def acknowledge_button(button_num, button_name):
    buttons_pressed.add(button_num)

    print("Buttons tested:", len(buttons_pressed), "/ 6")

# print statements for double presses
def double_press_U():
    print("UP Button has been double pressed!")
    acknowledge_button(0, "UP")
def double_press_L():
    print("LEFT Button has been double pressed!")
    acknowledge_button(1, "LEFT")
def double_press_D():
    print("DOWN Button has been double pressed!")
    acknowledge_button(2, "DOWN")
def double_press_R():
    print("RIGHT Button has been double pressed!") 
    acknowledge_button(3, "RIGHT")
def double_press_A():
    print("A Button has been double pressed!")
    acknowledge_button(4, "A")
def double_press_B():
    print("B Button has been double pressed!")
    acknowledge_button(5, "B")

# print statements for quick presses
def short_press_U():
    print("UP Button has been pressed quickly!")
    acknowledge_button(0, "UP")
def short_press_L():
    print("LEFT Button has been pressed quickly!")
    acknowledge_button(1, "LEFT")
def short_press_D():
    print("DOWN Button has been pressed quickly!")
    acknowledge_button(2, "DOWN")
def short_press_R():
    print("RIGHT Button has been pressed quickly!")
    acknowledge_button(3, "RIGHT")
def short_press_A():
    print("A Button has been pressed quickly!")
    acknowledge_button(4, "A")
def short_press_B():
    print("B Button has been pressed quickly!")
    acknowledge_button(5, "B")

# print statements for long presses
def long_press_U():
    print("UP Button has been pressed for a long time!")
    acknowledge_button(0, "UP")
def long_press_L():
    print("LEFT Button has been pressed for a long time!")
    acknowledge_button(1, "LEFT")
def long_press_D():
    print("DOWN Button has been pressed for a long time!")
    acknowledge_button(2, "DOWN")
def long_press_R():
    print("RIGHT Button has been pressed for a long time!")
    acknowledge_button(3, "RIGHT")
def long_press_A():
    print("A Button has been pressed for a long time!")
    acknowledge_button(4, "A")
def long_press_B():
    print("B Button has been pressed for a long time!")
    acknowledge_button(5, "B")
    
'''
Define pin mapping for the six buttons:

Up = D12 (button 0 in Keys class)
Left = D14 (button 1 in Keys class)
Down = D11 (button 2 in Keys class)
Right = D13 (button 3 in Keys class)
A = D15 (button 4 in Keys class)
B = D16 (button 5 in Keys class)

All buttons are active low with pull up resistors on PCB
'''
# create the Keys object
scanner = Keys([board.D12, board.D14, board.D11, board.D13, microcontroller.pin.GPIO21, microcontroller.pin.GPIO47], value_when_pressed=False)
callback_inputs = {
    ButtonInput(ButtonInput.DOUBLE_PRESS, 0, double_press_U),
    ButtonInput(ButtonInput.DOUBLE_PRESS, 1, double_press_L),
    ButtonInput(ButtonInput.DOUBLE_PRESS, 2, double_press_D),
    ButtonInput(ButtonInput.DOUBLE_PRESS, 3, double_press_R),
    ButtonInput(ButtonInput.DOUBLE_PRESS, 4, double_press_A),
    ButtonInput(ButtonInput.DOUBLE_PRESS, 5, double_press_B),
    ButtonInput(ButtonInput.SHORT_PRESS, 0, short_press_U),
    ButtonInput(ButtonInput.SHORT_PRESS, 1, short_press_L),
    ButtonInput(ButtonInput.SHORT_PRESS, 2, short_press_D),
    ButtonInput(ButtonInput.SHORT_PRESS, 3, short_press_R),
    ButtonInput(ButtonInput.SHORT_PRESS, 4, short_press_A),
    ButtonInput(ButtonInput.SHORT_PRESS, 5, short_press_B),
    ButtonInput(ButtonInput.LONG_PRESS, 0, long_press_U),
    ButtonInput(ButtonInput.LONG_PRESS, 1, long_press_L),
    ButtonInput(ButtonInput.LONG_PRESS, 2, long_press_D),
    ButtonInput(ButtonInput.LONG_PRESS, 3, long_press_R),
    ButtonInput(ButtonInput.LONG_PRESS, 4, long_press_A),
    ButtonInput(ButtonInput.LONG_PRESS, 5, long_press_B),
}

button_handler = ButtonHandler(scanner.events, callback_inputs, 6)


def testButtons():
    while len(buttons_pressed) < 6:
        button_handler.update()
        time.sleep(0.0025)
    printBlank(2)
    print("All six buttons have been acknowledged!")
    print("All 5 tests completed successfully!")
    print("We now return you to your regularly scheduled programming.")
    time.sleep(3)
    return

'''
==========================================================
Main part of the code.  Calls each function once
to test functinality of each module with a pause between
each test to give the user time to acknowledge test
completion.  The final module tests the buttons in an
infinite loop.  The program has to be manually cancelled
by hitting CTRL-C in the terminal.
==========================================================
'''

screenTestMinimal('This is an initial test of the display connectivity')
countDown(5,1)
printBlank(4)
screenTestFull()
print('Full screen test complete!')
screenTestMinimal()
countDown(5,1)
printBlank(4)
ADCtest()
printBlank(4)
print('Now testing DotStars')
countDown(5,1)
printBlank(4)
DotStarTest()
print('Now testing WiFi')
internet = wf.WifiManager()
currTime = internet.utc_time
printBlank(4)
print('Congratulations!  4 of 5 tests completed successfully.')
time.sleep(1)
print('Final test:  buttons')
print('\n')
print('Please press each of the six buttons at least once and confirm they are acknowledged on the screen.')
printBlank(3)
testButtons()
print("Test program finished...")