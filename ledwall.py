from picow_ledwall.ledwall import LedWall
from picow_ledwall.text import TextString
from picow_ledwall.effects import Scroll

# Define the GPIO pin
GPIO_PIN = 28

# Define the array size
nrows = 8
ncols = 32

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
        l.display(TextString("CIAO", color=r))
        # l.display(TextString("Mondo", position=(2, 0), color=g))
        # l.display(TextString("I am", position=(3, 1), color=b))
        # l.display(TextString("LED man!!!!!!!!!", color=r))
        # l.display(TextString("OutofRange", position=(0, 5), color=g))
        # l.display(TextString("BTC: +10%", position=(0, 0), color=b))
        # l.display(TextString("08/03/2024", position=(0, 1), color=r))
        # Scroll(l, TextString("CIAO", color=r))
        Scroll(l, TextString("This is some really long text", color=g), speed=5)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        break
    except Exception as e:
        print(e)
        break
# exit
l.quit()
print("Finished.")
