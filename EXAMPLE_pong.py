from tart import Canvas
from keys import Keyboard
import time
from dataclasses import dataclass


@dataclass
class Paddle:
    x: int
    y: int
    height: int = 4
    width: int = 1
    color: str = "white"

    def __getitem__(self, i: int):
        data: dict[str, object] = vars(self)
        keys = iter(data.keys())
        key = next(keys)
        while i > 0:
            key = next(keys)
            i -= 1
        return data[key]


left = Paddle(0, 0)


c = Canvas()
k = Keyboard()

k.begin()
c.setup()
while True:
    # paddle move
    if k.down("s"):
        left.y += 1

    c.drawRect(*left)
    c.show()

    # wait for next frame
    time.sleep(0.5)
