import sys
import json

def generator(model, text):
    from langchain.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_ollama import OllamaLLM


    llm = OllamaLLM(model="deepseek-r1:14b")

    template = text

    prompt = PromptTemplate.from_template(template=template)
    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({})
    return result

def main():
    # 입력 받기
    input_data = sys.stdin.read()
    data = json.loads(input_data)

    # 모델 이름과 질문 처리
    model_name = data.get("model_name")
    question = data.get("question")

    if not model_name or not question:
        print("Both model_name and question are required", file=sys.stderr)
        return

    answer = generator(model_name, question)

    # 결과 반환
    print(answer)

if __name__ == "__main__":
    main()

