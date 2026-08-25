"""dvd logo that counts the corner hits"""

from artsi import Canvas
import time


st = time.time()
pos: list[int] = [0, 0]
vel: list[int] = [1, 1]


num_corners = 0
timesteps = 0
FRAME_RATE = 15

WIDTH, HEIGHT = Canvas.get_shape()
Canvas.clear()

while True:
    try:
        print(f"Timestep: {timesteps}, Corner Hits: {num_corners}")
        Canvas.draw_rectangle(pos[0], pos[1], 1, 1, "red")
        Canvas.show()

        # check if we've hit a corner
        if (
            (pos[0] == 0 and pos[1] == 0)  # left top
            or (pos[0] == 0 and pos[1] == (HEIGHT - 1))  # left bottom
            or (pos[0] == (WIDTH - 1) and pos[1] == 0)  # right top
            or (pos[0] == (WIDTH - 1) and pos[1] == (HEIGHT - 1))  # right bottom
        ):
            num_corners += 1

        # motion
        for i in range(len(pos)):
            pos[i] += vel[i]

        # bounce
        if pos[0] == (WIDTH - 1) or pos[0] == 0:
            vel[0] *= -1
        if pos[1] == (HEIGHT - 1) or pos[1] == 0:
            vel[1] *= -1

        # wait for next frame
        timesteps += 1
        time.sleep(1 / FRAME_RATE)

    except KeyboardInterrupt:
        break

print(
    f"Out of {timesteps} timesteps, we hit the corner {num_corners} times, giving us a probability of {num_corners / timesteps}"
)
