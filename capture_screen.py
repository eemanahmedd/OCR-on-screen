import cv2
import numpy as np
import mss
import keyboard


# Global variables
drawing = False
ix, iy = -1, -1
rect = None
screen = None


def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, rect, screen

    roi = None
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            temp_screen = screen.copy()
            cv2.rectangle(temp_screen, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow('Screen', temp_screen)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        rect = (ix, iy, x, y)
        cv2.rectangle(screen, (ix, iy), (x, y), (0, 255, 0), 2)
        cv2.imshow('Screen', screen)

        # Extract and display ROI
        x1, y1, x2, y2 = rect
        roi = screen[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2)]
        if roi.size > 0:
            # cv2.imshow('Selected ROI', roi)

            return roi
    

def capture_screen():
    global screen
    screen_size = mss.mss().monitors[1]  # Capture the primary monitor
    with mss.mss() as sct:
        screen_shot = sct.grab(screen_size)
        screen = np.array(screen_shot)
        screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
        
def run_capture_and_return_roi():
    # screen_roi=None
    print("Press 'c' to capture the screen and 'q' to quit.")
    while True:
        if keyboard.is_pressed('c'):
            print("Screen captured. Draw a rectangle to select ROI.")
            capture_screen()
            cv2.namedWindow('Screen')
            cv2.setMouseCallback('Screen', draw_rectangle)
            cv2.imshow('Screen', screen)
            cv2.waitKey(0)
            cv2.destroyWindow('Screen')
            
            # Retrieve the ROI after the user selects it
            screen_roi = draw_rectangle(cv2.EVENT_LBUTTONUP, 0, 0, None, None)

        if keyboard.is_pressed('q'):
            print("Exiting.")
            break
        
    cv2.destroyAllWindows()
    if screen_roi is not None:
        return screen_roi