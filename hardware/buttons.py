"""
DAMNED ESP32-S3 Button Interface
ECEG 201 Final Project
"""

import board
import microcontroller
from keypad import Keys

class ButtonController:
    """Interface for the DAMNED's six physical buttons"""

    BUTTON_NAMES = (
        "UP",
        "LEFT",
        "DOWN",
        "RIGHT",
        "A",
        "B"
    )

    def __init__(self):
        """
        CircuitPython's Keys class monitors multiple GPIO inputs and generates a key press event
        whenever a button is pressed or released, i.e. a button state change.

        Each GPIO pin is assigned an index based on position in the tuple (0-5). The event_key_number
        attribute identifies which button triggered the event, allowing for mapping its index to a name
        using BUTTON_NAMES.

        The buttons are configured to active-low (value_when_pressed=False) 
        and use externall pull-up resistors (pull=False)
        """
        self.scanner = Keys(
            (
                board.D12,                      # Index 0: UP
                board.D14,                      # Index 1: LEFT
                board.D11,                      # Index 2: DOWN
                board.D13,                      # INDEX 3: RIGHT
                microcontroller.pin.GPIO21,     # INDEX 4: A
                microcontroller.pin.GPI047      # INDEX 5: B
            ),
            value_when_pressed=False,
            pull=False
        )

    def get_button(self):
        """
        Return the latest button press from the Keys event queue.

        Returns the corresponding button name when a press event occurs, or 
        None if no press event is available. Release events are ignored.
        """

        event = self.scanner.events.get()

        if event is not None and event.pressed:
            return self.BUTTON_NAMES(event.key_number)

        return None

    def close(self):
        """Release button scanner's hardware resources."""
        self.scanner.deinit()