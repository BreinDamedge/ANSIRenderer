from dataclasses import dataclass


CLEAR_SCREEN = "\x1bc"
RESET = "\033[0m"
HOME: str = "\033[H"  # might end in f

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


DEFAULT: str = colorChar("default")
background_color: str = colorChar("black")  # default background for our window


def prit(v_: object) -> None:
    print(v_, end="")


def clear_term() -> None:
    prit(CLEAR_SCREEN)
    prit(HOME)


class Canvas:
    def __init__(self) -> None:
        self.WIDTH: int = 40
        self.HEIGHT: int = int(
            (3 / 8) * self.WIDTH
        )  # makes 4:3 aspect ratio (accounts for the cursor being roughly half as wide as it is tall)
        self.frame_chars: list[str] = [" " * self.WIDTH] * self.HEIGHT
        self.frame_codes: list[list[str]] = [
            [background_color] * self.WIDTH for _ in range(self.HEIGHT)
        ]

    def set_background_color(self, color_: str) -> None:
        global background_color
        background_color = colorChar(color_)

    def shape(self) -> tuple[int, int]:
        return (self.HEIGHT, self.WIDTH)

    def _reset_data(self) -> None:
        self.frame_chars = [" " * self.WIDTH] * self.HEIGHT
        self.frame_codes = [[background_color] * self.WIDTH for _ in range(self.HEIGHT)]

    def setup(self) -> None:
        prit(CLEAR_SCREEN)
        self._ready()

    def _ready(self) -> None:
        prit(HOME)
        prit(DEFAULT)

    def drawRect(
        self, x_pos_: float, y_pos_: float, height_: int, width_: int, color_: str
    ) -> None:
        color_string: str = colorChar(color_)
        for h in range(height_):
            for w in range(width_):
                cy = int(y_pos_ + h)  # candidate y
                cx = int(x_pos_ + w)  # candidate x
                if (cy >= 0 and cy < self.HEIGHT) and (cx >= 0 and cx < self.WIDTH):
                    # only draw to canvas if the square is on the canvas
                    self.frame_codes[cy][cx] = color_string

    def show(self) -> None:
        frame_string: str = ""
        for r in range(self.HEIGHT):
            for c in range(self.WIDTH):
                frame_string += self.frame_codes[r][c]
                frame_string += self.frame_chars[r][c]
                frame_string += colorChar("default")
            frame_string += "\n"
        prit(frame_string)
        self._reset_data()
        self._ready()


### shapes and collisions
def _rect_collision(
    x1_: float,
    y1_: float,
    w1_: float,
    h1_: float,
    x2_: float,
    y2_: float,
    w2_: float,
    h2_: float,
) -> bool:
    if (
        (x1_ + w1_ >= x2_)  # r1 right edge past r2 left
        and (x1_ <= x2_ + w2_)  # r1 left edge past r2 right
        and (y1_ + h1_ >= y2_)  # r1 top edge past r2 bottom
        and (y1_ <= y2_ + h2_)  # r1 bottom edge past r2 top
    ):
        return True
    return False


class ConvenientToDraw:
    def __iter__(self) -> object:
        """overload so you can unpack object into drawRect"""
        data: dict[str, object] = vars(self)
        keys = iter(data.keys())
        for _ in range(5):
            key = next(keys)
            yield data[key]
        return


class Unpackable:
    def __iter__(self) -> object:
        """can be inherited by a dataclass to make it support the unpack operator"""
        data: dict[str, object] = vars(self)
        for key in data.keys():
            yield data[key]
        return


@dataclass
class Rect(ConvenientToDraw):
    x: float
    y: float
    height: float
    width: float
    color: str

    def point_in(self, x_: float, y_: float) -> bool:
        if (x_ >= self.x and x_ <= self.x + self.width) and (
            y_ >= self.y and y_ <= self.y + self.height
        ):
            return True
        return False

    def colliding(self, x_: float, y_: float, w_: float, h_: float) -> bool:
        return _rect_collision(self.x, self.y, self.width, self.height, x_, y_, w_, h_)
