import tkinter

import pyautogui
import time
import logging

import winsound
import winsound as ws
from win32gui import GetWindowText, GetForegroundWindow




def alertForAdrenaline(grace=4):

    shouldAlert = True
    countNotFound = 0
    adrenalineLocation = None
    while True:
        activeWindow = GetWindowText(GetForegroundWindow())
        if activeWindow == 'Path of Exile':
            im1 = pyautogui.screenshot(region=(0, 0, 2560, 300))
            adrenalineLocation = pyautogui.locate('adrenaline.png', im1, confidence=0.7)

            if adrenalineLocation is None:
                if shouldAlert and countNotFound >= grace:
                    winsound.MessageBeep(type=ws.MB_OK)
                    shouldAlert = False
                countNotFound += 1
            else:
                countNotFound = 0
                shouldAlert = True
        time.sleep(0.5)
        logging.error(f'{activeWindow} || {shouldAlert} || {countNotFound} || {adrenalineLocation}')


if __name__ == '__main__':
    alertForAdrenaline()
