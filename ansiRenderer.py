COLOR_NAMES: list[str] = [
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "default",
]
FOREGROUND_COLORS: dict[str, int] = {v: 30 + i for i, v in enumerate(COLOR_NAMES)}
FOREGROUND_COLORS["default"] = 0
BACKGROUND_COLORS: dict[str, int] = {k: v + 10 for k, v in FOREGROUND_COLORS.items()}
BACKGROUND_COLORS["default"] = 0


def colorChar(color_: str, bg_: bool = True) -> str:
    if bg_:
        return f"\033[{BACKGROUND_COLORS[color_]}m"
    else:
        return f"\033[{FOREGROUND_COLORS[color_]}m"


def prit(v_: object) -> None:
    print(v_, end="")


def set_color(color_: str) -> None:
    prit(colorChar(color_))


CLEAR_SCREEN = "\x1bc"
RESET = "\033[0m"
DEFAULT: str = colorChar("default")
DEFB: str = colorChar("black")  # default background for our window
HOME: str = "\033[H"  # might end in f


class Rect:
    def __init__(self, height_: int, width_: int, r_: float, c_: float) -> None:
        self.pos: list[float] = [r_, c_]
        self.shape: list[float] = [height_, width_]
        self.color: str = colorChar("red")

    def setPos(self, r_: float, c_: float) -> None:
        self.pos[0] = r_
        self.pos[1] = c_


class Canvas:
    def __init__(self) -> None:
        self.C: int = 40
        self.R: int = int(
            (3 / 8) * self.C
        )  # makes 4:3 aspect ratio (accounts for the cursor being roughly half as wide as it is tall)
        self.frame_chars: list[str] = [" " * self.C] * self.R
        self.frame_codes: list[list[str]] = [[DEFB] * self.C for _ in range(self.R)]

    def reset(self) -> None:
        self.frame_chars = [" " * self.C] * self.R
        self.frame_codes = [[DEFB] * self.C for _ in range(self.R)]

    def setup(self) -> None:
        prit(CLEAR_SCREEN)
        self.clear()

    def clear(self) -> None:
        prit(HOME)
        prit(DEFAULT)

    def drawRect(
        self, r_: float, c_: float, height_: int, width_: int, color_: str
    ) -> None:
        color_string: str = colorChar(color_)
        for h in range(height_):
            for w in range(width_):
                self.frame_codes[r_ + h][c_ + w] = color_string

    def show(self) -> None:
        frame_string: str = ""
        for r in range(self.R):
            for c in range(self.C):
                frame_string += self.frame_codes[r][c]
                frame_string += self.frame_chars[r][c]
                frame_string += colorChar("default")
            frame_string += "\n"
        prit(frame_string)
