import time
import logging
import sqlite3
from gpiozero import LED
import board
import adafruit_dht

# 하드웨어 핀 설정 (DHT22 데이터 핀: GPIO18 / LED 제어 핀: GPIO22)
DHT_PIN = board.D18
LED_PIN = 22

# 센서 및 LED 객체 초기화
dht_device = adafruit_dht.DHT22(DHT_PIN)
led = LED(LED_PIN)

def init_db():
    """센서 데이터를 저장할 SQLite 데이터베이스와 테이블을 초기화합니다."""
    with sqlite3.connect("sensors.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                temperature REAL,
                humidity REAL,
                status TEXT NOT NULL
            )
        """)
        conn.commit()

def save_reading(timestamp, temperature, humidity, status):
    """측정된 센서 데이터를 DB에 저장합니다."""
    try:
        with sqlite3.connect("sensors.db") as conn:
            conn.execute("""
                INSERT INTO readings (timestamp, temperature, humidity, status)
                VALUES (?, ?, ?, ?)
            """, (timestamp, temperature, humidity, status))
            conn.commit()
    except Exception as e:
        logging.error(f"DB 저장 오류: {e}")

def device_worker(command_queue, system_state, state_lock):
    """
    주기적으로 실제 센서 값을 읽어 DB에 저장하고, 공유 상태를 갱신하며,
    AUTO 모드 규칙 및 MANUAL 모드 큐 명령을 처리하는 통합 워커입니다.
    """
    init_db()
    logging.info("장치 제어 및 실제 센서 워커가 시작되었습니다.")
    
    while True:
        temperature = None
        humidity = None
        sensor_status = "OK"
        current_time = time.strftime("%Y-%m-%dT%H:%M:%S+09:00")

        # 1. 실제 DHT22 센서 데이터 읽기 시도
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            if temperature is None or humidity is None:
                raise RuntimeError("Sensor returned None value")
        except RuntimeError as error:
            # DHT 센서 특유의 타이밍 에러 발생 시 상태를 ERROR로 기록하되 루프는 유지
            sensor_status = "ERROR"
            logging.warning(f"센서 읽기 재시도 중: {error.args[0]}")
        except Exception as e:
            sensor_status = "ERROR"
            logging.error(f"센서 예외 발생: {e}")

        # 센서 측정값을 SQLite DB에 기록
        save_reading(current_time, temperature, humidity, sensor_status)

        # 2. 공유 상태 갱신 및 AUTO 모드 규칙 평가 (아비트레이션)
        with state_lock:
            system_state["temperature"] = temperature
            system_state["humidity"] = humidity
            system_state["sensor_status"] = sensor_status
            system_state["updated_at"] = current_time
            
            current_mode = system_state.get("mode", "MANUAL")
            
            # 7.7 AUTO 모드 규칙 적용 (온도 임계값 30℃ 기준)
            if current_mode == "AUTO" and sensor_status == "OK" and temperature is not None:
                if temperature >= 30.0:
                    led.on()
                    system_state["led_state"] = "on"
                    logging.info(f"device: AUTO rule applied (t={temperature:.1f}℃ >= 30℃) -> LED ON")
                else:
                    led.off()
                    system_state["led_state"] = "off"
                    logging.info(f"device: AUTO rule applied (t={temperature:.1f}℃ < 30℃) -> LED OFF")

        # 3. 비동기 제어 명령 큐 처리 (MANUAL 모드 수동 제어 등)
        try:
            if not command_queue.empty():
                command = command_queue.get_nowait()
                cmd_type = command.get("type")
                state = command.get("state")
                source = command.get("source")
                
                if cmd_type == "SET_LED":
                    with state_lock:
                        mode_check = system_state.get("mode", "MANUAL")
                    
                    if mode_check == "MANUAL":
                        if state == "on":
                            led.on()
                        elif state == "off":
                            led.off()
                        
                        with state_lock:
                            system_state["led_state"] = state
                            system_state["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S+09:00")
                        
                        logging.info(f"device: LED command source={source} state={state} -> applied")
                    else:
                        logging.warning(f"device: AUTO mode is active, ignoring browser manual command({state})")
                        
                command_queue.task_done()
        except Exception as e:
            pass

        # 센서 측정 주기 (2초 대기)
        time.sleep(2)