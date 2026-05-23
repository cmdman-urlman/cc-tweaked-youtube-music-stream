local dfpwm = require("cc.audio.dfpwm")
local url = ...

if not url then
    error("Kaytto: play <youtube_url>")
end

local speaker = peripheral.find("speaker")
if not speaker then
    error("Kaiutinta ei loytynyt")
end

print("Yhdistetaan...")

local res = http.get(
    "http://localhost:8000/stream?url=" .. textutils.urlEncode(url),
    nil,
    true
)

if not res then
    error("HTTP-pyynto epaonnistui")
end

local decoder = dfpwm.make_decoder()

print("Toistetaan...")

while true do
    local chunk = res.read(16384)

    if not chunk then
        break
    end

    local audio = decoder(chunk)

    while not speaker.playAudio(audio) do
        os.pullEvent("speaker_audio_empty")
    end
end

res.close()
print("Valmis")