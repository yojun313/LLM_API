from fastapi import FastAPI, WebSocket, HTTPException
import requests
from pydantic import BaseModel
import json

app = FastAPI()

# 내부 Docker Ollama 컨테이너 주소 (localhost:11434)
OLLAMA_API_URL = "http://localhost:11434/api/generate"


class RequestModel(BaseModel):
    model: str
    prompt: str
    stream: bool = False


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket을 통해 클라이언트와 통신하고, 내부 Ollama 컨테이너와 데이터를 주고받음
    """
    await websocket.accept()  # 클라이언트의 연결 수락
    try:
        while True:
            # 클라이언트로부터 JSON 데이터 수신
            data = await websocket.receive_text()
            request_data = json.loads(data)  # JSON 형식으로 변환

            # Ollama 컨테이너로 요청 전송
            response = requests.post(OLLAMA_API_URL, json=request_data)
            response_data = response.json()

            # Ollama의 응답을 WebSocket을 통해 클라이언트에게 전송
            await websocket.send_text(json.dumps(response_data))

    except Exception as e:
        await websocket.close()
        raise HTTPException(status_code=500, detail=f"WebSocket 통신 오류: {str(e)}")
