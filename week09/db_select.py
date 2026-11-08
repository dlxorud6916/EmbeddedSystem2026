import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect("sensors.db")
cursor = conn.cursor()

# 가장 최근 데이터 조회
cursor.execute("""
SELECT *
FROM readings
ORDER BY id DESC
LIMIT 1
""")

row = cursor.fetchone()

# 조회 결과 출력
if row:
    print("최근 센서 데이터")
    print("--------------------")
    print("ID:", row[0])
    print("측정 시간:", row[1])
    print("온도:", row[2], "°C")
    print("습도:", row[3], "%")
    print("상태:", row[4])
    print("장치 ID:", row[5])
    print("오류 메시지:", row[6])
else:
    print("저장된 데이터가 없습니다.")

# 연결 종료
conn.close()
