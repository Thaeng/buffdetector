import time

import pyautogui
import pyperclip
from urllib3 import request

from patreon import scanentries
from patreon.class_post import Post
from utils.util import wait_for_active_window, get_image_location_for, left_click_img_location_center, \
    right_click_img_location_center, log

PATREON_BRAVE = 'Yunya | Creating Audio Content | Patreon - Brave'

img_dotdotdot = '../patreon/img/dotdotdot.png'
img_download = '../patreon/img/download.png'
img_copylinkadress = '../patreon/img/copylinkadress.png'

download_folder = 'C:/Users/thaen/Downloads/'


def scan_dotdotdot():
    return get_image_location_for(image_location=img_dotdotdot, grayscale=True, confidence=0.95)


def scan_download():
    return get_image_location_for(image_location=img_download, grayscale=True, confidence=0.95)


def scan_copylincadress():
    return get_image_location_for(image_location=img_copylinkadress, grayscale=True, confidence=0.95)


def open_new_tab():
    pyautogui.hotkey('ctrl', 't')
    time.sleep(0.5)


def open_website(post: Post):
    open_new_tab()
    pyperclip.copy(post.url)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(1)


def close_tab():
    pyautogui.hotkey('ctrl', 'w')


def locate_dotdotdot():
    loc_dotdotdot = scan_dotdotdot()
    for i in range(0, 10):
        if loc_dotdotdot is not None:
            break
        pyautogui.scroll(-200)
        time.sleep(0.5)
        loc_dotdotdot = scan_dotdotdot()
        time.sleep(0.5)

    return loc_dotdotdot


def download_file(post: Post, url: str):
    resp = request("GET", url)

    if resp.status != 200:
        raise Exception(f'Response Status was: {resp.status} for Post [{post}]')

    filename = post.title
    filelength: int = (245 - len(post.published))
    if len(filename) >= filelength:
        filename = filename[:filelength]

    filename = filename + "_" + post.published
    f = open(f"{download_folder}{filename}.mp3", "wb")
    f.write(resp.data)
    f.close()


def run(posts: []):
    counter = 0

    wait_for_active_window(PATREON_BRAVE)

    for post in posts:
        log(f"Downloading Post: [{post}]")
        open_website(post)

        # dotdotdot btn
        loc_dotdotdot = locate_dotdotdot()
        if loc_dotdotdot is None:
            print(f'Could not find dotdotdot for [{post.url}]')
            break
        left_click_img_location_center(loc_dotdotdot)
        time.sleep(0.2)

        # download btn
        loc_download = scan_download()
        right_click_img_location_center(loc_download)

        # copylinkadress btn
        loc_copylinkadress = scan_copylincadress()
        left_click_img_location_center(loc_copylinkadress)

        # download file
        direct_url = pyperclip.paste()
        download_file(post, direct_url)

        close_tab()

        counter += 1
        log(f'[{counter}/{len(posts)}] Downloaded')


if __name__ == '__main__':
    run()
    exit()
