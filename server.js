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

    if (!model_name || !question) {
        return res.status(400).send({ error: 'Both model_name and question are required' });
    }

    // Python 스크립트 실행 (특정 경로 지정)
    const scriptPath = path.join(__dirname, 'process.py'); // Python 파일의 경로 설정
    console.log(scriptPath)
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
        const outputFilePath = 'C:/GitHub/LLM_API/result.txt'; // 파이썬에서 저장한 파일 경로
        fs.readFile(outputFilePath, 'utf8', (err, data) => {
            if (err) {
                console.error('Error reading file:', err);
                return res.status(500).send({ error: 'Failed to read output file' });
            }

            // 파일을 성공적으로 읽은 후 그 데이터를 클라이언트로 전송
            res.send({ result: data });
        });
        fs.unlink(outputFilePath, (err) => {
            if (err) {
                console.error('Error deleting file:', err);
                // 파일 삭제 실패는 응답에 영향을 주지 않음
            }
        });
    });
});

// 서버 실행
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
