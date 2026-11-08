import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect("sensors.db")
cursor = conn.cursor()

# 센서 데이터 통계 조회
cursor.execute("""
SELECT
    AVG(temperature),
    MIN(temperature),
    MAX(temperature),
    COUNT(*)
FROM readings
WHERE status = 'OK'
""")

stats = cursor.fetchone()

# 조회 결과 출력
print("센서 데이터 통계")
print("--------------------")

if stats[3] > 0:
    print("평균 온도:", round(stats[0], 2), "°C")
    print("최저 온도:", stats[1], "°C")
    print("최고 온도:", stats[2], "°C")
    print("데이터 개수:", stats[3], "개")
else:
    print("저장된 정상 센서 데이터가 없습니다.")

# 연결 종료
conn.close()
