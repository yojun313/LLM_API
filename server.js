const express = require('express');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');

const app = express();
const port = 3333;

// JSON 요청 파싱
app.use(bodyParser.json());

// POST 엔드포인트 생성
app.post('/api/process', (req, res) => {
    const { model_name, question } = req.body;

    if (!model_name || !question) {
        return res.status(400).send({ error: 'Both model_name and question are required' });
    }

    // Python 스크립트 실행
    const python = spawn('python3', ['process.py']);

    let pythonOutput = '';

    python.stdout.on('data', (data) => {
        pythonOutput += data.toString();
    });

    python.stderr.on('data', (data) => {
        console.error(`Python Error: ${data}`);
    });

    python.on('close', (code) => {
        if (code !== 0) {
            return res.status(500).send({ error: 'Python script failed' });
        }
        res.send({ result: pythonOutput.trim() });
    });

    // Python 코드에 입력 전달
    python.stdin.write(JSON.stringify({ model_name, question }));
    python.stdin.end();
});

// 서버 실행
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
