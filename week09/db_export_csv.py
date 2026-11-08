import csv
import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect("sensors.db")
cursor = conn.cursor()

# 센서 데이터 조회
cursor.execute("SELECT * FROM readings")
rows = cursor.fetchall()

# CSV 파일 생성
with open("export.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)

    # CSV 첫 번째 줄에 제목 작성
    writer.writerow([
        "id",
        "timestamp",
        "temperature",
        "humidity",
        "status",
        "device_id",
        "error_message"
    ])

    # 데이터베이스에서 가져온 데이터 저장
    writer.writerows(rows)

# 데이터베이스 연결 종료
conn.close()

print("CSV 내보내기 완료")
print("저장된 데이터 개수:", len(rows))