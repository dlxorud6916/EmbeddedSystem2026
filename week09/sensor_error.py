import random
import time

try:
    while True:
        try:
            temperature = round(random.uniform(20.0, 30.0), 1)
            humidity = round(random.uniform(40.0, 70.0), 1)

            error = random.choice([True, False, False])

            if error:
                raise Exception("센서 연결 오류")

            print("온도:", temperature, "°C")
            print("습도:", humidity, "%")
            print("--------------------")

        except Exception as e:
            print("센서 데이터 수집 오류:", e)
            print("--------------------")

        time.sleep(2)

except KeyboardInterrupt:
    print("\n프로그램 종료")
