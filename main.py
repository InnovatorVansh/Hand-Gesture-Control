import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import cv2
import mediapipe as mp
import pyautogui
import time

import config
import gestures
import actions

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)
draw = mp.solutions.drawing_utils

# Try camera indices
cap = None
for idx in [0, 1, 2]:
    test = cv2.VideoCapture(idx)
    if test.isOpened():
        cap = test
        print(f"Camera opened on index: {idx}")
        break
    test.release()

if cap is None:
    print("ERROR: Could not open any camera (0/1/2). Check Windows camera permissions + close apps using camera.")
    raise SystemExit(1)

screen_w, screen_h = pyautogui.size()
prev_x, prev_y = 0, 0
dragging = False
swipe_start_x = None
last_right_click_time = 0

while True:
    success, frame = cap.read()
    if not success:
        print("ERROR: Failed to read frame from camera.")
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        lm = [(int(p.x * w), int(p.y * h)) for p in hand.landmark]
        draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        ix, iy = lm[8]
        mx = int(ix / w * screen_w)
        my = int(iy / h * screen_h)

        curr_x = prev_x + (mx - prev_x) / config.SCREEN_SMOOTHING
        curr_y = prev_y + (my - prev_y) / config.SCREEN_SMOOTHING
        actions.move_mouse(curr_x, curr_y)
        prev_x, prev_y = curr_x, curr_y

        pinch = gestures.is_pinch(lm, config.PINCH_THRESHOLD)
        right_pinch = gestures.is_right_pinch(lm, config.PINCH_THRESHOLD)
        now = time.time()

        # Drag with pinch-hold
        if pinch and not dragging:
            actions.mouse_down()
            dragging = True
        elif not pinch and dragging:
            actions.mouse_up()
            dragging = False

        # Right click with thumb+middle pinch
        if right_pinch and (now - last_right_click_time) > config.CLICK_COOLDOWN:
            actions.right_click()
            last_right_click_time = now

        # Swipe for Alt-Tab (simple)
        if swipe_start_x is None:
            swipe_start_x = ix
        direction = gestures.swipe_direction(swipe_start_x, ix, config.SWIPE_THRESHOLD)
        if direction:
            actions.alt_tab()
            swipe_start_x = None

    cv2.putText(frame, "ESC to quit", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
  