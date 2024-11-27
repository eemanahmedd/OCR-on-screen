import cv2
import numpy as np
import mss
import keyboard

# Global variables
drawing = False
ix, iy = -1, -1
rect = None
screen = None
roi = None  # To store the selected ROI


def draw_rectangle(event, x, y, flags, param):
    """
    Mouse callback function to draw a rectangle on the screen capture.
    """
    global ix, iy, drawing, rect, roi, screen

    if event == cv2.EVENT_LBUTTONDOWN:
        # Start drawing the rectangle
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        # Update the rectangle as the mouse moves
        if drawing:
            temp_screen = screen.copy()
            cv2.rectangle(temp_screen, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow('Screen', temp_screen)

    elif event == cv2.EVENT_LBUTTONUP:
        # Finalize the rectangle and extract the ROI
        drawing = False
        rect = (ix, iy, x, y)
        cv2.rectangle(screen, (ix, iy), (x, y), (0, 255, 0), 2)
        cv2.imshow('Screen', screen)

        # Extract the ROI
        x1, y1, x2, y2 = rect
        roi = screen[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2)]


def capture_screen():
    """
    Captures the primary monitor's screen and returns it as a NumPy array.
    """
    with mss.mss() as sct:
        screen_size = sct.monitors[1]
        screen_shot = sct.grab(screen_size)
        screen = np.array(screen_shot)
        return cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)


def select_screen_roi():
    """
    Captures the screen, lets the user select an ROI, and returns the ROI.
    """
    global screen, roi

    print("Press 'c' to capture the screen and 'q' to quit.")
    while True:
        if keyboard.is_pressed('c'):
            print("Screen captured. Draw a rectangle to select ROI.")
            screen = capture_screen()

            cv2.namedWindow('Screen')
            cv2.setMouseCallback('Screen', draw_rectangle)

            while True:
                cv2.imshow('Screen', screen)
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # Esc key to finish
                    break

            cv2.destroyWindow('Screen')
            if roi is not None:
                print("ROI selected.")
                return roi
            else:
                print("No ROI selected. Try again.")

        elif keyboard.is_pressed('q'):
            print("Exiting without ROI selection.")
            break

    cv2.destroyAllWindows()
    return None

