from gpiozero import Button

button = Button(22)

try:
    print("버튼을 누르세요.")
    button.wait_for_press()
    print("버튼이 눌렸습니다.")
finally:
    button.close()