import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect("sensors.db")
cursor = conn.cursor()

# 센서 데이터 조회
cursor.execute("""
SELECT timestamp, temperature, humidity, status, device_id
FROM readings
ORDER BY id DESC
""")

rows = cursor.fetchall()
conn.close()

# HTML 기본 구조
html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>센서 데이터 보고서</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 30px;
        }
        h1 {
            color: #333;
        }
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #ccc;
            padding: 10px;
            text-align: center;
        }
        th {
            background-color: #eee;
        }
    </style>
</head>
<body>
    <h1>센서 데이터 보고서</h1>
    <p>데이터베이스에 저장된 온도 및 습도 데이터</p>

    <table>
        <tr>
            <th>시간</th>
            <th>온도(°C)</th>
            <th>습도(%)</th>
            <th>상태</th>
            <th>장치 ID</th>
        </tr>
"""

# 데이터베이스 내용을 HTML 표에 추가
for row in rows:
    html += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
            <td>{row[3]}</td>
            <td>{row[4]}</td>
        </tr>
    """

# HTML 마무리
html += """
    </table>
</body>
</html>
"""

# HTML 파일 저장
with open("report.html", "w", encoding="utf-8") as file:
    file.write(html)

print("HTML 보고서 생성 완료")
print("저장된 데이터 개수:", len(rows))