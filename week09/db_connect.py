import sqlite3

conn = sqlite3.connect("sensors.db")
cursor = conn.cursor()

print("데이터베이스 연결 완료")