import csv
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

file_path = Path("sensor_data.csv")

now = datetime.now(ZoneInfo("Asia/Seoul"))
timestamp = now.isoformat(timespec="seconds")

temperature = 25.5
humidity = 60.2

file_exists = file_path.exists()

with open(file_path, "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    if not file_exists:
        writer.writerow([
            "timestamp",
            "temperature",
            "humidity"
        ])

    writer.writerow([
        timestamp,
        temperature,
        humidity
    ])

print("데이터 저장 완료")