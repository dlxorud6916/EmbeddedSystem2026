import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect("sensors.db")
cursor = conn.cursor()

# 조회할 기간 설정
start_time = "2026-11-08T00:00:00+09:00"
end_time = "2026-11-08T23:59:59+09:00"

# 지정한 기간의 정상 데이터 조회
cursor.execute("""
SELECT *
FROM readings
WHERE timestamp BETWEEN ? AND ?
AND status = 'OK'
ORDER BY timestamp ASC
""", (start_time, end_time))

rows = cursor.fetchall()

# 조회 결과 출력
if rows:
    print("기간별 센서 데이터")
    print("--------------------")

    for row in rows:
        print("ID:", row[0])
        print("측정 시간:", row[1])
        print("온도:", row[2], "°C")
        print("습도:", row[3], "%")
        print("상태:", row[4])
        print("--------------------")
else:
    print("해당 기간에 저장된 데이터가 없습니다.")

# 연결 종료
conn.close()
