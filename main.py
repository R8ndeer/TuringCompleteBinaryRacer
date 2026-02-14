import cv2
import numpy as np
import mss
import pytesseract
import pyautogui
import time

from matplotlib import pyplot as plt

# ==============================================================================
# CONFIGS (2440x1560)
# ==============================================================================
NUMBER_REGION = {
    'top': 734,
    'left': 1023,
    'width': 507,
    'height': 92
}
Y_BUTTON = 1413
x_button = (724, 869, 1012, 1159, 1300, 1446, 1589, 1731)
BUTTON_COORDS = [(x, Y_BUTTON) for x in x_button]


def get_number_from_screen():
    with mss.mss() as sct:
        img = np.array(sct.grab(NUMBER_REGION))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        
        plt.imshow(thresh)
        plt.title("Is this the right region?")
        plt.show()


def main():
    get_number_from_screen()


if __name__ == "__main__":
    main()