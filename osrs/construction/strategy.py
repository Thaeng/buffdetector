import time
import pyautogui

from osrs.helper import helper

build_remove_location = [1200, 1340]
butler_side_pos = [1900, 800]
demon_butler_img = 'osrs/construction/img/demonbutler.png'


def run():
    helper.wait_for_active_window('RuneLite')
    rotation_one()
    rotation_two()


def rotation_one():
    helper.obfuscated_sleep(0.650, max_offset=0.2)
    move_mouse_to_build_location()
    if is_butler_in_front():
        helper.log('Butler is infront')
        helper.leftClick()
        helper.obfuscated_sleep(0.4, max_offset=0.1)
        pyautogui.press('1')
        helper.obfuscated_sleep(0.650, max_offset=0.2)
    else:
        helper.log('Butler is not infront')
        move_mouse_to_butler_side_location()
        helper.leftClick()
        helper.obfuscated_sleep(0.4, max_offset=0.1)
        pyautogui.press('1')
        move_mouse_to_build_location()
        helper.obfuscated_sleep(0.650, max_offset=0.2)

    build()
    helper.obfuscated_sleep(1.2, max_offset=0.1)
    remove()
    helper.obfuscated_sleep(0.5, max_offset=0.1)
    build()
    helper.obfuscated_sleep(1.2, max_offset=0.1)
    remove()


def rotation_two():
    helper.obfuscated_sleep(1.2, max_offset=0.1)
    build()
    helper.obfuscated_sleep(1.2, max_offset=0.1)
    remove()
    helper.obfuscated_sleep(0.650, max_offset=0.2)

    if is_butler_in_front():
        helper.log('Butler is infront')
        helper.leftClick()
        helper.obfuscated_sleep(0.4, max_offset=0.1)
        helper.leftClick()
        helper.obfuscated_sleep(0.4, max_offset=0.1)
        pyautogui.press('1')
        helper.obfuscated_sleep(0.650, max_offset=0.2)
    else:
        helper.log('Butler is not infront')
        move_mouse_to_butler_side_location()
        helper.leftClick()
        helper.obfuscated_sleep(0.4, max_offset=0.1)
        helper.leftClick()
        helper.obfuscated_sleep(0.4, max_offset=0.1)
        pyautogui.press('1')
        move_mouse_to_build_location()
        helper.obfuscated_sleep(0.650, max_offset=0.2)

    build()
    helper.obfuscated_sleep(1.2, max_offset=0.1)
    remove()
    helper.obfuscated_sleep(0.5, max_offset=0.1)
    build()
    helper.obfuscated_sleep(1.2, max_offset=0.1)
    remove()


def move_mouse_to_build_location():
    helper.log('Moving Mouse to Build Location.')
    x = build_remove_location[0]
    y = build_remove_location[1]
    helper.mouse_move_to_obfuscated(x, y, rng=True, offsetrngx=85, offsety=2)


def move_mouse_to_butler_side_location():
    helper.log('Moving Mouse to Butler Side Location.')
    x = butler_side_pos[0]
    y = butler_side_pos[1]
    helper.mouse_move_to_obfuscated(x, y, rng=True, offsetrngx=26, offsety=202)


def is_butler_in_front() -> bool:
    for i in range(0, 5):
        screenshot = helper.take_screenshot(0, 0, width=2000, height=1400)
        imgLoc = helper.get_image_location_for(demon_butler_img, screenshot=screenshot, confidence=0.8)
        if imgLoc is not None:
            return True
        time.sleep(0.5)
    return False


def build():
    remove()


def remove():
    helper.rightClick()
    helper.obfuscated_sleep(0.1, max_offset=0.05)
    helper.leftClick()
    helper.obfuscated_sleep(0.6, max_offset=0.05)
    pyautogui.press('1')

