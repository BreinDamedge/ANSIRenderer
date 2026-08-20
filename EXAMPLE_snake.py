from tart import Canvas, clear_term, Rect, Unpackable
from keys import Keyboard
import time
from enum import Enum
from dataclasses import dataclass


@dataclass
class Point(Unpackable):
    x: float
    y: float


# class syntax
class Direction(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3


# some defines
FRAME_WAIT: float = 1 / 2


# silly little helper function
def game_running() -> bool:
    time.sleep(FRAME_WAIT)
    return True


if __name__ == "__main__":
    # variables I need for game
    c = Canvas()
    k = Keyboard()
    snake_tiles: list[Point] = [Point(0, 0), Point(-1, 0)]
    snake_direction: Direction = Direction.RIGHT
    fruit: Point = Point(5, 5)

    c.setup()
    k.begin()
    while game_running():
        # check for keypresses and set the direction the snake is moving
        # ELIF CHAIN MAY CAUSE BUG W/KEY PRIORITIES
        if (k.down("w") or k.triggered("w")) and snake_direction != Direction.DOWN:
            snake_direction = Direction.UP
        elif (k.down("a") or k.triggered("a")) and snake_direction != Direction.RIGHT:
            snake_direction = Direction.LEFT
        elif (k.down("s") or k.triggered("s")) and snake_direction != Direction.UP:
            snake_direction = Direction.DOWN
        elif (k.down("d") or k.triggered("d")) and snake_direction != Direction.LEFT:
            snake_direction = Direction.RIGHT

        # if you ate food grow the tail before moving
        if k.down("q"):
            # pretend you ate food via keypress for now
            snake_tiles.append(Point(*snake_tiles[-1]))

        # move the snake based on its current direction
        # set the back tile to where the front tile is
        snake_tiles[-1].x = snake_tiles[0].x
        snake_tiles[-1].y = snake_tiles[0].y
        # set the front tile to a new position (based on direction)
        if snake_direction == Direction.UP:
            snake_tiles[0].y -= 1
        elif snake_direction == Direction.LEFT:
            snake_tiles[0].x -= 2
        elif snake_direction == Direction.DOWN:
            snake_tiles[0].y += 1
        elif snake_direction == Direction.RIGHT:
            snake_tiles[0].x += 2
        else:
            raise ValueError("brother your snake is pointing a crazy direction")

        # move the back to just behind the head
        snake_tiles.insert(1, snake_tiles.pop())

        # draw the snake
        for i, p in enumerate(snake_tiles):
            if i:
                # draw tile
                c.drawRect(*p, 1, 2, "white")
            else:
                # draw head
                c.drawRect(*p, 1, 2, "green")

        # draw and ready keys for next frame
        c.show()
        k.cleanup()
