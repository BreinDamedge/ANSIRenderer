# ArtSI | Drawing In The Terminal With ANSI Escape Codes
A python module for drawing in the terminal using ansi escape codes

ArtSI is purely an interface for drawing in the terminal. The keyboard input wrapper is a seprate thing so it should not be included as a package dependancy when this is published.


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

# Todo:
- [ ] make artsi documentation
- [ ] release artsi as a python package on pypi
  - [ ] finalize api
  - [ ] format files as package
    - [ ] ...
- [ ] ...



# Getters for constants?
For consistancy I made getters for the colors/special constants but might wanna switch those to attribute lookups bc there's absolutely no reason to create an entire stack frame.
