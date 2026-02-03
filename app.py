from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Cloud Downloader</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; text-align: center; padding: 20px; background: #222; color: white; }
        input { width: 80%; padding: 15px; margin: 10px 0; border-radius: 5px; border: none; }
        button { background-color: #e62117; color: white; padding: 15px 30px; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <h2>YT to MP3 Cloud</h2>
    <form action="/download" method="post">
        <input type="text" name="url" placeholder="Paste Link..." required>
        <br>
        <button type="submit">Download</button>
    </form>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    download_folder = "/tmp"
    
    # We look for cookies.txt in the current folder
    cookie_path = "cookies.txt"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{download_folder}/%(title)s.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
        
        # --- NEW SETTINGS TO FIX THE ERROR ---
        'cookiefile': cookie_path if os.path.exists(cookie_path) else None,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
            return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
