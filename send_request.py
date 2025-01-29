def LLM_API(question, model_name = "deepseek-r1:14b"):
    import requests

    # 서버 URL
    url = "http://121.152.225.232:3333/api/process"

    # 전송할 데이터
    data = {
        "model_name": model_name,
        "question": question
    }

    try:
        # POST 요청 보내기
        response = requests.post(url, json=data)

        # 응답 확인
        if response.status_code == 200:
            print(response.json()['result'])
        else:
            print("Failed to get a valid response:", response.status_code, response.text)

    except requests.exceptions.RequestException as e:
        print("Error communicating with the server:", e)


if __name__ == "__main__":
    llm_list = [
        'deepseek-r1:14b',
        'llama3.1-instruct-8b',
        'deepseek-r1:70b',
        'llama3.3',
        'gemma:7b',
        'gemma2:27b'
    ]
    
    question = "너를 만든 회사를 소개해줘"
    LLM_API(question, llm_list[0])