
"""
ECEG 201 - DAMNED Arcade
Hardware Integration Test

Tests the ST7789 LCD and six physical button,
and the ADXL345 accelerometer.

Controls:
    A - Restart test and recalibrate accelerometer
    B - Finish test
"""

import time
import displayio
import terminalio
from adafruit_display_text import label

from hardware.display import initialize_display
from hardware.buttons import ButtonController
from hardware.accelerometer import AccelerometerController

# ==========================================================
# Initialize hardware
# ==========================================================

display = initialize_display()
buttons = ButtonController()
accelerometer = AccelerometerController()

# ==========================================================
# Configure LCD
# ==========================================================

screen = displayio.Group()
display.root_group = screen

def make_label(text, x, y, color=0xFFFFFF, scale=1):
    """Create a text label for the ST7789 display."""
    return label.Label(
        terminalio.FONT,
        text=text,
        color=color,
        scale=scale,
        x=x,
        y=y
    )


title = make_label(
    "DAMNED ARCADE", 50, 30, 0xFFFF00, 2
)

button_status = make_label(
    "Buttons tested: 0/6", 20, 70
)

last_button = make_label(
    "Last button: NONE", 20, 90
)

accel_xy = make_label(
    "X: 0.00  Y: 0.00", 20, 125
)

accel_z = make_label(
    "Z: 0.00", 20, 145
)

tilt_status = make_label(
    "Tilt: NONE", 20, 165
)

instructions = make_label(
    "A x2: Restart  B x2: Finish", 20, 210
)

for item in (
    title,
    button_status,
    last_button,
    accel_xy,
    accel_z,
    tilt_status,
    instructions
):
    screen.append(item)


# ==========================================================
# Test State
# ==========================================================

tested_buttons = set()
test_running = True
last_update = 0

a_count = 0
b_count = 0


def update_button_count():
    """Update the number of unique buttons tested."""
    button_status.text = "Buttons tested: {}/6".format(
        len(tested_buttons)
    )


def restart_test():
    """Clear test results and recalibrate accelerometer."""
    global test_running, last_update

    tested_buttons.clear()
    tested_buttons.add("A")

    test_running = True
    last_update = 0

    accelerometer.calibrate()

    update_button_count()
    last_button.text = "Last button: A"
    accel_xy.text = "X: 0.00  Y: 0.00"
    accel_z.text = "Z: 0.00"
    tilt_status.text = "Tilt: NONE"

    print("\nHardware test restarted.")


def finish_test():
    """Freeze accelerometer readings and display results."""
    global test_running

    test_running = False
    tested_buttons.add("B")

    update_button_count()
    last_button.text = "Last button: B"
    tilt_status.text = "TEST COMPLETE"

    print("\nHardware test complete.")
    print("Buttons tested:", sorted(tested_buttons))
    print("Total:", len(tested_buttons), "/6")


# ==========================================================
# Main Test Loop
# ==========================================================

print("DAMNED Arcade Hardware Test")
print("Press the directional buttons to test them.")
print("Tilt the accelerometer to test movement.")
print("Press B to finish or A to restart.")

while True:

    # ------------------------------------------------------
    # Button Events
    # ------------------------------------------------------

    button = buttons.get_button()

    if button is not None:

        print("Pressed:", button)

        if button == "A":
            a_count += 1
            if a_count >= 2:
                restart_test()

            elif test_running:
                tested_buttons.add("A")
                update_button_count()
                last_button.text = "Last button: A"
        

        elif button == "B" and test_running:
            b_count += 1
            if b_count >= 2:
                finish_test()

            elif test_running:
                tested_buttons.add("B")
                update_button_count()
                last_button.text = "Last button: B"

        elif test_running:
            tested_buttons.add(button)

            update_button_count()
            last_button.text = "Last button: " + button

    # ------------------------------------------------------
    # Accelerometer Measurements
    # ------------------------------------------------------

    current_time = time.monotonic()

    if test_running and current_time - last_update >= 0.2:

        last_update = current_time

        x, y, z = accelerometer.get_acceleration()
        direction = accelerometer.get_direction()

        accel_xy.text = "X:{:.2f} Y:{:.2f}".format(x, y)
        accel_z.text = "Z:{:.2f}".format(z)

        tilt_status.text = "Tilt: {}".format(
            direction if direction else "NONE"
        )

    time.sleep(0.01)