from sys import path
path.append("./python")
import ReadFiles

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from pathlib import Path
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/javascript", StaticFiles(directory="javascript"), name="javascript")

def read_template(template_name: str) -> str:
    template_path = Path("templates") / template_name
    return template_path.read_text(encoding='utf-8')

@app.get('/', response_class=HTMLResponse)
def home():
    return read_template('index.html')

@app.get('/about', response_class=HTMLResponse)
def about():
    return read_template('about.html')

@app.get('/read-files', response_class=JSONResponse)
def read_files():
    # Obtener el JSON como string y parsearlo para retornarlo como diccionario
    json_data = ReadFiles.read_files()
    return json.loads(json_data)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)

