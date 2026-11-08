
import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect("sensors.db")
cursor = conn.cursor()

# 테이블 생성
cursor.execute("""
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    temperature REAL,
    humidity REAL,
    status TEXT,
    device_id TEXT,
    error_message TEXT
)
""")

# 변경 사항 저장
conn.commit()

print("readings 테이블 생성 완료")

# 연결 종료
conn.close()
