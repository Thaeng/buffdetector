import time
from osrs.helper import helper
import pyautogui
from datetime import datetime
import threading

target_location = [1529, 972]

RETRY_IN_SECONDS = 30

ok_image_location = 'holocure/fishing/img/ok.png'

img_locations = [
    'holocure/fishing/img/down.png',
    'holocure/fishing/img/left.png',
    'holocure/fishing/img/right.png',
    'holocure/fishing/img/space.png',
    'holocure/fishing/img/up.png'
]

actions = [
    's',
    'a',
    'd',
    'space',
    'w'
]


def run():
    helper.wait_for_active_window('HoloCure')

    press_k('space')
    time.sleep(0.5)
    press_k('space')

    helper.log('Start Thread t_handle_ok')
    threading.Thread(target=handle_ok, daemon=True).start()

    helper.log('Start loop_fishing')
    loop_fishing()



def loop_fishing():
    while True:
        helper.wait_for_active_window('HoloCure')
        fish()


def fish():
    found = check_multi()
    if found == -1:
        return
    helper.log(f'Pressing [{actions[found]}]')
    press_k(actions[found])


def press_k(key):
    pyautogui.keyDown(key)
    #time.sleep(0.05)
    pyautogui.keyUp(key)


def check_multi() -> int:
    screenshot = helper.take_screenshot(xPos=target_location[0] - 10, yPos=target_location[1] - 10, width=100,
                                        height=100, test=False)
    # Threading saves about 0.02 seconds per check (about a 20-25% faster execution time)
    threads = list()
    for i in range(0, len(img_locations)):
        t = helper.ThreadWithReturnValue(target=check_image_loc, args=(i, screenshot,))
        threads.append(t)
        t.start()

    for t in threads:
        result = t.join(0.3)
        if result != -1:
            return result

    return -1


def check_image_loc(i, screenshot) -> int:
    imgLoc = helper.get_image_location_for(img_locations[i], screenshot=screenshot, confidence=0.65)
    if imgLoc is not None:
        # screenshot.save(f'test_{datetime.now().strftime("%H_%M_%S_%f")[:-3]}.png')
        helper.log(f'Found [{actions[i]}]')
        return i
    return -1


def handle_ok():
    start = datetime.now()
    while True:
        helper.wait_for_active_window('HoloCure')
        screenshot = helper.take_screenshot(xPos=1102, yPos=985, width=350,
                                            height=150, test=False)
        imgLoc = helper.get_image_location_for(ok_image_location, screenshot=screenshot, confidence=0.95)
        if imgLoc is not None:
            helper.log("Done with Fishing")
            press_k('space')
            time.sleep(0.5)
            press_k('space')
            start = datetime.now()
        time.sleep(2)

        # If Ok wasnt found for 30 seconds straight, try to recover
        if time_up(start):
            helper.log('Recover from not finding OK')
            press_k('space')
            time.sleep(0.5)
            press_k('space')
            start = datetime.now()


def time_up(start_time) -> bool:
    now = datetime.now()
    tdif = now - start_time
    if tdif.seconds > RETRY_IN_SECONDS:
        return True
    return False
