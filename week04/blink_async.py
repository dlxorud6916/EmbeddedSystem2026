from gpiozero import LED
from signal import pause

led = LED(17)

# 백그라운드 비동기 점멸 등록 (ON 0.2초, OFF 0.8초)
led.blink(on_time=0.2, off_time=0.8)

try:
    print("비동기 점멸 동작 중... (Ctrl+C 종료)")
    pause()        # 메인 프로세스가 종료되지 않도록 무한 대기
finally:
    led.close()