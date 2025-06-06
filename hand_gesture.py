import cv2
import mediapipe as mp

class HandGesture:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands()
        self.draw = mp.solutions.drawing_utils
        self.prev_index_tip = None  # For tracking movement across frames

    def detect(self, frame):
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        gesture = None

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                self.draw.draw_landmarks(frame, handLms, mp.solutions.hands.HAND_CONNECTIONS)

                h, w, _ = frame.shape

                lm = handLms.landmark
                index_tip = lm[8]
                middle_tip = lm[12]
                middle_pip = lm[10]
                ring_tip = lm[16]
                pinky_tip = lm[20]

                cx, cy = int(index_tip.x * w), int(index_tip.y * h)

                # Exit when only middle finger is raised
                if (
                    middle_tip.y < middle_pip.y and
                    index_tip.y > lm[6].y and
                    ring_tip.y > lm[14].y and
                    pinky_tip.y > lm[18].y
                ):
                    gesture = "exit"
                    return frame, gesture  # Exit immediately if middle finger is shown

                # Check direction using change in index tip position
                if self.prev_index_tip:
                    dx = cx - self.prev_index_tip[0]
                    dy = cy - self.prev_index_tip[1]

                    threshold = 20  # Movement threshold in pixels

                    if abs(dx) > abs(dy):
                        if dx > threshold:
                            gesture = "right"
                        elif dx < -threshold:
                            gesture = "left"
                    else:
                        if dy > threshold:
                            gesture = "down"
                        elif dy < -threshold:
                            gesture = "up"

                self.prev_index_tip = (cx, cy)

        return frame, gesture
