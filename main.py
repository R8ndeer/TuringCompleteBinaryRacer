import re
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
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
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

        # '--psm' 7 for single line OCR
        raw_text = pytesseract.image_to_string(thresh, config='--psm 7')
        
        match = re.search(r'\d+', raw_text)
        if match:
            target = int(match.group())
            print(f"Extracted: {target} from text: '{raw_text.strip()}'")
        else:
            print((f"Failed to find a number in '{raw_text.strip()}'"))


def main():
    get_number_from_screen()


if __name__ == "__main__":
    main()