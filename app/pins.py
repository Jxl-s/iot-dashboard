try:
    import RPi.GPIO as GPIO
except:
    import Mock.GPIO as GPIO

# Set the pins here
PINS = {
    "LED": 17,

    # DHT
    "DHT11": 4,

    # Motor
    "MOTOR_EN": 23,
    "MOTOR_IN1": 24,
    "MOTOR_IN2": 25,
}

# Define a setup method
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PINS["LED"], GPIO.OUT)

    # Motor
    GPIO.setup(PINS["MOTOR_EN"], GPIO.OUT)
    GPIO.setup(PINS["MOTOR_IN1"], GPIO.OUT)
    GPIO.setup(PINS["MOTOR_IN2"], GPIO.OUT)
