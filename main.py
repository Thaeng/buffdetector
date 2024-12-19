import logging
import signal
import time
import winsound
import winsound as ws
from multiprocessing import Process
from random import uniform
from threading import Event

import pyautogui
from win32gui import GetWindowText, GetForegroundWindow

from osrs.canifis_rooftop import strategy as canifis
from osrs.mining import strategy as mining
from osrs.construction import strategy as construction
from holocure.fishing import strategy as hc_fishing

sound = ws.MB_OK
running_processes = []
event = Event()


def signal_handler(sig, frame):
    print('Exiting...')
    event.set()
    exit(1)


signal.signal(signal.SIGINT, signal_handler)


def look_for(image_location, xPos=0, yPos=0, width=2560, height=300):
    screenshot = pyautogui.screenshot('test.png', region=(xPos, yPos, width, height))
    image_location = pyautogui.locate(image_location, screenshot, confidence=0.8)
    return image_location


def watch_plague_bearer():
    process = Process(target=alert_for_plague_bearer)
    process.start()


def watch_press_button():
    process = Process(target=press_button)
    process.start()


def alert_for_plague_bearer():
    has_alerted = False
    while True:
        if event.is_set():
            break
        active_window = GetWindowText(GetForegroundWindow())
        if active_window == 'Path of Exile':
            img_loc_full = look_for('plague_bearer/plague_full.png')
            print(f'[PB] Full: {active_window} || {has_alerted} || {img_loc_full}')

            if img_loc_full is not None and not has_alerted:
                winsound.MessageBeep(type=sound)
                has_alerted = True

            else:
                img_loc_incu = look_for('plague_bearer/plague_incubating.png')
                print(f'[PB] Incubating: {active_window} || {has_alerted} || {img_loc_incu}')
                if img_loc_incu is not None:
                    has_alerted = False
        else:
            print('[PB] Waiting for active Window...')
        time.sleep(1.5)
    print('[PB] Terminated Watcher for Plague Bearer')


def alert_for_adrenaline(grace=4):
    shouldAlert = True
    couldNotFindCounter = 0
    imageLocation = None
    while True:
        activeWindow = GetWindowText(GetForegroundWindow())
        if activeWindow == 'Path of Exile':
            im1 = pyautogui.screenshot(region=(0, 0, 2560, 300))
            imageLocation = pyautogui.locate('adrenaline.png', im1, confidence=0.7)

            if imageLocation is None:
                if shouldAlert and couldNotFindCounter >= grace:
                    winsound.MessageBeep(type=sound)
                    shouldAlert = False
                couldNotFindCounter += 1
            else:
                couldNotFindCounter = 0
                shouldAlert = True
        time.sleep(0.5)
        print(f'{activeWindow} || {shouldAlert} || {couldNotFindCounter} || {imageLocation}')


def press_button():
    utility_flasks_running = False
    counter_not_running = 0
    while True:
        if event.is_set():
            break
        active_window = GetWindowText(GetForegroundWindow())

        if active_window == 'Path of Exile':

            if are_utility_flasks_running():
                utility_flasks_running = True
                counter_not_running = 0
            else:
                counter_not_running += 1
                if counter_not_running >= 3:
                    utility_flasks_running = False

            if utility_flasks_running:
                pyautogui.press('1')
        else:
            print('[Button] Waiting for active Window...')
        time.sleep(uniform(2.3, 2.9))
    print('[Button] Terminated Watcher for Plague Bearer')


def are_utility_flasks_running() -> bool:
    image_location = look_for('plague_bearer/flask_running.png', xPos=470, yPos=1420, width=240, height=20)
    print(f'[Button] Utility Flasks running: {image_location}')
    return image_location is not None


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    construction.run()
    # mining.run()
    # hc_fishing.run()
    # canifis.run()
    # watch_plague_bearer()
    # watch_press_button()
