import pytesseract
import cv2

def extract_text(plate_image):
    gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    text = pytesseract.image_to_string(gray, config='--psm 7')
    return ''.join(filter(str.isalnum, text)).upper()
