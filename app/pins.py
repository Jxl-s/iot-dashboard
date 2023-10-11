try:
    import RPi.GPIO as GPIO
except:
    import Mock.GPIO as GPIO

# Set the pins here
PINS = {
    "LED": 17,
}

# Define a setup method
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PINS["LED"], GPIO.OUT)
