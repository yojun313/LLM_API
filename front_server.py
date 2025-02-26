from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel

app = FastAPI()

# 내부 Docker Ollama 컨테이너 주소 (localhost:11434)
OLLAMA_API_URL = "http://localhost:11434/api/generate"


class RequestModel(BaseModel):
    model: str
    prompt: str
    stream: bool = False


@app.post("/generate")
def generate_text(request: RequestModel):
    """
    외부에서 받은 요청을 내부 Ollama 컨테이너로 전달하고 응답을 반환
    """
    try:
        # Ollama 컨테이너로 요청 전송
        response = requests.post(OLLAMA_API_URL, json=request.dict())

        # Ollama의 응답을 외부 클라이언트로 반환
        return response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ollama 컨테이너 요청 실패: {str(e)}")

