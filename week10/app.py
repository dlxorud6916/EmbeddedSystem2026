from flask import Flask, jsonify, request, render_template
from threading import Lock, Thread
import sqlite3
from queue import Queue, Full
import logging
import time
from device_worker import device_worker

# 9절: 서버 로그 형식 설정 (요청 및 장치 제어 결과 상세 로깅)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app = Flask(__name__)

# 동시 접근 보호용 Lock 및 공유 상태 초기화
state_lock = Lock()
system_state = {
    "temperature": None,
    "humidity": None,
    "sensor_status": "INIT",
    "led_state": "off",
    "mode": "MANUAL",
    "updated_at": None
}

# 제어 명령 전달을 위한 Queue 선언 (최대 10개 제한)
command_queue = Queue(maxsize=10)

def get_current_mode():
    """현재 시스템의 제어 모드(AUTO 또는 MANUAL)를 안전하게 반환합니다."""
    with state_lock:
        return system_state.get("mode", "MANUAL")

# 대시보드 HTML 페이지 반환
@app.get("/")
def dashboard():
    logging.info("web: GET / 200")
    return render_template("index.html")

@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "embedded-web"
    }), 200

# 상태 조회 API
@app.get("/api/status")
def api_status():
    with state_lock:
        snapshot = system_state.copy()
    logging.info("web: GET /api/status 200")
    return jsonify(snapshot), 200

# 센서 기록 조회 API (DB에서 데이터 조회)
@app.get("/api/readings")
def api_readings():
    limit = min(
        request.args.get("limit", 20, type=int),
        100
    )
    with sqlite3.connect("sensors.db") as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT timestamp, temperature, humidity, status
            FROM readings
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,)).fetchall()
    logging.info(f"web: GET /api/readings?limit={limit} 200")
    return jsonify([dict(row) for row in rows]), 200

# 모드 변경 API (AUTO / MANUAL 전환)
@app.post("/api/mode")
def api_mode():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        logging.warning("web: POST /api/mode 400 (Invalid JSON)")
        return jsonify({"error": "request body must be JSON object"}), 400

    mode = body.get("mode")
    if mode not in {"AUTO", "MANUAL"}:
        logging.warning(f"web: POST /api/mode 400 (Invalid mode: {mode})")
        return jsonify({"error": "mode must be AUTO or MANUAL"}), 400

    with state_lock:
        system_state["mode"] = mode
        system_state["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S+09:00")

    logging.info(f"web: POST /api/mode 200 -> mode={mode}")
    return jsonify({
        "success": True,
        "mode": mode
    }), 200

# LED 제어 API (8.2 잘못된 요청 400, 8.3 모드 충돌 409, 8.4 Queue 포화 503 처리)
@app.post("/api/led")
def api_led():
    # 8.2 잘못된 JSON 요청 검증
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        logging.warning("web: POST /api/led 400 (Invalid JSON)")
        return jsonify({
            "error": "request body must be JSON object"
        }), 400

    # state 값이 on 또는 off인지 허용 목록 검증 (예: "blink" 거부 -> 400)
    state = body.get("state")
    if state not in {"on", "off"}:
        logging.warning(f"web: POST /api/led 400 (Invalid state value: {state})")
        return jsonify({
            "error": "state must be on or off"
        }), 400

    # 8.3 AUTO 모드 충돌 검증 (AUTO 모드일 경우 수동 제어 요청 거부 -> 409 Conflict)
    if get_current_mode() != "MANUAL":
        logging.warning("web: POST /api/led 409 (Conflict: manual mode required)")
        return jsonify({
            "error": "manual mode required"
        }), 409

    command = {
        "type": "SET_LED",
        "state": state,
        "source": "browser"
    }

    # 8.4 Queue 포화 검증 (큐가 가득 찬 경우 -> 503 Service Unavailable)
    try:
        command_queue.put(command, timeout=0.2)
    except Full:
        logging.error("web: POST /api/led 503 (Command queue full)")
        return jsonify({
            "error": "command queue full"
        }), 503

    # 정상 접수 시 HTTP 202 Accepted 반환
    logging.info(f"web: POST /api/led 202 (Command accepted: state={state})")
    return jsonify({
        "accepted": True,
        "command": command
    }), 202

if __name__ == "__main__":
    # 백그라운드 워커 스레드 시작
    worker_thread = Thread(
        target=device_worker,
        args=(command_queue, system_state, state_lock),
        daemon=True
    )
    worker_thread.start()
    
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )