import random
import pyautogui
from pyautogui import Point
from win32gui import GetWindowText, GetForegroundWindow
import time
from datetime import datetime

TWEEN = pyautogui.easeOutCubic

MINIMUM_DELAY = 0
ALTERNATIVES = 1
RECOVERIES = 2

SHUTDOWN_TIME_IN_SECONDS = 35 * 60

current_obstacle: int = 2
obstacle_conf = []
mark_count = 4

consecutive_fails = 0
last_screenshot = None

# TODO Very inaccurate as of rn - Want to invest more time into this in the future
start_of_round: datetime = datetime.now()
round_times = []


def run():
    init()
    #setup_zoom()
    start = datetime.now()
    while not time_up(start):

        if current_obstacle == 1:
            global start_of_round
            start_of_round = datetime.now()

        active_window: str = GetWindowText(GetForegroundWindow())

        if active_window.startswith('RuneLite'):
            if consecutive_fails >= 10:
                log('Failing - Terminating')
                last_screenshot.save(f'last_{datetime.now().strftime("%H_%M_%S")}.png')
                break

            search_mark()
            interact_obstacle(f'osrs/canifis_rooftop/img/obs_{current_obstacle}')

            random_break()
        else:
            log('Waiting for Active Window...')
        obfuscated_sleep(0.8)
    log(f'Round Times:\n ' + '\n'.join(round_times))


def time_up(start_time) -> bool:
    now = datetime.now()
    tdif = now - start_time
    if tdif.seconds > SHUTDOWN_TIME_IN_SECONDS:
        log('SHUTDOWN DUE TO TIMER')
        return True
    return False


def random_break():
    if random.uniform(0, 1) >= 0.99:
        break_time = random.uniform(10, 40)
        log(f'Breaktime of {break_time}s')
        time.sleep(break_time)


def init():
    # Delay, Alternatives, Recovery enabled
    obstacle_conf.append([5.1, 1, 0])
    obstacle_conf.append([3.6, 1, 0])
    obstacle_conf.append([3.6, 1, 0])
    obstacle_conf.append([3.9, 4, 0])
    obstacle_conf.append([4.0, 3, 1])
    obstacle_conf.append([5.2, 0, 0])
    obstacle_conf.append([5.2, 0, 0])
    obstacle_conf.append([4.0, 0, 1])


def setup_zoom():
    while True:
        active_window: str = GetWindowText(GetForegroundWindow())
        if active_window.startswith('RuneLite'):
            log('Scrolling ...')
            for i in range(1, 15):
                pyautogui.scroll(-300)
            for i in range(1, 15):
                pyautogui.scroll(40)
            log('Scrolling done.')
            break


def interact_obstacle(image_path):
    global current_obstacle
    global consecutive_fails

    log(f'Current Obstacle: {current_obstacle}')
    log(f'Trying to Interact with {image_path}')

    # Take screenshot of Health right before Obstacle 5
    # This way it can be known that it fell down
    health_before_five = None
    if 4 == current_obstacle:
        health_before_five = take_screenshot(1761, 598, 75, 691, save=False)

    screenshot = take_screenshot()
    imgLoc = get_image_location_for(f'{image_path}.png', screenshot=screenshot)
    if imgLoc is not None:
        moveToObstacle(imgLoc)
        return
    else:
        # Trying Alternatives if Main Fails
        max_alts = obstacle_conf[current_obstacle - 1][ALTERNATIVES]
        if max_alts > 0:
            for i in range(0, max_alts):
                altImagePath = f'{image_path}_alt_{i + 1}.png'
                log(f'Trying Alternative {altImagePath}')
                imgLocAlt = get_image_location_for(altImagePath, screenshot=screenshot)
                if imgLocAlt is not None:
                    moveToObstacle(imgLocAlt)
                    return

        # Recovery Handling in case of Falling down
        # Only after a certain amount of failed attempts
        if consecutive_fails >= 2:
            max_recovery = obstacle_conf[current_obstacle - 1][RECOVERIES]
            if max_recovery > 0:
                log('Trying Recover')
                if 8 == current_obstacle:
                    log('Trying Recover for 8')
                    recover_from_eight(max_recovery, image_path, screenshot)
                    return
                if 5 == current_obstacle:
                    log('Trying Recover for 5')
                    obfuscated_sleep(0.1)
                    log('Comparing Health')
                    health_after_four = take_screenshot(1761, 598, 75, 691, save=False)
                    imgLoc = get_image_location_for(health_after_four, screenshot=health_before_five, confidence=0.95)
                    if imgLoc is not None:
                        recover_from_5()
                    return

    log('Could not interact')
    consecutive_fails += 1


def recover_from_5():
    global current_obstacle
    mouse_move_to_obfuscated(1718, 938, offsetx=0, offsety=0, offsetrngx=6, offsetrngy=6)
    pyautogui.rightClick()
    obfuscated_sleep(0.05, max_offset=0.1)
    mouse_move_to_obfuscated(1712, 1010, offsetx=0, offsety=0, offsetrngx=6, offsetrngy=6)
    pyautogui.leftClick()
    obfuscated_sleep(5)
    mouse_move_to_obfuscated(1720, 567, offsetx=0, offsety=0, offsetrngx=2, offsetrngy=2)
    pyautogui.leftClick()
    obfuscated_sleep(7)
    current_obstacle = 2


# Jump from 7 -> 8 fails
# Strategy:
#       In this case it should be enough to let the Imagerecognition for Obstacle 8 fail
#       and see if we can find the recovery Image
#       (Image of Obstacle 1 from the Position of Falling down after Position 7)
#       After detecting it we need to set the current_obstacle to 2 because it just climbed the first
def recover_from_eight(max_recovery, image_path, screenshot):
    global current_obstacle
    for i in range(0, max_recovery):
        recoveryImagePath = f'{image_path}_recovery_{i + 1}.png'
        log(f'Trying Recovery {recoveryImagePath}')
        imgLocAlt = get_image_location_for(recoveryImagePath, screenshot=screenshot)
        if imgLocAlt is not None:
            moveToObstacle(imgLocAlt)
            current_obstacle = 2
            obfuscated_sleep(5)


def moveToObstacle(imgLoc):
    global current_obstacle
    global consecutive_fails
    p: Point = pyautogui.center(imgLoc)
    mouse_move_to_obfuscated(p.x, p.y)
    pyautogui.leftClick()
    obfuscated_sleep(obstacle_conf[current_obstacle - 1][MINIMUM_DELAY])
    current_obstacle += 1
    consecutive_fails = 0

    if current_obstacle >= 9:
        log_round_time()
        current_obstacle = 1


def log_round_time():
    global start_of_round
    now = datetime.now()
    tdif = now - start_of_round
    round_times.append(str(tdif.seconds))
    log(f'Round time: {tdif.seconds} Seconds')


def mouse_move_to_obfuscated(x, y, offsetx=25, offsety=20, rng=True, offsetrngx=20, offsetrngy=20):
    duration = random.uniform(0.25, 0.40)
    random_x_offset = 0
    random_y_offset = 0
    if rng:
        medianx: int = int(offsetrngx / 2)
        mediany: int = int(offsetrngy / 2)
        random_x_offset = random.randrange(medianx * -1, medianx)
        random_y_offset = random.randrange(mediany * -1, mediany)
    xFinal = x + offsetx + random_x_offset
    yFinal = y + offsety + random_y_offset
    pyautogui.moveTo(xFinal, yFinal, duration=duration, tween=TWEEN)


def search_mark(image_path='osrs/canifis_rooftop/img/mark_'):
    screenshot = take_screenshot()
    for i in range(0, mark_count):
        mark_path = f'{image_path}{i + 1}.png'
        log(f'Trying {mark_path}')
        imgLoc = get_image_location_for(mark_path, screenshot=screenshot, confidence=0.75)
        if imgLoc is None:
            continue
        p: Point = pyautogui.center(imgLoc)
        pyautogui.moveTo(p.x + 25, p.y + 30, duration=0.3, tween=pyautogui.linear)
        pyautogui.leftClick()
        log('Mark Found')

        # Move Cursor out of the Way , can interfere with image recognition
        x = random.randrange(100, 1200)
        y = random.randrange(940, 1100)
        pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.linear)
        obfuscated_sleep(2)
        log(f'Found Image Location: {imgLoc}')
        return
    log('No Mark Found')


def get_image_location_for(image_location, screenshot=None, confidence=0.65):
    if screenshot is None:
        screenshot = take_screenshot()
    image_location = pyautogui.locate(image_location, screenshot, confidence=confidence)
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
