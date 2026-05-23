from flask import Flask, Response, request
import subprocess
import shutil
import sys


def pip_install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])


# Tarkistetaan ja asennetaan Flask
try:
    import flask
    print(f"Flask on asennettu (versio {flask.__version__}), päivitetään...")
    pip_install("flask")
except ImportError:
    print("Flask ei löydy, asennetaan...")
    pip_install("flask")

from flask import Flask, Response, request

# Tarkistetaan ja asennetaan/päivitetään yt-dlp
try:
    import yt_dlp
    print(f"yt-dlp on asennettu (versio {yt_dlp.version.__version__}), päivitetään...")
    pip_install("yt-dlp")
except ImportError:
    print("yt-dlp ei löydy, asennetaan...")
    pip_install("yt-dlp")

print("Kaikki riippuvuudet kunnossa!")

# Tarkistetaan ffmpeg
FFMPEG = shutil.which("ffmpeg")
if not FFMPEG:
    print("VIRHE: ffmpeg ei löydy PATH:ista!")
    print("Lataa ffmpeg: https://ffmpeg.org/download.html")
    print("Lisää ffmpeg/bin PATH-muuttujaan ja käynnistä uudelleen.")
    sys.exit(1)

PYTHON = sys.executable

print(f"Python: {PYTHON}")
print(f"ffmpeg: {FFMPEG}")

app = Flask(__name__)


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
             "-acodec", "dfpwm",
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
