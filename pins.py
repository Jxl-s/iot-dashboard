try:
    import RPi.GPIO as GPIO
except ImportError:
    import _gpio as GPIO

# Set the pins here
PINS = {
    "LED": 17,
}


# Define a setup method
def setup():
    GPIO.setup(PINS["LED"], GPIO.OUT)