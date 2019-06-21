import pyautogui
import time
import os
import numpy as np
import clipboard
# import requests
# from bs4 import BeautifulSoup
import cv2 as cv

from geom_utils import *


def take_screenshot():
    # TODO don't save screenshot on disk, use img = pyautogui.screenshot()
    # and get rid of 4-th dimension. Just to be safe, we'll work with imread by cv2
    tmp = "screen-tmp.png"
    pyautogui.screenshot(tmp)
    img_screen = cv.imread(tmp)
    print("Screenshot size", img_screen.shape)
    return img_screen


# class PyWeb(object):
#     def _get_url(self, url):
#         resp = requests.get(url)
#         if resp:
#             return resp.text
#         return None
#
#     def get_buttons(self, url):
#         text = self._get_url(url)
#         soup = BeautifulSoup(text, 'html.parser')
#         buttons = soup.find_all('button')
#         return buttons


class PyScreen(object):
    def __init__(self):
        self.debug_i = 0
        im1 = np.array(pyautogui.screenshot())
        self.actual_size = im1.shape[:2]
        print("Actual screen size   ", self.actual_size)
        self.pag_w, self.pag_h = pyautogui.size()
        print("PyAutoGUI screen size", self.pag_w, self.pag_h)

    def _locate_image(self, img_search, img_screen, threshold=0.8):
        assert len(img_search.shape) == len(img_screen.shape), "search and base image have different dimensions"
        res = cv.matchTemplate(img_screen, img_search, cv.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        w, h = img_search.shape[1], img_search.shape[0]
        points = list()
        for pt in zip(*loc[::-1]):
            up_left_coor = pt
            down_right_coor = (pt[0] + w, pt[1] + h)
            cv.rectangle(img_screen, up_left_coor, down_right_coor, (0, 0, 255), 2)
            points.append([pt[0], pt[1], pt[0] + w, pt[1] + h])
        img_debug = f"img_{self.debug_i}.png"
        self.debug_i += 1
        cv.imwrite(img_debug, img_screen)
        return points

    def _locate_on_screen(self, img_fname, similarity=0.8, screenshot=None):
        img_search = cv.imread(img_fname)
        print("Search image size", img_search.shape)
        if screenshot is None:
            img_screen = take_screenshot()
        else:
            img_screen = screenshot
        recs = self._locate_image(img_search, img_screen)
        # merge similar rectangles
        if recs:
            recs = merge_rectangles(recs, similarity=similarity)
        return recs, img_screen

    def locate_on_screen(self, img, left_of=None):
        recs, img_screen = self._locate_on_screen(img)
        if left_of is not None:
            recs_left, _ = self._locate_on_screen(left_of, screenshot=img_screen)
            if recs_left:
                rec_left = recs_left[0]
                recs = [x for x in recs if rectangle_left_of(x, rec_left)]
        return recs

    def wait_for_image(self, img_wait, timeout):
        start = time.time()
        while time.time() - start < timeout:
            recs = self.locate_on_screen(img_wait)
            if len(recs) > 0:
                return recs[0]
        return None

    def _get_xy_from_rectangle(self, rec):
        x = int((rec[0] + rec[2]) / 2)
        y = int((rec[1] + rec[3]) / 2)
        x = int(x / self.actual_size[1] * self.pag_w)
        y = int(y / self.actual_size[0] * self.pag_h)
        return x, y

    def _click_and_wait(self, x, y, img_wait=None, timeout=1):
        pyautogui.click(x, y)
        if img_wait:
            return self.wait_for_image(img_wait, timeout)
        return None

    def click(self, rec, img_wait=None):
        x, y = self._get_xy_from_rectangle(rec)
        pyautogui.moveTo(x, y, duration=0.5)
        return self._click_and_wait(x, y, img_wait=img_wait)


if __name__ == "__main__":
    pysc = PyScreen()
    img_ago = os.path.join("images", "ago-txt.png")
    img_apply = os.path.join("images", "apply-btn.png")
    matches = pysc.locate_on_screen(img_ago, left_of=img_apply)
    print("found matches", len(matches))
    for match in matches[:1]:
        rec_wait = pysc.click(match, img_wait=img_apply)
        if rec_wait:
            pysc.click(rec_wait)
            time.sleep(2)
            pyautogui.hotkey('command', 'l')
            pyautogui.hotkey('command', 'c')
            url = clipboard.paste()
            print(url)
            # web = PyWeb()
            # buttons = web.get_buttons(url)
            pass

