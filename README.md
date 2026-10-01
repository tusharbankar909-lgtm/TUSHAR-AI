# TUSHAR AI — FREE
GitHub-ready frontend + FastAPI backend + local Ollama.

## Windows local setup
Install Python 3.11+, Ollama, then:
`python -m venv .venv`
`\.venv\Scripts\Activate.ps1`
`python -m pip install -r requirements.txt`
`ollama pull qwen2.5:3b`
`python server.py`
Open `http://127.0.0.1:8000`.

## GitHub Pages
GitHub Pages can host the `static/index.html` UI only. It cannot run Python/FastAPI, Ollama, FFmpeg, or AI models. For a public AI link, deploy the backend separately and change the frontend API URL from relative `/api/...` to your backend URL.

## Included
Chat, browser voice input, browser female-voice output when an available female voice exists, file upload, Story→Video storyboard generator, and a free/no-ads/no-paid-lock UI. Full 4K image/video generation requires additional local models and enough hardware.
