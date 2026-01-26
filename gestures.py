
import math

def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def is_pinch(lm, threshold):
    return distance(lm[4], lm[8]) < threshold

def is_right_pinch(lm, threshold):
    return distance(lm[4], lm[12]) < threshold

def is_open_palm(lm):
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    return all(lm[t][1] < lm[p][1] for t, p in zip(tips, pips))

def swipe_direction(start_x, current_x, threshold):
    if current_x - start_x > threshold:
        return "right"
    elif start_x - current_x > threshold:
        return "left"
    return None
