### non-blocking input with pynput

from pynput import keyboard
import time
from collections import defaultdict
from dataclasses import dataclass, field

NAN: float = float("nan")


@dataclass
class KeyState:
    state: bool = False
    prev_state: bool = False
    held: bool = False
    triggered: bool = False
    hold_start_time: float = NAN
    locked: bool = False


@dataclass
class Keyboard:
    key_info: defaultdict[str, KeyState] = field(
        default_factory=lambda: defaultdict(KeyState)
    )

    def on_press(self, key_) -> None:
        """handle keydown state, handle trigger and engage lock"""
        try:
            key_ = key_.char
            # alpha keys
            self.key_info[key_].state = True
            if not self.key_info[key_].locked:
                self.key_info[key_].locked = True
                self.key_info[key_].triggered = True
            # print("alphanumeric key {0} pressed".format(key.char))
        except AttributeError:
            pass

    def on_release(self, key_) -> None:
        """undo keydown, release trigger-lock, and end hold"""
        try:
            key_ = key_.char
            self.key_info[key_].state = False
            self.key_info[key_].held = False
            self.key_info[key_].hold_start_time = NAN
            self.key_info[key_].locked = False
        except AttributeError:
            pass
        # print("{0} released".format(key))
        # to stop this listener return FALSE

    def key_stuff(self) -> None:
        """
        held and triggered logic
        """
        for key in self.key_info:
            cur_key = self.key_info[key]
            if cur_key.prev_state and cur_key.state and not cur_key.held:
                cur_key.held = True
                cur_key.hold_start_time = time.time()
            cur_key.prev_state = cur_key.state
            # reset triggered
            cur_key.triggered = False

    def begin(self) -> None:
        def press2(key_):
            return self.on_press(key_)

        def release2(key_):
            return self.on_release(key_)

        listener = keyboard.Listener(
            on_press=press2, on_release=release2
        )  # to stop this listener return FALSE from one of the functions
        listener.start()

    def silly_print(self) -> None:
        for key in self.key_info:
            key_state = self.key_info[key]
            if key_state.state:
                print(f"{key} : {key_state}")


if __name__ == "__main__":
    k = Keyboard()
    k.begin()
    while True:
        k.silly_print()
        k.key_stuff()
        time.sleep(1)
