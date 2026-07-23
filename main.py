from ansiRenderer import Canvas
import time


C = 40
R = int((3 / 8) * C)

c = Canvas()
st = time.time()
pos: list[int] = [0, 0]
c.setup()
vel = 1
while True:
    c.reset()
    c.drawRect(*pos, 1, 1, "red")
    c.clear()
    c.show()

    pos[0] += vel
    if pos[0] == (R - 1) or pos[0] == 0:
        vel *= -1

    # wait for next frame
    time.sleep(0.5)
