### non-blocking input with pynput

from pynput import keyboard
from pynput.keyboard import Key, KeyCode
import time
from collections import defaultdict
from dataclasses import dataclass, field
from math import isnan


NAN: float = float("nan")
_key_info: defaultdict[str, KeyState] = field(
    default_factory=lambda: defaultdict(KeyState)
)


@dataclass
class KeyState:
    state: bool = False
    prev_state: bool = False
    triggered: bool = False
    hold_start_time: float = NAN
    locked: bool = False


def _get_key_name(key_: Key | KeyCode) -> str:
    global _key_info
    """
    Determines a consistent string name for the given pynput key object.
    Returns 'unknown' if nothing recognizable is found.
    """
    try:
        # alphanumeric characters
        return str(key_.char)
    except AttributeError:
        # special characters
        if hasattr(key_, "name"):
            return key_.name

        # if key doesn't have a name return an empty string
        return ""
        # return str(key_)  # alternative approach


def on_press(key_: Key | KeyCode) -> None:
    global _key_info
    """handle keydown state, handle trigger and engage lock"""
    key_name = _get_key_name(key_)

    # don't handle quirky keys
    if key_name == "":
        return

    # for debugging
    # print(f"key {key_name} pressed")

    # actual logic updating keys state
    try:
        _key_info[key_name].state = True
        if not _key_info[key_name].locked:
            _key_info[key_name].locked = True
            _key_info[key_name].triggered = True
            _key_info[key_name].prev_state = True

    except Exception as _:
        # ignore errors
        pass
        # print(f"Error during on_press for {key_name}: {e}")


def on_release(key_: Key | KeyCode) -> None:
    global _key_info
    """undo keydown, release trigger-lock, and end hold"""
    key_name = _get_key_name(key_)

    # actual logic again
    try:
        _key_info[key_name].state = False
        _key_info[key_name].hold_start_time = NAN
        _key_info[key_name].locked = False

    except Exception as _:
        pass
        # print(f"Error during on_release for {key_name}: {e}")


def cleanup() -> None:
    global _key_info
    """
    held and triggered logic
    """
    for key in _key_info:
        cur_key = _key_info[key]
        if cur_key.prev_state and cur_key.state and isnan(cur_key.hold_start_time):
            cur_key.hold_start_time = time.time()
        cur_key.prev_state = cur_key.state
        # reset triggered
        cur_key.triggered = False


def begin() -> None:
    global _key_info

    def press2(key_: Key | KeyCode):
        return on_press(key_)

    def release2(key_: Key | KeyCode):
        return on_release(key_)

    listener = keyboard.Listener(
        on_press=press2, on_release=release2
    )  # to stop this listener return FALSE from one of the functions
    listener.start()


def display_key_info() -> None:
    global _key_info
    for key in _key_info:
        key_state = _key_info[key]
        if key_state.state or key_state.triggered:
            out: str = f"{key} :"
            if key_state.state:
                out += "down, "
            if key_state.triggered:
                out += "triggered, "
            if not isnan(key_state.hold_start_time):
                out += f"held ({time.time() - key_state.hold_start_time:.1f}sec),"
            print(out)


def down(key_: str) -> bool:

    global _key_info
    return _key_info[key_].state


def up(key_: str) -> bool:
    global _key_info
    return not _key_info[key_].state


def triggered(key_: str) -> bool:
    global _key_info
    return _key_info[key_].triggered


def hold_time(key_: str) -> float:
    global _key_info
    """returns time held. 0 if not held"""
    if not isnan(_key_info[key_].hold_start_time):
        return time.time() - _key_info[key_].hold_start_time
    return 0.0


def held(key_: str) -> bool:
    global _key_info
    return bool(hold_time(key_))
