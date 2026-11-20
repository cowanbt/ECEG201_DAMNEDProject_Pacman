
"""
ECEG 201 - DAMNED Arcade
Hardware Integration Test

Tests the ST7789 LCD and six physical buttons.
"""

import time
import displayio
import terminalio
from adafruit_display_text import label

from hardware.display import initialize_display
from hardware.buttons import ButtonController


# ==========================================================
# Initialize hardware
# ==========================================================

display = initialize_display()
buttons = ButtonController()


# ==========================================================
# Configure LCD
# ==========================================================

screen = displayio.Group()
display.root_group = screen

# Display title
title = label.Label(
    terminalio.FONT,
    text="DAMNED ARCADE",
    color=0xFFFF00,
    scale=2,
    x=50,
    y=70
)

# Display button status
status = label.Label(
    terminalio.FONT,
    text="Press any button",
    color=0xFFFFFF,
    scale=2,
    x=40,
    y=130
)

# Add labels to display
screen.append(title)
screen.append(status)


# ==========================================================
# Main Test Loop
# ==========================================================

print("DAMNED Arcade Hardware Test")
print("Press each of the six buttons.")

tested_buttons = set()

while True:

    button = buttons.get_button()

    if button is not None:

        # Update LCD
        status.text = "Button: " + button

        # Print to serial monitor
        print("Pressed:", button)

        # Record successfully tested buttons
        tested_buttons.add(button)

        print("Buttons tested:", len(tested_buttons), "/ 6")

        # Check if all six buttons have been tested
        if len(tested_buttons) == 6:

            status.text = "ALL BUTTONS OK!"
            print("All six buttons tested successfully!")

            break

    time.sleep(0.01)


# ==========================================================
# Test Complete
# ==========================================================

while True:
    time.sleep(1)
