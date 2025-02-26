from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
import datetime
import json
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM

# uvicorn server_socket:app --host 0.0.0.0 --port 3333 --reload

app = FastAPI()

# 🔹 모델 캐싱 (초기에는 None, 요청이 오면 생성)
ollama_cache = {
    "current_model": None,  # 현재 활성화된 모델 이름
    "llm_instance": None  # 현재 활성화된 모델 객체
}


class RequestData(BaseModel):
    model: str
    prompt: str


def generator(model, text):
    """ 모델이 요청될 때만 생성하고 유지하며, 다른 모델 요청 시 교체 """
    if ollama_cache["current_model"] != model:
        ollama_cache["llm_instance"] = OllamaLLM(model=model)
        ollama_cache["current_model"] = model

    llm = ollama_cache["llm_instance"]
    prompt = PromptTemplate.from_template(template=text)
    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({})
    return result


def save_to_file(model, prompt, answer, filename="C:/GitHub/llm_history.txt"):
    """ 모델 이름, 질문, 답변을 파일에 저장 """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"[ {timestamp} ] - {model}\n")
        file.write(f"Q. {prompt}\n")
        file.write(f"A. {answer}\n\n")
        file.write("=" * 50 + "\n\n")  # 구분선 추가


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """ WebSocket을 통해 클라이언트와 통신 """
    await websocket.accept()
    try:
        while True:
            # 클라이언트에서 JSON 형식의 요청 데이터 수신
            data = await websocket.receive_text()
            request_data = json.loads(data)  # JSON 파싱

            # 필수 데이터 체크
            if "model" not in request_data or "prompt" not in request_data:
                await websocket.send_text(json.dumps({"error": "Both model and prompt are required"}))
                continue

            model = request_data["model"]
            prompt = request_data["prompt"]

            # LLM 응답 생성
            answer = generator(model, prompt)

            # 응답 저장
            save_to_file(model, prompt, answer)

            # 결과를 WebSocket을 통해 전송
            await websocket.send_text(json.dumps({"result": answer}))

    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_text(json.dumps({"error": f"서버 오류: {str(e)}"}))


@app.get("/models")
async def get_models():
    """ 현재 활성화된 모델을 반환 """
    return {
        "current_model": ollama_cache["current_model"]
    }
