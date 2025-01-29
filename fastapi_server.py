from fastapi import FastAPI
from pydantic import BaseModel
import datetime
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM

app = FastAPI()

# Ollama 모델 캐싱 (다시 로딩하지 않도록 유지)
ollama_cache = {}

class RequestData(BaseModel):
    model_name: str
    question: str

def generator(model, text):
    global ollama_cache

    if model not in ollama_cache:
        ollama_cache[model] = OllamaLLM(model=model, streaming=True, num_threads=4)  # 모델 캐싱

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

@app.post("/generate")
async def generate_response(data: RequestData):
    answer = generator(data.model_name, data.question)
    save_to_file(data.model_name, data.question, answer)
    return {"result": answer}
