# Gesture-Controlled Snake Game

A classic Snake game implemented in Python using Turtle graphics, controlled by hand gestures detected via OpenCV and a custom `HandGesture` class. The game runs in a window where players navigate the snake to eat balls, grow longer, and achieve high scores—all using gestures like "up," "down," "left," "right," and "exit" to control movement.

---

## Features

- **Gesture Control:** Use hand gestures to direct the snake (up, down, left, right, or exit).
- **Turtle Graphics:** Visuals rendered with Python's Turtle module for a simple, retro game feel.
- **Score Tracking:** Displays current score and high score, saved to a `Highscore.txt` file.
- **Boundary Wrapping:** Snake wraps around the screen edges for continuous play.
- **Collision Detection:** Game ends if the snake bites itself; score updates when eating balls.

---

## Prerequisites

- **Python 3.x**

### Required libraries:

- `turtle` (built-in)
- `opencv-python` (`pip install opencv-python`)
- `numpy` (dependency for OpenCV, `pip install numpy`)
- `asyncio` (built-in)
- A custom `HandGesture` class/module for gesture detection (not included in this repo; ensure it's implemented or sourced)
- **Webcam** for gesture detection

---

## How to Run

1. **Clone or download this repository.**
2. **Install the required libraries:**
    ```bash
    pip install opencv-python numpy
    ```
3. **Ensure your `hand_gesture.py` (or equivalent) is present in the project directory.**
4. **Connect your webcam.**
5. **Run the game:**
    ```bash
    python main.py
    ```
6. **Control the snake using your hand gestures!**
    - Raise your hand and move it in the direction you want the snake to go.
    - Show only the middle finger to exit the game.

---

## Notes

- The `HandGesture` class/module is required for gesture detection. If not included, you must implement or source it separately.
- The game saves your high score in `Highscore.txt` in the same directory.
- If you encounter issues with the webcam or gesture detection, ensure your webcam is properly connected and not used by another application.

---

Enjoy playing Snake with your hands!
