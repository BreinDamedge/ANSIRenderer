"""dino game"""

from tart import Canvas, Rect
from keys import Keyboard

import time


c = Canvas()
k = Keyboard()

c.setup()
k.begin()

st = time.time()
DINO_HEIGHT = 4
DINO_WIDTH = 3
JUMP_HEIGHT = 4
dino = Rect(0, c.HEIGHT - DINO_HEIGHT, DINO_HEIGHT, DINO_WIDTH, "red")


while True:
    try:
        # handle button presses

        # duck
        if k.down("s") or k.down("shift"):
            dino.height = DINO_HEIGHT // 2
        else:
            dino.height = DINO_HEIGHT
        dino.y = c.HEIGHT - dino.height

        # jump
        if k.down("w") or k.down("space"):
            dino.y = c.HEIGHT - dino.height - JUMP_HEIGHT

        # draw the dino
        c.drawRect(*dino)

        # display
        c.show()
        # cleanup key input
        k.cleanup()
        # wait for next frame
        time.sleep(1 / 60)

    except KeyboardInterrupt:
        break

print(
    f"Out of {timesteps} timesteps, we hit the corner {num_corners} times, giving us a probability of {num_corners / timesteps}"
)
