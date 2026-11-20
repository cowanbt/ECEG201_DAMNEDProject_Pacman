"""
DAMNED ESP32-S3 Display Interface
ECEG 201 Final Project
"""

import board
import microcontroller
import displayio
from fourwire import FourWire
from adafruit_st7789 import ST7789

def initialize_display():
    """Initialize and return the 320x240 ST7789 LCD."""

    displayio.release_displays()
    spi = board.SPI()

    display_bus = FourWire(
        spi,
        command=microcontroller.pin.GPI40,
        chip_select=microcontroller.pin.GPIO42,
        reset=microcontroller.pin.GPI041
    )

    display = ST7789(
        display_bus,
        width=320,
        height=240,
        rotation=270
    )

    return display