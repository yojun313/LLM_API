from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datetime
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM

# uvicorn fastapi_server:app --host 0.0.0.0 --port 3333 --reload

app = FastAPI()

# 🔹 모델 캐싱 (초기에는 None, 요청이 오면 생성)
ollama_cache = {
    "current_model": None,  # 현재 활성화된 모델 이름
    "llm_instance": None   # 현재 활성화된 모델 객체
}

class RequestData(BaseModel):
    model_name: str
    question: str

def generator(model, text):
    """ 모델이 요청될 때만 생성하고 유지하며, 다른 모델 요청 시 교체 """
    if ollama_cache["current_model"] != model:
        print(f"🔄 모델 변경: {ollama_cache['current_model']} → {model}")
        ollama_cache["llm_instance"] = OllamaLLM(model=model, streaming=True, num_threads=4)
        ollama_cache["current_model"] = model

    llm = ollama_cache["llm_instance"]
    prompt = PromptTemplate.from_template(template=text)
    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({})
    return result

def save_to_file(model_name, question, answer, filename="C:/GitHub/llm_history.txt"):
    """ 모델 이름, 질문, 답변을 파일에 저장 """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"[ {timestamp} ] - {model_name}\n")
        file.write(f"Q. {question}\n")
        file.write(f"A. {answer}\n")
        file.write("=" * 50 + "\n\n")  # 구분선 추가

@app.post("/api/process")
async def generate_response(data: RequestData):
    """ 첫 요청이 오면 모델을 생성하고 유지, 다른 모델 요청이 오면 교체 """
    if not data.model_name or not data.question:
        raise HTTPException(status_code=400, detail="Both model_name and question are required")
    
    answer = generator(data.model_name, data.question)
    save_to_file(data.model_name, data.question, answer)
    return {"result": answer}

@app.get("/models")
async def get_models():
    """ 현재 활성화된 모델을 반환 """
    return {
        "current_model": ollama_cache["current_model"]
    }
