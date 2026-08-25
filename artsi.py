from typing import final


def prit(v_: object) -> None:
    print(v_, end="")


@final
class Colors:
    """This class contains definitions for the color codes the Canvas will support"""

    _COLOR_NAMES: list[str] = [
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
    _FOREGROUND_CODES: dict[str, str] = {
        v: f"\033[{30 + i}m" for i, v in enumerate(_COLOR_NAMES)
    }
    _FOREGROUND_CODES["default"] = "\033[0m"
    _BACKGROUND_CODES: dict[str, str] = {
        v: f"\033[{40 + i}m" for i, v in enumerate(_COLOR_NAMES)
    }
    _BACKGROUND_CODES["default"] = _FOREGROUND_CODES["default"]

    @staticmethod
    def get_code(color_: str, bg_: bool = True) -> str:
        if bg_:
            return Colors._BACKGROUND_CODES[color_]
        else:
            return Colors._FOREGROUND_CODES[color_]


@final
class Special:
    """Contains Special characters for moving the cursor and clearing the screen"""

    _CLEAR_SCREEN = "\x1bc"
    _RESET = "\033[0m"
    _HOME: str = "\033[H"  # might end in f

    @staticmethod
    def reset() -> str:
        return Special._RESET

    @staticmethod
    def home() -> str:
        return Special._HOME

    @staticmethod
    def clear() -> str:
        return Special._CLEAR_SCREEN


class Canvas:
    background_color: str = Colors.get_code(
        "white"
    )  # default background for the Canvas
    width: int = 40
    height: int = int(
        (3 / 8) * width
    )  # makes 4:3 aspect ratio (accounts for the cursor being roughly half as wide as it is tall)
    # sparse frame buffer
    frame_chars: dict[tuple[int, int], str] = {}
    frame_codes: dict[tuple[int, int], str] = {}
    # TODO: frame codes may technically have multiple entries (ex. one for bg color and another for fg. may need to change this data structure to store a tuple of bg and fg colors, or can just have another dict for fg colors. leave undone for now w/this comment)

    @staticmethod
    def clear() -> None:
        prit(Special.clear())
        prit(Special.home())

    @staticmethod
    def reset() -> None:
        """reset frame buffer"""
        Canvas.frame_chars = {}
        Canvas.frame_codes = {}

    @staticmethod
    def set_background_color(color_: str) -> None:
        Canvas.background_color = Colors.get_code(color_)

    @staticmethod
    def get_shape() -> tuple[int, int]:
        return (Canvas.width, Canvas.height)

    @staticmethod
    def get_width() -> int:
        return Canvas.width

    @staticmethod
    def get_height() -> int:
        return Canvas.height

    @staticmethod
    def set_width(new_width_: int) -> None:
        """set the width of the canvas"""
        Canvas.width = new_width_

    @staticmethod
    def set_height(new_height_: int) -> None:
        """set the height of the canvas"""
        Canvas.height = new_height_

    @staticmethod
    def draw_rectangle(
        x_: float, y_: float, width_: int, height_: int, color_: str
    ) -> None:
        """mark frame buffer with codes"""
        color_char: str = Colors.get_code(color_)
        for h in range(height_):
            for w in range(width_):
                cy = int(y_ + h)  # candidate y
                cx = int(x_ + w)  # candidate x
                if (cy >= 0 and cy < Canvas.height) and (cx >= 0 and cx < Canvas.width):
                    # only draw to canvas if the square is on the canvas
                    Canvas.frame_codes[(cx, cy)] = color_char

    @staticmethod
    def show() -> None:
        """construct the frame string from the row column data and then print it"""
        # NOTE: for large Canvas sizes threading this (map reduce on rows?) may speed up construction
        frame_string: str = ""
        for y in range(Canvas.height):
            for x in range(Canvas.width):
                # color code
                try:
                    code = Canvas.frame_codes[(x, y)]
                except KeyError:
                    code = Canvas.background_color
                frame_string += code
                # character
                try:
                    char = Canvas.frame_chars[(x, y)]
                except KeyError:
                    char = " "  # default character is blank
                frame_string += char
            # reset the color and start the next line
            frame_string += Colors.get_code("default")
            frame_string += "\n"

        frame_string += Colors.get_code("default")
        prit(frame_string)

        # reset data & home cursor
        Canvas.reset()
        # NOTE: consider adding a parameter that will stop the frame buffer from being deleted/cleared.
        prit(Special.home())


if __name__ == "__main__":
    import time

    Canvas.clear()
    Canvas.draw_rectangle(0, 0, 3, 4, "red")
    Canvas.show()
    time.sleep(10)
    print("all good")
