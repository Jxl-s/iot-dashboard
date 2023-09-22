# This is a file that can kind of emulate a board, using it to develop on other devices
# than my raspberry PI
BCM = "BCM"
OUT = "OUT"
IN = "IN"
HIGH = 1
LOW = 0

_pin_states = {}


def setmode(mode):
    _pin_states = {}


def setwarnings(state):
    pass


def setup(pin, mode):
    _pin_states[pin] = False  # Initialize pin state to false


def output(pin, state):
    _pin_states[pin] = state


def input(pin):
    return _pin_states[pin]


def cleanup():
    _pin_states = {}


# returns a list of pins that are currently set to output, it will return a string
def print_board():
    out = ""
    out += "Board:<br />"
    out += "-----<br />"
    for pin in _pin_states:
        out += "Pin: " + str(pin) + " State: " + str(_pin_states[pin]) + "<br />"
    out += "-----<br />"

    return out
