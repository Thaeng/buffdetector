import pyautogui
from datetime import datetime
import time
from win32gui import GetWindowText, GetForegroundWindow


def take_screenshot(xPos, yPos, width, height, test=False):
    screenshot = pyautogui.screenshot(region=(xPos, yPos, width, height))

    if test:
        screenshot.save(f'test_{datetime.now().strftime("%H_%M_%S_%f")[:-3]}.png')

    return screenshot


def wait_for_active_window(window: str):
    active_window: str = GetWindowText(GetForegroundWindow())
    while not active_window.startswith(window):
        active_window = GetWindowText(GetForegroundWindow())
        log(f'[{window}] Waiting for active Window ...  Currently Active Window: {active_window}')
        time.sleep(1)
    return


def left_click_img_location_center(img_location):
    if img_location is None:
        raise Exception(f'Image Location was None: [{img_location}]')
    pyautogui.moveTo(pyautogui.center(img_location))
    pyautogui.leftClick()

def right_click_img_location_center(img_location):
    if img_location is None:
        raise Exception(f'Image Location was None: [{img_location}]')
    pyautogui.moveTo(pyautogui.center(img_location))
    pyautogui.rightClick()


def get_image_location_for(image_location, screenshot=None, confidence=0.65, grayscale=False):
    try:
        if screenshot is None:
            screenshot = pyautogui.screenshot()
        image_location = pyautogui.locate(image_location, screenshot, confidence=confidence, grayscale=grayscale)
        return image_location
    except pyautogui.ImageNotFoundException:
        return None


def log(message: str):
    now = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f' [{now}]  {message}')
