import logging

__motion_available = True

def set_motion_available(value: bool):
    global __motion_available
    __motion_available = value
    print(f"Motion availability set to {value}")

def motion_available():
    global __motion_available
    return __motion_available
