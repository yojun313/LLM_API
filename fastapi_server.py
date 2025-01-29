from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datetime
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM

app = FastAPI()

# 🔹 사용할 LLM 모델 리스트
llm_list = [
    'deepseek-r1:14b',
    'llama3.1-instruct-8b',
    'deepseek-r1:70b',
    'llama3.3',
    'gemma:7b',
    'gemma2:27b'
]

# 🔹 모델 캐싱 (서버 시작 시 모든 모델을 미리 생성)
ollama_cache = {model: OllamaLLM(model=model, streaming=True, num_threads=4) for model in llm_list}

class RequestData(BaseModel):
    model_name: str
    question: str

def generator(model, text):
    """ 요청된 모델이 미리 캐싱되어 있다면 바로 사용 """
    if model not in ollama_cache:
        return f"Error: Model '{model}' is not available."

    llm = ollama_cache[model]
    prompt = PromptTemplate.from_template(template=text)
    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({})
    return result

def save_to_file(model_name, question, answer, filename="C:/GitHub/llm_history.txt"):
    """ 모델 이름, 질문, 답변을 파일에 저장 """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"[ {timestamp} ]\n")
        file.write(f"Question: {question}\n")
        file.write(f"{model_name}: {answer}\n")
        file.write("=" * 50 + "\n")  # 구분선 추가

@app.post("/api/process")
async def generate_response(data: RequestData):
    """ 요청된 모델로 질문을 처리하고 결과 반환 (Node.js와 동일한 요청 방식) """
    if not data.model_name or not data.question:
        raise HTTPException(status_code=400, detail="Both model_name and question are required")

    answer = generator(data.model_name, data.question)
    save_to_file(data.model_name, data.question, answer)
    return {"result": answer}

@app.get("/models")
async def get_models():
    """ 현재 캐싱된 모델 목록을 반환 """
    return {"available_models": list(ollama_cache.keys())}
