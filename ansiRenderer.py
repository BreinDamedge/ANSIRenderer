import time

COLOR_NAMES = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white", "default"]
FOREGROUND_COLORS = { v : 30+i for i, v in enumerate(COLOR_NAMES) }
FOREGROUND_COLORS["default"] = 0
BACKGROUND_COLORS = { k : v+10 for k, v in FOREGROUND_COLORS.items() }
BACKGROUND_COLORS["default"] = 0

def colorChar(color_:str, bg_=True) -> str:
    if bg_ == True: return f"\033[{BACKGROUND_COLORS[color_]}m"
    else: return f"\033[{FOREGROUND_COLORS[color_]}m"

def prit(v_):
    print(v_, end="")

def set_color(color_:str) -> None:
    prit(colorChar(color_))

CLEAR_SCREEN = "\x1bc"
RESET = "\033[0m"
DEFAULT = colorChar("default")
DEFB:str = colorChar("black")   # default background for our window
HOME:str = "\033[H" # might end in f

# --------------------------------------------------------------
if __name__ == "__main__":

    C = 60
    R = int((3/8)*C)
    """
    current idea is have a grid of single chars for actual screen content, and then a second 2d array of escape codes
    """

# make a box float across the screen @ 2 cells/sec
    st = time.time()
    lf_end = st
    box_pos = [0, 0]    # rows, cols
    box_vel = [3, 10]
    box_size = [1,1]
    box_color = "red"
    MIN_FRAME_DELAY = (1/30)
    prit(CLEAR_SCREEN)

    def clip(v_, min_, max_) -> int:
        if v_ < min_: return min_
        elif v_ > max_: return max_
        else: return v_




    while True:
        f_start = time.time()
        # blank refresh of the screen
        frame_chars:str = [" "*C]*R
        frame_codes:list[list[str]] = [[DEFB]*C for _ in range(R)]
        frame_string:str = ""

        # determine the box's position
        box_pos[0] = box_pos[0] + (f_start-lf_end)*box_vel[0]
        box_pos[1] = box_pos[1] + (f_start-lf_end)*box_vel[1]

        # get box's position as screen_coords
        bpi = [int(box_pos[0]), int(box_pos[1])]
        # if box has gone off screen, turn it around
        if (bpi[0] >= R-1 and box_vel[0] > 0) or (bpi[0] <= 0 and box_vel[0] < 0):
            box_vel[0] *= -1
            # box_pos[0] + 2 + (f_start-lf_end)*box_vel[0]
        if (bpi[1] >= C-1 and box_vel[1] > 0) or (bpi[1] <= 0 and box_vel[1] < 0):
            box_vel[1] *= -1
            # box_pos[1] + 2 + (f_start-lf_end)*box_vel[1]


        bpi[0] = clip(bpi[0], 0, R-1)
        bpi[1] = clip(bpi[1], 0, C-1)


        # set frame_codes
        frame_codes[bpi[0]][bpi[1]] = colorChar("red")



        for r in range(len(frame_chars)):
            for c in range(len(frame_chars[r])):
                frame_string += frame_codes[r][c]
                frame_string += frame_chars[r][c]
                frame_string += colorChar("default")
            frame_string += "\n"

        prit(frame_string)

        # print(f"r: {box_pos[0]}\nc: {box_pos[1]}")
        prit(HOME)
        set_color("default")

        frame_time = time.time()-f_start
        if frame_time < MIN_FRAME_DELAY:
            time.sleep(MIN_FRAME_DELAY)

        lf_end = f_start


