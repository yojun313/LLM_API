const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');  // Axios를 사용해 FastAPI에 요청 보냄
const app = express();
const port = 3333;

// JSON 요청 파싱
app.use(bodyParser.json());

// POST 엔드포인트 생성
app.post('/api/process', async (req, res) => {
    const { model_name, question } = req.body;

    if (!model_name || !question) {
        return res.status(400).send({ error: 'Both model_name and question are required' });
    }

    try {
        // FastAPI 서버에 요청 보내기
        const response = await axios.post('http://localhost:8000/generate', {
            model_name,
            question
        });

        res.send(response.data);  // FastAPI 서버의 응답을 그대로 반환
    } catch (error) {
        console.error("Error communicating with FastAPI:", error);
        res.status(500).send({ error: 'Failed to communicate with Python API' });
    }
});

// 서버 실행
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
