import cv2
from extract_text_ocr import perform_ocr
from select_roi import select_screen_roi

selected_roi = select_screen_roi()
ocr_text = perform_ocr(selected_roi)

# Save the extracted text to a file
output_file = 'extracted_text.txt'
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(ocr_text)
    
print('text extracted')
