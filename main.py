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


def correct_raw_text(raw_text: str) -> str:
    # match between "is ... in"
    # (.*?) captures any characters, non-greedily
    match = re.search(r'is\s+(.*?)\s+in', raw_text, re.IGNORECASE)
    if not match:
        print(f"Format unrecoginised in raw text correction: '{raw_text.strip()}'")
        return None
    target_str = match.group(1).strip()

    corrections = {
        'l': '1',
        'I': '1',
    }
    corrected_str = ""
    for c in target_str:
        corrected_str += corrections.get(c, c)  # fall back to original char

    final_digits = re.sub(r'\D', '', corrected_str)
    if final_digits:
        return int(final_digits)
    else:
        print(f"Failed to extract number from corrected string: '{corrected_str}'")
        return None


def get_number_from_screen() -> int:
    with mss.mss() as sct:
        img = np.array(sct.grab(NUMBER_REGION))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

        # '--psm' 7 for single line OCR
        raw_text = pytesseract.image_to_string(thresh, config='--psm 7')
        
        target = correct_raw_text(raw_text)
        if target:
            print(f"Extracted: {target} from text: '{raw_text.strip()}'")
            return target
        else:
            print((f"Failed to find a number in '{raw_text.strip()}'"))
            return None


def main():
    target = get_number_from_screen()
    if not target: return

    binary_str = format(target, '08b')
    print(binary_str)


if __name__ == "__main__":
    main()