# 🎧 Audiolight: Immersive Reading Experience

Audiolight turns plain text into an immersive, dual-sensory reading experience — syncing high-quality audio with dynamic word-by-word highlighting in real time.

It’s like karaoke, but for articles.

Built for people who want to retain more, focus better, or just enjoy reading in a new way.

---

## ✨ What It Does

1. **You paste any text** — longform, shortform, whatever.  
2. **It speaks it out loud** using macOS' native TTS engine.  
3. **It runs forced alignment** using Gentle to get word-level timings.  
4. **You see every word highlighted** exactly when it’s being spoken.  

All in the browser. No extensions. No fluff. Just flow.

---

## 🧠 Why This Exists

Reading and listening together hits different.  
Audiobooks are great, but they don’t show you the words.  
Visual readers are fast, but they don’t make things *stick*.  

Audiolight tries to bridge that gap — using two senses instead of one, and syncing them precisely.

---

## 🛠️ Tech Stack

- **Frontend:** HTML + vanilla JS  
- **Backend:** Python (Flask)  
- **TTS:** macOS `say` command  
- **Alignment:** [Gentle](https://github.com/lowerquality/gentle) via Docker  
- **Audio processing:** `ffmpeg`

---

## 🧪 Run Locally

1. Clone this repo:

    ```bash
    git clone https://github.com/YOURUSERNAME/audiolight.git
    cd audiolight
    ```

2. (Optional) Create a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:

    ```bash
    pip install flask flask-cors requests
    ```

4. Make sure you have:
    - macOS (for `say`)
    - Docker + Gentle running on port 8767
    - `ffmpeg` installed (`brew install ffmpeg`)

5. Run the Flask server:

    ```bash
    python server.py
    ```

6. Serve the frontend in a second terminal:

    ```bash
    python -m http.server 8000
    ```

7. Open:

    ```
    http://127.0.0.1:8000/index.html
    ```

Paste some text. Click Proceed.  
Hit play. Watch the words light up.  
Welcome to Audiolight.

---

## 🧩 What’s Next

- UI polish  
- Timing offsets for smoother feel  
- Exportable HTML player  
- Chrome extension?  
- Mobile support  

---

## 👀 Demo

Coming soon.

---

## 📣 Author

Built by [@prakhargupta](https://github.com/prakhargupta)  
Because the world needs more readers — and better ways to read.
