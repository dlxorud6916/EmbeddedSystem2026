from gpiozero import LED
from time import sleep

# BCM GPIO17 핀 객체 생성
led = LED(17)

try:
    print("LED ON")
    led.on()
    sleep(2)
finally:
    print("LED OFF & Cleaned Up")
    led.off()
    led.close()