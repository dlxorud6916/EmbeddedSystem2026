from gpiozero import Button
from signal import pause

button = Button(
    22,
    bounce_time=0.1,
    hold_time=2.0
)

def pressed():
    print("버튼을 눌렀습니다.")

def held():
    print("2초 이상 누름")

button.when_pressed = pressed
button.when_held = held

try:
    pause()
finally:
    button.close()