import asyncio
import platform
import turtle
import random
import cv2
from hand_gesture import HandGesture
import threading
import queue

# Initialize gesture detection
gesture_detector = HandGesture()
cap = cv2.VideoCapture(0)
current_gesture = queue.Queue()

def gesture_loop():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)  # Flip to fix lateral inversion
        frame, gesture = gesture_detector.detect(frame)
        if gesture:
            current_gesture.put(gesture)
            if gesture == "exit":
                break
        cv2.imshow("Gesture Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# Start gesture detection in a separate thread
gesture_thread = threading.Thread(target=gesture_loop, daemon=True)
gesture_thread.start()

# Initialize turtle
S = turtle.Screen()
S.setup(width=630, height=630)
S.bgcolor("Light Green")
S.title("Snakeeyy")
S.tracer(0)
parts = []

# Snake part creation
def snake():
    nPart = turtle.Turtle("square")
    nPart.penup()
    nPart.shapesize(0.9)
    nPart.color("Dark Grey")
    nPart.goto((-20 * len(parts), 0))
    parts.append(nPart)
    nPart.hideturtle()

# Change snake direction
def dir(a):
    if (a + 180) % 360 != head.heading() % 360:
        head.setheading(a)

# Initialize snake
for _ in range(3):
    snake()
head = parts[0]

# Initialize ball
noball = 1
sBall = turtle.Turtle("circle")
sBall.color("LightCoral")
sBall.shapesize(1)
sBall.penup()
sBall.hideturtle()

# Score display
writer = turtle.Turtle()
writer.turtlesize(10)
writer.hideturtle()
writer.penup()

score = 0
try:
    with open("Highscore.txt", "r+") as file:
        HS = int(file.read())
except:
    HS = 0

def updateScore(v):
    global score, HS
    writer.goto(0, turtle.window_height() / 2 - 50)
    writer.clear()
    if v == "over":
        writer.color("Red")
        writer.write(f"Score: Snake bit itself!", align="center", font=("Arial", 24, "bold"))
        return
    score += v
    if score > HS:
        HS = score
    writer.write(f"Score: {score}  High Score: {HS}", align="center", font=("Arial", 24, "bold"))

updateScore(0)

# Map gestures to directions
gesture_to_direction = {
    "up": 90,
    "down": 270,
    "left": 180,
    "right": 0
}

async def main():
    global noball, game
    game = True
    while game:
        S.update()
        # Process gestures
        try:
            gesture = current_gesture.get_nowait()
            if gesture == "exit":
                game = False
                break
            if gesture in gesture_to_direction:
                dir(gesture_to_direction[gesture])
        except queue.Empty:
            pass

        # Update snake parts
        for p in range(len(parts)):
            parts[p].showturtle()
            if p != 0:
                parts[len(parts) - p].goto(parts[len(parts) - p - 1].position())
                parts[len(parts) - p].setheading(parts[len(parts) - p - 1].heading())

        # Check for collision with self
        for p in range(3, len(parts)):
            if head.distance(parts[p]) < 20:
                updateScore("over")
                game = False
                break

        # Move head
        head.fd(20)

        # Spawn ball
        if noball:
            noball = 0
            sBall.showturtle()
            sBall.goto(random.randint(-280, 280), random.randint(-280, 280))

        # Check for ball collision
        if head.distance(sBall) <= 20:
            noball = 1
            sBall.hideturtle()
            updateScore(10)
            snake()

        # Boundary wrapping
        if head.xcor() > 301:
            head.goto(-300, head.ycor())
        elif head.xcor() < -301:
            head.goto(300, head.ycor())
        elif head.ycor() > 301:
            head.goto(head.xcor(), -300)
        elif head.ycor() < -301:
            head.goto(head.xcor(), 300)

        await asyncio.sleep(0.15)

    # Save high score
    try:
        with open("Highscore.txt", "w") as file:
            file.write(str(HS))
    except:
        pass
    S.bye()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())