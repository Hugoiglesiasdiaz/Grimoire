from sys import path
path.append("./python")
from leer_archivos import leer_archivos
from buscador_logica import buscar_informacion

from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

import uvicorn

import json

from pathlib import Path
import os

from typing import List

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/javascript", StaticFiles(directory="javascript"), name="javascript")

UPLOAD_FOLDER = 'testfiles'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def read_template(template_name: str) -> str:
    template_path = Path("templates") / template_name
    return template_path.read_text(encoding='utf-8')

@app.get('/', response_class=HTMLResponse)
def home():
    return read_template('index.html')

@app.post('/upload', response_class=JSONResponse)
async def upload_file(files: List[UploadFile] = File(...)):
    if not files:
        return {"success": False, "message": "No se seleccionó ningún archivo.", "count": 0}
        
    uploaded_count = 0
    for file in files:
        if file.filename:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            uploaded_count += 1
            
    if uploaded_count > 0:
        return {
            "success": True, 
            "message": f"¡Subida completada! {uploaded_count} archivo(s) guardado(s) correctamente.",
            "count": uploaded_count
        }
    else:
        return {"success": False, "message": "Hubo un problema al guardar los archivos.", "count": 0}

@app.get('/about', response_class=HTMLResponse)
def about():
    return read_template('about.html')

@app.get('/read-files', response_class=JSONResponse)
def read_files():
    json_data = leer_archivos()
    return json.loads(json_data)

@app.get('/buscador', response_class=HTMLResponse)
def buscador():
    return read_template('buscador.html')

@app.get('/api/buscar', response_class=JSONResponse)
def api_buscar(q: str = Query("", description="Término de búsqueda")):
    query = q.strip()
    
    if query:
        resultados = buscar_informacion(query)
    else:
        resultados = []
        
    return resultados

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)

