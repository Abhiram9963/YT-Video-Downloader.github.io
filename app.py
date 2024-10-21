from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

def download_video(url):
    ydl_opts = {
        'format': 'best',  # Best quality video
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save to 'downloads' folder
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_file = ydl.prepare_filename(info_dict)  # Path of the downloaded video
    return video_file

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    try:
        video_file = download_video(url)
        return send_file(video_file, as_attachment=True, download_name=os.path.basename(video_file))
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)


