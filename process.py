import sys
import json
import datetime

def generator(model, text):
    from langchain.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_ollama import OllamaLLM

    llm = OllamaLLM(model=model)
    template = text
    prompt = PromptTemplate.from_template(template=template)
    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({})
    return result

def save_to_file(model_name, question, answer, filename="C:/GitHub/llm_history.txt"):
    """ 모델 이름, 질문, 답변을 파일에 저장하는 함수 """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"Question: {question}\n")
        file.write(f"[{timestamp}] {model_name}: {answer}\n")
        file.write("=" * 50 + "\n")  # 구분선 추가

def main():
    # 입력 받기
    input_data = json.loads(sys.argv[1])

    # 모델 이름과 질문 처리
    model_name = input_data.get("model_name")
    question = input_data.get("question")

    if not model_name or not question:
        print("Both model_name and question are required {data}", file=sys.stderr)
        return

    # 모델 실행 및 답변 생성
    answer = generator(model_name, question)

    # 결과를 파일에 저장
    save_to_file(model_name, question, answer)

    # 결과 출력
    print(answer)

main()
