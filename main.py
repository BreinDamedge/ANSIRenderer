from keys import Keyboard
import time


k = Keyboard()
k.begin()
while True:
    k.display_key_info()
    k.cleanup()
    time.sleep(1)

