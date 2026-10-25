import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

i2c = busio.I2C(board.SCL, board.SDA)

display = adafruit_ssd1306.SSD1306_I2C(
    128, 64, i2c, addr=0x3C
)

image = Image.new("1", (display.width, display.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

draw.text((0, 0), "Hello OLED", font=font, fill=255)
draw.text((0, 16), "I2C Display", font=font, fill=255)

display.image(image)
display.show()