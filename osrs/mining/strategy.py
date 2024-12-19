import time

from osrs.helper import helper
import pyautogui
import numpy

base_img_path = 'osrs/mining/img/'

inventory_slot_locations = [
    [1910, 750],
    [2050, 750],
    [2190, 750]
]

rock_locations = [
    [877, 838, base_img_path + 'rock_down'],
    [513, 583, base_img_path + 'rock_left'],
    [862, 331, base_img_path + 'rock_up']
]
next_rock_locations = rock_locations[1:] + rock_locations[:1]


def run():
    while True:
        helper.wait_for_active_window('RuneLite')
        mine()
        helper.wait_for_active_window('RuneLite')
        drop_items()


def drop_items():
    pyautogui.keyDown('shift')
    for inventory_slot in inventory_slot_locations:
        x = inventory_slot[0]
        y = inventory_slot[1]
        helper.mouse_move_to_obfuscated(x, y)
        pyautogui.leftClick()
    pyautogui.keyUp('shift')
    helper.obfuscated_sleep(0.05, max_offset=0.05)
    return


def mine():
    for i in range(0, len(rock_locations)):
        rock = rock_locations[i]
        helper.log(f'Mining Rock [{rock}]')
        helper.wait_for_active_window('RuneLite')

        move_to_rock(rock)
        pyautogui.leftClick()

        helper.log(f'Waiting for Mining Rock [{rock}]')

        if i == (len(rock_locations)-1):
            helper.mouse_move_to_obfuscated(inventory_slot_locations[0][0], inventory_slot_locations[0][1])
        else:
            move_to_rock(next_rock_locations[i], offsety=-40)

        wait_for_mining(rock)

        helper.log(f'Done Mining Rock [{rock}]')
    return


def move_to_rock(rock: [], offsety: int = 0):
    x = rock[0]
    y = rock[1]
    helper.mouse_move_to_obfuscated(x, y, offsety=offsety, offsetrngx=30, offsetrngy=30)


def wait_for_mining(rock: []):
    for i in range(0, 10):
        screenshot = helper.take_screenshot(xPos=rock[0] - 250, yPos=rock[1] - 200, width=600, height=400)
        imgLoc = helper.get_image_location_for(f'{rock[2]}.png', screenshot=screenshot, confidence=0.95)
        if imgLoc is not None:
            break
        time.sleep(0.5)
