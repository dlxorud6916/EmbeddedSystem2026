import time
import board
import adafruit_dht
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

sensor = adafruit_dht.DHT22(board.D22)

i2c = busio.I2C(board.SCL, board.SDA)

display = adafruit_ssd1306.SSD1306_I2C(
    128, 64, i2c, addr=0x3C
)

font = ImageFont.load_default()

try:
    while True:
        try:
            temperature = sensor.temperature
            humidity = sensor.humidity

            image = Image.new(
                "1", (display.width, display.height)
            )
            draw = ImageDraw.Draw(image)

            draw.text(
                (0, 0), "Sensor Monitor",
                font=font, fill=255
            )
            draw.text(
                (0, 20), f"Temp: {temperature:.1f} C",
                font=font, fill=255
            )
            draw.text(
                (0, 40), f"Humi: {humidity:.1f} %",
                font=font, fill=255
            )

            display.image(image)
            display.show()

            print(
                f"Temperature: {temperature:.1f} C, "
                f"Humidity: {humidity:.1f} %"
            )

        except RuntimeError as error:
            print(f"Sensor read error: {error.args[0]}")

        time.sleep(2)

finally:
    sensor.exit()
    display.fill(0)
    display.show()