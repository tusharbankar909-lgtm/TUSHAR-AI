import os, shutil, uuid
from pathlib import Path
import requests
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
BASE=Path(__file__).resolve().parent; UPLOADS=BASE/'uploads'; UPLOADS.mkdir(exist_ok=True)
app=FastAPI(title='TUSHAR AI'); app.mount('/static',StaticFiles(directory=BASE/'static'),name='static')
OLLAMA_URL=os.getenv('OLLAMA_URL','http://127.0.0.1:11434'); DEFAULT_MODEL=os.getenv('OLLAMA_MODEL','qwen2.5:3b')
@app.get('/')
def home(): return FileResponse(BASE/'static/index.html')
@app.get('/api/health')
def health():
    try: ok=requests.get(f'{OLLAMA_URL}/api/tags',timeout=2).ok
    except: ok=False
    return {'ok':True,'ollama':ok,'model':DEFAULT_MODEL}
@app.post('/api/chat')
async def chat(payload:dict):
    msg=payload.get('message',''); model=payload.get('model') or DEFAULT_MODEL
    if not msg:return {'error':'Message required'}
    try:
        r=requests.post(f'{OLLAMA_URL}/api/chat',json={'model':model,'messages':[{'role':'user','content':msg}],'stream':False},timeout=120); r.raise_for_status(); return {'reply':r.json().get('message',{}).get('content',''),'model':model}
    except Exception as e:return {'reply':'Local AI is not running. Start Ollama and pull the model.','error':str(e)}
@app.post('/api/upload')
async def upload(file:UploadFile=File(...)):
    safe=Path(file.filename or 'file').name; dest=UPLOADS/f'{uuid.uuid4().hex}_{safe}'
    with dest.open('wb') as f: shutil.copyfileobj(file.file,f)
    return {'name':safe,'path':dest.name,'size':dest.stat().st_size}
@app.post('/api/storyboard')
async def storyboard(payload:dict):
    story=payload.get('story','').strip(); model=payload.get('model') or DEFAULT_MODEL
    if not story:return {'error':'Story required'}
    prompt=f'''Create a video storyboard from this story. Return JSON only with a scenes array. Each scene must contain scene, duration_seconds, visual_prompt, narration. Story:\n{story}'''
    try:
        r=requests.post(f'{OLLAMA_URL}/api/chat',json={'model':model,'messages':[{'role':'user','content':prompt}],'stream':False},timeout=120); r.raise_for_status(); return {'storyboard':r.json().get('message',{}).get('content','')}
    except Exception as e:return {'storyboard':'AI storyboard unavailable. Start Ollama first.','error':str(e)}
@app.get('/api/tools')
def tools(): return {'tools':['AI Chat','Female Voice','Image Generator','HD/4K Upscaler','Background Remover','OCR','PDF Chat','Translator','Speech-to-Text','Text-to-Speech','Study Tutor','Notes','CSV/Excel Analyzer','Website Builder','Code Helper','Debugger','Project ZIP Builder','Web Research','AI Agent','Story to Video']}
