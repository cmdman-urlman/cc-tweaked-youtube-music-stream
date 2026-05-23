# CC Tweaked YouTube-soitin 🎵

Toista YouTube-videoiden ääni suoraan CC: Tweaked -tietokoneella DFPWM1a-koodekin avulla.

---

## Vaatimukset

- Python 3.x
- ffmpeg (PATH:issa)
- CC: Tweaked -modi Minecraftissa + kaiutin (speaker)

> Flask ja yt-dlp asennetaan ja päivitetään **automaattisesti** kun `server.py` käynnistetään.

---

## Asennus

### 1. Asenna ffmpeg

1. Lataa: https://ffmpeg.org/download.html → Windows builds
2. Pura esim. `C:\ffmpeg\`
3. Lisää `C:\ffmpeg\bin` Windowsin PATH-muuttujaan:
   - Ohjauspaneeli → Järjestelmä → Lisäasetukset → Ympäristömuuttujat → Path → Muokkaa → Uusi
4. Käynnistä komentokehote uudelleen ja testaa:
   ```
   ffmpeg -version
   ```

### 2. Lataa Lua-skripti CC: Tweaked -tietokoneelle

Avaa CC: Tweaked -tietokone Minecraftissa ja aja:

```
pastebin get Qv902mAH play.lua
```

---

## Käyttö

### 1. Käynnistä palvelin

Avaa komentokehote `server.py`:n kansiossa ja aja:

```
python server.py
```

Ensimmäisellä käynnistyksellä palvelin asentaa automaattisesti:
- `flask`
- `yt-dlp`

Ja päivittää ne aina uusimpaan versioon. Näet tulosteen:

```
yt-dlp on asennettu, päivitetään...
Flask on asennettu, päivitetään...
Kaikki riippuvuudet kunnossa!
Python: C:\...\python.exe
ffmpeg: C:\ffmpeg\bin\ffmpeg.exe
* Running on http://0.0.0.0:8000
```

### 2. Toista musiikkia

CC: Tweaked -tietokoneella:

```
play.lua <youtube-url>
```

Esimerkki:

```
play.lua https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

---

## Tiedostorakenne

```
server.py   - Flask-palvelin (asentaa riippuvuudet automaattisesti)
play.lua        - CC: Tweaked Lua-skripti (pastebin: Qv902mAH)
```

---

## Tekniset tiedot

| Asetus | Arvo |
|--------|------|
| Koodekki | DFPWM1a |
| Näytteenottotaajuus | 48000 Hz |
| Kanavat | Mono |
| Chunk-koko | 16384 tavua |
| Portti | 8000 |

---

## Ongelmatilanteet

**ffmpeg ei löydy**
→ Varmista että ffmpeg on PATH:issa. Testaa `ffmpeg -version` komentorivillä.

**HTTP-pyyntö epäonnistui CC:ssä**
→ Varmista että `server.py` on käynnissä. Tarkista IP-osoite tulosteesta ja että olet samassa verkossa.
→ CC: Tweaked estää oletuksena yhteydet paikallisiin IP-osoitteisiin. Korjaa se muokkaamalla `.minecraft/config/computercraft-server.toml` tiedostoa. Etsi tämä kohta:
```toml
[[http.rules]]
    #The magic "$private" host matches all private address ranges, such as localhost and 192.168.0.0/16.
    #This rule prevents computers accessing internal services, and is strongly recommended.
    host = "$private"
    #deny all requests to private IP addresses.
    action = "deny"
```
Muuta `action = "deny"` → `action = "allow"`:
```toml
[[http.rules]]
    #The magic "$private" host matches all private address ranges, such as localhost and 192.168.0.0/16.
    #This rule prevents computers accessing internal services, and is strongly recommended.
    host = "$private"
    #Allow all requests to private IP addresses.
    action = "allow"
```
Käynnistä Minecraft uudelleen muutoksen jälkeen.

**Ei ääntä / kaiutinta ei löydy**
→ Varmista että CC: Tweaked -tietokoneeseen on liitetty `speaker`-periferia.

**yt-dlp ei lataa videota**
→ Käynnistä `server.py` uudelleen — se päivittää yt-dlp:n automaattisesti.
