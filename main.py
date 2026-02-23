import re
import keyboard
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
X_BUTTONS = (724, 869, 1012, 1159, 1300, 1446, 1589, 1731)
BUTTON_COORDS = [(x, Y_BUTTON) for x in X_BUTTONS]
SUBMIT_BUTTON = (1278, 1521)


def correct_raw_text(raw_text: str) -> str:
    # match between "is ... in"
    # (.*?) captures any characters, non-greedily
    match = re.search(r'is\s+(.*?)\s+in', raw_text, re.IGNORECASE)
    if not match:
        print(f"Format unrecoginised in raw text correction: '{raw_text.strip()}'")
        return None
    target_str = match.group(1).strip()

    corrections = {
        'o': '0',
        'O': '0',
        'l': '1',
        'L': '1',
        'I': '1',
        '/': '7',
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
        config = '--psm 7 -c tessedit_char_whitelist="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ?"'
        raw_text = pytesseract.image_to_string(thresh, config=config)
        
        target = correct_raw_text(raw_text)
        if target:
            print(f"Extracted: {target} from text: '{raw_text.strip()}'")
            return target
        else:
            print((f"Failed to find a number in '{raw_text.strip()}'"))
            return None


def play_round() -> None:
    target = get_number_from_screen()
    if not target: return

    binary_str = format(target, '08b')
    for i, bit in enumerate(binary_str):
        if bit == '1':
            x, y = BUTTON_COORDS[i]
            pyautogui.click(x, y)
    pyautogui.click(x=SUBMIT_BUTTON[0], y=SUBMIT_BUTTON[1])


def main():
    trigger_key = 'e'
    kill_key = 'esc'

    print("--- Binary Racer Bot Started ---")
    print(f"Press '{trigger_key}' to execute one round.")
    print(f"Press '{kill_key} to exit.")

    keyboard.add_hotkey(trigger_key, lambda: play_round())

    keyboard.wait(kill_key)
    print("--- Binary Racer Bot Terminated ---")

if __name__ == "__main__":
    main()