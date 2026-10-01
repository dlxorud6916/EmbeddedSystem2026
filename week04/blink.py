from gpiozero import LED
from time import sleep

led = LED(17)

try:
    # 1초 간격으로 5회 점멸
    for count in range(5):
        led.on()
        sleep(0.2)
        led.off()
        sleep(0.8)
        print(f"Loop {count + 1}")
finally:
    led.close()