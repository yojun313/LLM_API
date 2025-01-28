import requests

# 서버 URL
url = "http://121.152.225.232:3333/api/process"

# 전송할 데이터
data = {
    "model_name": "deepseek-r1:14b",
    "question": "Who are you?"
}

try:
    # POST 요청 보내기
    response = requests.post(url, json=data)

    # 응답 확인
    if response.status_code == 200:
        print("Server response:", response.json())
    else:
        print("Failed to get a valid response:", response.status_code, response.text)

except requests.exceptions.RequestException as e:
    print("Error communicating with the server:", e)

