from gpiozero import Button
from signal import pause

button = Button(22)

def pressed():
    print("버튼을 눌렀습니다.")

button.when_pressed = pressed

try:
    pause()
finally:
    button.close()