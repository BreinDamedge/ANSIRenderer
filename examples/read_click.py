# gemini pynput example for mouse click
from pynput import mouse


def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at position: ({x}, {y}) with button: {button}")
        # To stop the background listener loop, return False here
        if button == mouse.Button.right:
            print("Right click detected. Stopping listener.")
            return False


# Start listening to global mouse events in the background
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
