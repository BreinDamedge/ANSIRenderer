from tart import Canvas
from keys import Keyboard
import time
from dataclasses import dataclass
import random


class convenientToDraw:
    def __iter__(self) -> object:
        """overload so you can unpack object into drawRect"""
        data: dict[str, object] = vars(self)
        keys = iter(data.keys())
        for _ in range(5):
            key = next(keys)
            yield data[key]
        return


@dataclass
class Paddle(convenientToDraw):
    x: int
    y: int
    height: int = 4
    width: int = 1
    color: str = "white"


@dataclass
class Ball(convenientToDraw):
    x: int = 20 - 1  # should be half way through the screen
    y: int = int((3 / 8) * 20)
    height: int = 1
    width: int = 2
    color: str = "white"
    vx: int = random.choice([1, -1])
    vy: int = random.choice([1, -1])


c = Canvas()
k = Keyboard()

# paddles
left = Paddle(0, 0)
right = Paddle(c.WIDTH - 1, 0)

# ball
b = Ball()

k.begin()
c.setup()
while True:
    try:
        # paddle movement
        if k.down("d") or k.triggered("d"):
            if left.y < (c.HEIGHT - left.height):
                left.y += 1
        if k.down("f") or k.triggered("f"):
            if left.y > 0:
                left.y -= 1
        if k.down("j") or k.triggered("j"):
            if right.y < (c.HEIGHT - right.height):
                right.y += 1
        if k.down("k") or k.triggered("k"):
            if right.y > 0:
                right.y -= 1

        # bounce off top or bottom of screen
        if (b.y + b.vy < 0) or (b.y + b.vy >= c.HEIGHT):
            b.vy *= -1
        # bounce of left or right of screen
        # TODO: replace this with paddle collision logic
        if (b.x + b.vx < 0) or (
            b.x + b.vx >= c.WIDTH - (b.width - 1)
        ):  # -1 here bc otherwise it tries to draw off screen
            b.vx *= -1

        # update ball position
        b.y += b.vy
        b.x += b.vx

        c.drawRect(*left)
        c.drawRect(*right)
        c.drawRect(*b)

        c.show()

        # wait for next frame
        k.cleanup()
        time.sleep(0.2)
    except KeyboardInterrupt:
        break
