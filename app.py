from flask import Flask, request, jsonify, render_template
import yt_dlp

app = Flask(__name__)

# Funkcija za preuzimanje audio linka sa YouTube-a
def download_audio(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegAudioConvertor',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(id)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=True)
        return info_dict['id']

@app.route('/')
def home():
    return render_template('index.html')  # HTML stranica za unos linkova

@app.route('/start_stream', methods=['POST'])
def start_stream():
    youtube_url = request.form['url']
    try:
        video_id = download_audio(youtube_url)
        return jsonify({'status': 'success', 'video_id': video_id})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
