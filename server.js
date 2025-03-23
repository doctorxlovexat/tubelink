const express = require('express');
const ytDlp = require('yt-dlp');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static('public'));

let streamURL = "";

app.post('/start-stream', (req, res) => {
    const url = req.body.url;
    ytDlp.exec([url, '-f', 'bestaudio'], {
        stdOut: 'pipe',
        stdErr: 'pipe',
    }).then(output => {
        streamURL = output[0];
        res.status(200).send({ message: 'Stream Started', streamURL });
    }).catch(err => {
        res.status(500).send({ error: err.message });
    });
});

app.post('/stop-stream', (req, res) => {
    // Logic to stop stream if needed (terminate process)
    streamURL = '';
    res.status(200).send({ message: 'Stream Stopped' });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
