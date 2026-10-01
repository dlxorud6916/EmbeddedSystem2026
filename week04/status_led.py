from gpiozero import LED
from time import sleep

led = LED(17)

def show_ok():
    print("Status: OK (Slow Blink)")
    led.blink(1.0, 1.0)

def show_warning():
    print("Status: WARNING (Fast Blink)")
    led.blink(0.2, 0.2)

def show_error():
    print("Status: ERROR (Pattern)")
    led.off()
    for _ in range(3):
        led.on(); sleep(0.1)
        led.off(); sleep(0.1)
    sleep(1.5)

try:
    show_ok()
    sleep(4)
    show_warning()
    sleep(4)
    show_error()
    sleep(5)
finally:
    led.close()