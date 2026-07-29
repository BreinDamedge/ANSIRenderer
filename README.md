# Ansi Renderer (T-art or Tart, Terminal Art)
A python module for drawing in the terminal using ansi escape codes

Has pynput as a dependancy now.

# Ideas/Concepts
A canvas will be the main object.


# Concepts / Objects
## Canvas API
```py


def setup(self) -> None:
"""
"""


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
- [ ] change canvas from rc to xy
- [ ] support drawing at position outside of the viewport
- [ ] support drawing with float coords
- [ ] make pong
- [ ] ...
- [ ] ...
- [ ] ...
- [ ] ...
- [ ] ...


# Keyboard Input Handling
tart will support keyboard input. Because it is expected that any "game logic" is in the main game loop, I'm making an interface to get info about the state of the keys while in that loop. pynput uses key events (as it should) but polling aligns more with the draw loop (unfortunately for performance) so I've made the Keyboard class as a wrapper for pynput that can be used in a game/draw loop.
The `cleanup()` method is the part I like the least atm. It handles the key_triggered and key_held flags/logic. Currently it handles them a bit worse than I'd like it too and it also requires you to remember another call at the end of your loop. Another option could be that the triggered/held flags flip after a certain amount of time that the key has been down but depending on the framerate of the game that couuld have some weird bugs. I'll think about it more once I've made some demos as is.

