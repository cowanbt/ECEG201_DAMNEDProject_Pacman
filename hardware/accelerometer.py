"""
DAMNED Arcade - ADXL345 Acceleromter Interface
ECEG 201 Final Project
"""
import board
import adafruit_adxl34x

class AccelerometerController:
    """ Manage ADXL345 acceleration measurements and tilt controls."""
    def __init__(self, threshold=3.0):
        """
        Initialize the accelerometer over I2C

        Args:
            threshold: Minimum acceleration along an axis
                       required to register a tilt, in m/s^2.
        """
        self.i2c = board.I2C()
        self.sensor = adafruit_adxl34x.ADXL345(self.i2c)
        self.threshold = threshold
        self.x_offset = 0.0
        self.y_offset = 0.0
        self.calibrate()

    def get_acceleration(self):
        """Return X, Y, Z acceleration in m/s^2."""
        return self.sensor.acceleration

    def calibrate(self):
        """
        Record the current X and Y acceleration as the
        neutral position. Hold the board still when calling.
        """
        x, y, z = self.get_acceleration()
        self.x_offset = x
        self.y_offset = y

    def get_direction(self):
        """
        Determine movement from X-Y tilt relative to neutral.

        Returns:
            str: UP, DOWN, LEFT, or RIGHT
            None: If tilt is below the threshold
        """
        x, y, z = self.get_acceleration()

        # Remove neutral position offsets
        x -= self.x_offset
        y -= self.y_offset

        # Dead zone around neutral position
        if abs(x) < self.threshold and abs(y) < self.threshold:
            return None

        # Use the dominant tilt axis
        if abs(x) > abs(y):
            return "RIGHT" if x > 0 else "LEFT"

        return "DOWN" if y > 0 else "UP"