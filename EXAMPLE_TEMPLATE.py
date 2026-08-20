"""Template Game Loop"""

# imports to get us the code for drawing
from tart import Canvas
from keys import Keyboard
import time

# CONSTANTS
FRAME_RATE = 30

# setup drawing and button pressing (do not change this code)
c = Canvas()
k = Keyboard()
c.setup()
k.begin()

# put your variables HERE:
# ...


# Game Loop
while True:
    # Your Code Goes Here
    # ...

    # End of Loop (do not change this code)
    c.show()
    k.cleanup()
    time.sleep(1 / FRAME_RATE)
