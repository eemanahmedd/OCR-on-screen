import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  

def perform_ocr(roi_image):
    # Convert ROI to grayscale for better OCR accuracy
    gray_roi = cv2.cvtColor(roi_image, cv2.COLOR_BGR2GRAY)
    
    # Run OCR on the grayscale ROI
    text = pytesseract.image_to_string(gray_roi)
    return text