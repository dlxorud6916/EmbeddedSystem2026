import time
import board
import adafruit_dht

sensor = adafruit_dht.DHT22(board.D22)

try:
    while True:
        temperature = sensor.temperature
        humidity = sensor.humidity

        print(f"Temperature: {temperature:.1f} C")
        print(f"Humidity: {humidity:.1f} %")
        print("--------------------")

        time.sleep(2)
finally:
    sensor.exit()