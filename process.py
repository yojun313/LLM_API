import sys
import json

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

def main():
    # 입력 받기
    input_data = json.loads(sys.argv[1])

    # 모델 이름과 질문 처리
    model_name = input_data["model_name"]
    question = input_data["question"]

    if not model_name or not question:
        print("Both model_name and question are required {data}", file=sys.stderr)
        return

    answer = generator(model_name, question)

    # 결과 반환
    print(answer)

main()

