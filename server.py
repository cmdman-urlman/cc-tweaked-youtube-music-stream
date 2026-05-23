from flask import Flask, Response, request
import subprocess
import shutil
import sys

app = Flask(__name__)

PYTHON = sys.executable
FFMPEG = shutil.which("ffmpeg")

if not FFMPEG:
    print("VIRHE: ffmpeg ei löydy PATH:ista!")
    sys.exit(1)

# Tarkistetaan ja asennetaan yt-dlp tarvittaessa
try:
    import yt_dlp
    print("yt-dlp on jo asennettu")
except ImportError:
    print("yt-dlp ei löydy, asennetaan...")
    subprocess.check_call([PYTHON, "-m", "pip", "install", "yt-dlp"])
    print("yt-dlp asennettu!")

print(f"Python: {PYTHON}")
print(f"ffmpeg: {FFMPEG}")

@app.route("/stream")
def stream():
    url = request.args.get("url")
    if not url:
        return "Puuttuva url-parametri", 400

    print(f"Aloitetaan: {url}")

    try:
        ytdlp = subprocess.Popen(
            [PYTHON, "-m", "yt_dlp", "-f", "bestaudio", "-o", "-", "--quiet", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"yt-dlp käynnistyi, PID={ytdlp.pid}")
    except Exception as e:
        print(f"yt-dlp KAATUI: {e}")
        return f"yt-dlp virhe: {e}", 500

    try:
        ffmpeg = subprocess.Popen(
            [FFMPEG,
             "-i", "pipe:0",
             "-f", "dfpwm",
             "-ac", "1",
             "-ar", "48000",
             "pipe:1"],
            stdin=ytdlp.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"ffmpeg käynnistyi, PID={ffmpeg.pid}")
    except Exception as e:
        print(f"ffmpeg KAATUI: {e}")
        ytdlp.kill()
        return f"ffmpeg virhe: {e}", 500

    def generate():
        try:
            while True:
                data = ffmpeg.stdout.read(4096)
                if not data:
                    err = ffmpeg.stderr.read()
                    if err:
                        print(f"ffmpeg stderr: {err.decode(errors='replace')}")
                    break
                yield data
        finally:
            ffmpeg.kill()
            ytdlp.kill()
            try:
                ffmpeg.wait(timeout=2)
                ytdlp.wait(timeout=2)
            except subprocess.TimeoutExpired:
                pass

    return Response(generate(), mimetype="application/octet-stream")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, threaded=True)