"""Example Scene With Moving Rectangle"""

# imports to get us the code for drawing
from tart import Canvas, Rect
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
c.set_background_color("blue")
my_guy = Rect(c.WIDTH / 2, c.HEIGHT / 2, 5 // 2, 5, "red")
my_guy_speed = 0.5  # speed is squares per frame
dots = []


def make_dot(x, y):
    return Rect(x, y, 1, 1, "white")


# Game Loop
while True:
    # Your Code Goes Here
    # ...

    # move the guy around when you press keys
    if k.down("s") or k.down("down"):
        my_guy.y += my_guy_speed / 2
    if k.down("w") or k.down("up"):
        my_guy.y -= my_guy_speed / 2
    if k.down("a") or k.down("left"):
        my_guy.x -= my_guy_speed
    if k.down("d") or k.down("right"):
        my_guy.x += my_guy_speed
    # draw the guy
    c.drawRect(*my_guy)

    # now let the guy drop little dots
    if k.triggered("space"):
        # add a dot to the screen where my guy is
        dots.append(make_dot(my_guy.x, my_guy.y))
    # now draw all the dots
    for dot in dots:
        c.drawRect(*dot)

    # End of Loop (do not change this code)
    c.show()
    k.cleanup()
    time.sleep(1 / FRAME_RATE)
