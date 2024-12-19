import random
from threading import Thread

import pyautogui
from win32gui import GetWindowText, GetForegroundWindow
import time
from datetime import datetime


class ThreadWithReturnValue(Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=True)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


def wait_for_active_window(window:str):
    active_window: str = GetWindowText(GetForegroundWindow())
    while not active_window.startswith(window):
        active_window = GetWindowText(GetForegroundWindow())
        log(f'[{window}] Waiting for active Window ...  Currently Active Window: {active_window}')
        time.sleep(1)
    return


def mouse_move_to_obfuscated(x:int, y:int, offsetx:int=0, offsety:int=0, rng:bool=True, offsetrngx:int=20, offsetrngy:int=20):
    duration = random.uniform(0.15, 0.30)
    random_x_offset = 0
    random_y_offset = 0
    if rng:
        medianx: int = int(offsetrngx * 0.5)
        mediany: int = int(offsetrngy * 0.5)
        random_x_offset = random.randrange(medianx * -1, medianx)
        random_y_offset = random.randrange(mediany * -1, mediany)
    xFinal = x + offsetx + random_x_offset
    yFinal = y + offsety + random_y_offset
    pyautogui.moveTo(xFinal, yFinal, duration=duration, tween=pyautogui.easeOutCubic)


def get_image_location_for(image_location, screenshot=None, confidence=0.65, grayscale=False):
    if screenshot is None:
        screenshot = take_screenshot()
    image_location = pyautogui.locate(image_location, screenshot, confidence=confidence, grayscale=grayscale)
    return image_location


def take_screenshot(xPos=20, yPos=30, width=1720, height=930, save=True, test=False):
    global last_screenshot
    screenshot = pyautogui.screenshot(region=(xPos, yPos, width, height))

    if save:
        last_screenshot = screenshot

    if test:
        screenshot.save(f'test_{datetime.now().strftime("%H_%M_%S_%f")[:-3]}.png')

    return last_screenshot


def obfuscated_sleep(min_duration: float, min_offset: float = 0.0, max_offset: float = 0.4):
    sleep_offset = random.uniform(min_offset, max_offset)
    time.sleep(min_duration + sleep_offset)


def log(message: str):
    now = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f' [{now}]  {message}')


def leftClick():
    duration = random.uniform(0.05, 0.1)
    pyautogui.leftClick(duration=duration)


def rightClick():
    duration = random.uniform(0.05, 0.1)
    pyautogui.rightClick(duration=duration)