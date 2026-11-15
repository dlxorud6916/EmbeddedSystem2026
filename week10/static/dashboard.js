// 메시지 표시 함수
function showMessage(text) {
    const messageEl = document.querySelector("#message");
    if (messageEl) {
        messageEl.textContent = text;
    }
}

// 7.2절: 서버 상태를 비동기로 조회하여 화면 갱신[cite: 38]
async function refreshStatus() {
    try {
        const response = await fetch("/api/status", {
            cache: "no-store"
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        document.querySelector("#temperature").textContent = 
            data.temperature ?? "--";

        document.querySelector("#humidity").textContent = 
            data.humidity ?? "--";

        document.querySelector("#sensor-status").textContent = 
            data.sensor_status ?? "INIT";

        document.querySelector("#led-state").textContent = 
            data.led_state ?? "--";

        document.querySelector("#mode").textContent = 
            data.mode ?? "--";

        document.querySelector("#updated-at").textContent = 
            data.updated_at ?? "--";

    } catch (error) {
        console.error(error);
        showMessage("연결 오류: " + error.message);
    }
}

// 7.3절: 이전 조회가 끝난 뒤 2초 뒤 다음 조회를 예약하는 고정 주기 폴링[cite: 40]
async function poll() {
    await refreshStatus();
    window.setTimeout(poll, 2000);
}

// 7.5절: 브라우저에서 서버로 LED 제어 POST 요청 전송[cite: 46]
async function setLed(state) {
    const response = await fetch("/api/led", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ state })
    });

    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.error ?? "request failed");
    }

    console.log("명령 접수:", result);
    await refreshStatus();
}

// 7.5절: ON/OFF 버튼에 클릭 이벤트 연결[cite: 46]
document.querySelectorAll("[data-state]").forEach(button => {
    button.addEventListener("click", () => {
        setLed(button.dataset.state).catch(error => {
            console.error(error);
            showMessage("제어 실패: " + error.message);
        });
    });
});

// 페이지 로드 시 폴링 시작
poll();