import msvcrt  # Windows non-blocking input
import random
import time
from ansiRenderer import Canvas


def get_keys() -> list[str]:
    keys: list[str] = []
    while msvcrt.kbhit():
        keys.append(msvcrt.getch().decode("utf-8", errors="ignore"))
    return keys


def clear_keys() -> None:
    while msvcrt.kbhit():
        _ = msvcrt.getch()


def get_key() -> str:
    char = ""
    if msvcrt.kbhit():
        char = msvcrt.getch().decode("utf-8", errors="ignore")
    return char


def random_grid_position(r_: int, c_: int) -> tuple[int, int]:
    return (random.randint(0, r_ - 1), random.randint(0, c_ - 1))


if __name__ == "__main__":
    c = Canvas()
    c.setup()
    R, C = c.shape()
    apple_pos = random_grid_position(R, C)
    while True:
        c.drawRect(*apple_pos, 1, 1, "red")
        c.ready()
        c.show()
        time.sleep(1 / 2)
