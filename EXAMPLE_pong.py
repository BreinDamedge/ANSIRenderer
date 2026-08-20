from tart import Canvas, clear_term, Rect
from keys import Keyboard
import time
from dataclasses import dataclass
import random


@dataclass
class Paddle(Rect):
    height: float = 4
    width: float = 1
    color: str = "white"


@dataclass
class Ball(Rect):
    x: float = 20 - 1  # should be half way through the screen
    y: float = (3 / 8) * 20
    height: float = 1
    width: float = 2
    color: str = "white"
    vx: float = random.choice([1, -1])
    vy: float = random.choice([1, -1]) * 0.5

    def speed_up(self) -> None:
        self.vx *= 1.1
        self.vy *= 1.1

    def reset(self) -> None:
        self.x = 20 - 1  # should be half way through the screen
        self.y = (3 / 8) * 20
        self.vx = random.choice([1, -1])
        self.vy = random.choice([1, -1]) * 0.5


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

        # update ball position
        b.y += b.vy
        b.x += b.vx

        hit_left = left.colliding(b.x, b.y, 2, 1)
        hit_right = right.colliding(b.x, b.y, 2, 1)
        # paddle collision (to change the ball's velocity for next timestep)
        if hit_left or hit_right:
            b.vx *= -1
            b.speed_up()

        # check if the ball is offscreen
        if (b.x < 0 and not hit_left) or (b.x >= c.WIDTH and not hit_right):
            print("point")
            time.sleep(2)
            b.reset()

        c.drawRect(*left)
        c.drawRect(*right)
        c.drawRect(*b)

        c.show()

        # wait for next frame
        k.cleanup()
        time.sleep(0.2)
    except KeyboardInterrupt:
        clear_term()
        break
