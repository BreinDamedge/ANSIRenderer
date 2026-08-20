### non-blocking input with pynput

from pynput import keyboard
import time
from collections import defaultdict
from dataclasses import dataclass, field
from math import isnan

NAN: float = float("nan")


@dataclass
class KeyState:
    state: bool = False
    prev_state: bool = False
    triggered: bool = False
    hold_start_time: float = NAN
    locked: bool = False


@dataclass
class Keyboard:
    _key_info: defaultdict[str, KeyState] = field(
        default_factory=lambda: defaultdict(KeyState)
    )

    def on_press(self, key_) -> None:
        """handle keydown state, handle trigger and engage lock"""
        try:
            key_ = key_.char
            # alpha keys
            self._key_info[key_].state = True
            if not self._key_info[key_].locked:
                self._key_info[key_].locked = True
                self._key_info[key_].triggered = True
                self._key_info[
                    key_
                ].prev_state = True  # triggering automatically sets prev_state to true

            # print("alphanumeric key {0} pressed".format(key.char))
        except AttributeError:
            pass

    def on_release(self, key_) -> None:
        """undo keydown, release trigger-lock, and end hold"""
        try:
            key_ = key_.char
            self._key_info[key_].state = False
            self._key_info[key_].hold_start_time = NAN
            self._key_info[key_].locked = False
        except AttributeError:
            pass
        # print("{0} released".format(key))
        # to stop this listener return FALSE

    def cleanup(self) -> None:
        """
        held and triggered logic
        """
        for key in self._key_info:
            cur_key = self._key_info[key]
            if cur_key.prev_state and cur_key.state and isnan(cur_key.hold_start_time):
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

    def display_key_info(self) -> None:
        for key in self._key_info:
            key_state = self._key_info[key]
            if key_state.state or key_state.triggered:
                out: str = f"{key} :"
                if key_state.state:
                    out += "down, "
                if key_state.triggered:
                    out += "triggered, "
                if not isnan(key_state.hold_start_time):
                    out += f"held ({time.time() - key_state.hold_start_time:.1f}sec),"
                print(out)

    def down(self, key_: str) -> bool:
        return self._key_info[key_].state

    def up(self, key_: str) -> bool:
        return not self._key_info[key_].state

    def triggered(self, key_: str) -> bool:
        return self._key_info[key_].triggered

    def hold_time(self, key_: str) -> float:
        """returns time held. 0 if not held"""
        if not isnan(self._key_info[key_].hold_start_time):
            return time.time() - self._key_info[key_].hold_start_time
        return 0.0

    def held(self, key_: str) -> bool:
        return bool(self.hold_time(key_))
