# ArtSI | Drawing In The Terminal With ANSI Escape Codes
A python module for drawing in the terminal using ansi escape codes

ArtSI is purely an interface for drawing in the terminal. The keyboard input wrapper is a seprate thing so it should not be included as a package dependancy when this is published.

# TODO:
- [ ] make artsi documentation
- [ ] release artsi as a python package on pypi
  - only the interface for drawing

```py
# ArtSI hello world
if __name__ == "__main__":
    from artsi import Canvas

    Canvas.hello_canvas()
```


```py
# Rectangle Drawing
if __name__ == "__main__":
    Canvas.clear()
    Canvas.draw_rectangle(0, 0, 3, 4)
    Canvas.show(home_=False)
```

# Ideas/Concepts
You have a Canvas that you are drawing on. You can draw colored rectangles. All of this is displayed using ANSI escape codes in the terminal.

You can make little animations with this and also when combined with keyboard input from something like pynput you can make little games too.

# Concepts
## Canvas API
```py



def drawRect(self, r_: float, c_: float, height_: int, width_: int, color_: str) -> None:
"""
"""

def show(self) -> None:
"""
"""

def shape(self) -> tuple[int, int]:
"""
"""

```


# Todo:
- [ ] make pong
  - [x] basic game
  - [ ] decide if you want proper collision
  - [ ] sub pixel positioning asyncronosly from draw loop?
  - [ ] score tracking
- [ ] make snake
  - [x] movement
    - one physics update per frame
  - [x] growing the snake
  - [ ] make fruit
  - [ ] collision checks
  - [ ] score
  - [ ] play again?
- [ ] ...
- [ ] ...
- [ ] ...
- [ ] ...


# Keyboard Input Handling
tart will support keyboard input. Because it is expected that any "game logic" is in the main game loop, I'm making an interface to get info about the state of the keys while in that loop. pynput uses key events (as it should) but polling aligns more with the draw loop (unfortunately for performance) so I've made the Keyboard class as a wrapper for pynput that can be used in a game/draw loop.
The `cleanup()` method is the part I like the least atm. It handles the key_triggered and key_held flags/logic. Currently it handles them a bit worse than I'd like it too and it also requires you to remember another call at the end of your loop. Another option could be that the triggered/held flags flip after a certain amount of time that the key has been down but depending on the framerate of the game that couuld have some weird bugs. I'll think about it more once I've made some demos as is.


```py
@classmethod
def initialize(cls) -> None:
    cls.frame_codes: list[list[str]] = [
        [Canvas.background_color] * Canvas.height for _ in range(Canvas.height)
    ]
```

# Getters for constants?
For consistancy I made getters for the colors/special constants but might wanna switch those to attribute lookups bc there's absolutely no reason to create an entire stack frame.
