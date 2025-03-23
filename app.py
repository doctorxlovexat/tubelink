import yt_dlp
import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Lista linkova
links = []

# Funkcija za preuzimanje YouTube audio linka
def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'extractaudio': True,
        'audioquality': 1,
        'postprocessors': [{
            'key': 'FFmpegAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Route za početnu stranicu
@app.route('/')
def index():
    return render_template('index.html', links=links)

# Route za dodavanje novog linka
@app.route('/add_link', methods=['POST'])
def add_link():
    if request.method == 'POST':
        url = request.form['url']
        if url not in links:
            links.append(url)
            download_audio(url)  # Preuzmi audio odmah
        return redirect(url_for('index'))

# Route za brisanje linka
@app.route('/delete_link/<url>')
def delete_link(url):
    if url in links:
        links.remove(url)
    return redirect(url_for('index'))

# Pokretanje servera
if __name__ == '__main__':
    app.run(debug=True)
