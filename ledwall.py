import time

from picow_ledwall.ledwall import LedWall
from picow_ledwall.text import TextString

# Define the GPIO pin
GPIO_PIN = 28

# Define the array size
nrows = 8
ncols = 32
numpix = nrows * ncols


# Define the colors


# for some reason does not run in RGB mode
def convert_RGB_to_GRB(tuple_rgb: tuple) -> tuple:
    """convert RGB tuple to GRB tuple"""
    return tuple_rgb[1], tuple_rgb[0], tuple_rgb[2]


# Define some colors
zero = (0, 0, 0)
r = convert_RGB_to_GRB((255, 0, 0))
g = convert_RGB_to_GRB((0, 255, 0))
b = convert_RGB_to_GRB((0, 0, 255))


# LEDWALL
l = LedWall(nrows, ncols, GPIO_PIN)
print("LedWall created.")

while True:
    try:
        TextString("CIAO", l).display(2, r)
        time.sleep(1)
        l.clear_all()
        TextString("Bella", l).display(2, g)
        time.sleep(1)
        l.clear_all()
        TextString("I am", l).display(2, b)
        time.sleep(1)
        l.clear_all()

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        break
    except Exception as e:
        print(e)
        break
# exit
l.clear_all()
print("Finished.")
