import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo

# 데이터베이스 연결
conn = sqlite3.connect("sensors.db")
cursor = conn.cursor()

# 가상 센서 데이터 생성
timestamp = datetime.now(
    ZoneInfo("Asia/Seoul")
).isoformat(timespec="seconds")

temperature = 25.5
humidity = 60.2
status = "OK"
device_id = "sensor_01"
error_message = None

# 데이터 삽입
cursor.execute("""
INSERT INTO readings (
    timestamp,
    temperature,
    humidity,
    status,
    device_id,
    error_message
)
VALUES (?, ?, ?, ?, ?, ?)
""", (
    timestamp,
    temperature,
    humidity,
    status,
    device_id,
    error_message
))

# 변경 사항 저장
conn.commit()

print("센서 데이터 저장 완료")
print("측정 시간:", timestamp)
print("온도:", temperature, "°C")
print("습도:", humidity, "%")

# 연결 종료
conn.close()
