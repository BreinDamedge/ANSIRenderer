"""dvd logo that counts the corner hits"""

from tart import Canvas
import time


c = Canvas()
st = time.time()
pos: list[int] = [0, 0]
vel: list[int] = [1, 1]

c.setup()

num_corners = 0
timesteps = 0

while True:
    try:
        print(f"Timestep: {timesteps}, Corner Hits: {num_corners}")
        c.drawRect(*pos, 1, 1, "red")
        c.show()

        # check if we've hit a corner
        if (
            (pos[0] == 0 and pos[1] == 0)
            or (pos[0] == 0 and pos[1] == c.C - 1)
            or (pos[0] == c.R - 1 and pos[1] == 0)
            or (pos[0] == c.R - 1 and pos[1] == c.C - 1)
        ):
            num_corners += 1

        # motion
        for i in range(len(pos)):
            pos[i] += vel[i]

        # bounce
        if pos[0] == (c.R - 1) or pos[0] == 0:
            vel[0] *= -1
        if pos[1] == (c.C - 1) or pos[1] == 0:
            vel[1] *= -1

        # wait for next frame
        timesteps += 1
        time.sleep(1 / 60)

    except KeyboardInterrupt:
        break

print(
    f"Out of {timesteps} timesteps, we hit the corner {num_corners} times, giving us a probability of {num_corners / timesteps}"
)
