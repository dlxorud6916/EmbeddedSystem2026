import time
import board
import adafruit_dht

sensor = adafruit_dht.DHT22(board.D22)

success = 0
failure = 0

try:
    while True:
        try:
            temperature = sensor.temperature
            humidity = sensor.humidity

            if temperature is None or humidity is None:
                raise ValueError("값 없음")

            if not (-40 <= temperature <= 80 and 0 <= humidity <= 100):
                raise ValueError("범위 초과")

            success += 1
            print(f"정상 | {temperature:.1f} ℃ | {humidity:.1f} %RH")

        except RuntimeError as error:
            failure += 1
            print(f"재시도 | {error}")

        except ValueError as error:
            failure += 1
            print(f"제외 | {error}")

        print(f"성공: {success}회 | 실패: {failure}회")
        time.sleep(2)

finally:
    sensor.exit()