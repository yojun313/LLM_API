const express = require('express');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const port = 3333;

// JSON 요청 파싱
app.use(bodyParser.json());

// POST 엔드포인트 생성
app.post('/api/process', (req, res) => {
    const { model_name, question } = req.body;

    console.log(req.body)

    if (!model_name || !question) {
        return res.status(400).send({ error: 'Both model_name and question are required' });
    }

    // Python 스크립트 실행 (특정 경로 지정)
    const scriptPath = path.join(__dirname, 'process.py'); // Python 파일의 경로 설정
    const globalInputData = { model_name, question };

    const pythonProcess = spawn('python', ['-u', scriptPath, JSON.stringify(globalInputData)]);

    let pythonOutput = '';

    pythonProcess.stdout.on('data', (data) => {
        pythonOutput += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python Error: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        if (code !== 0) {
            console.error(`Python script exited with code ${code}`);
            return res.status(500).send({ error: 'Python script failed' });
        }
        res.send({ result: pythonOutput.trim() });
    });
});

// 서버 실행
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
