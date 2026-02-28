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

# app.secret_key = 'grimoire_super_secret'

# app.config['UPLOAD_FOLDER'] = 'testfiles'
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def read_template(template_name: str) -> str:
    template_path = Path("templates") / template_name
    return template_path.read_text(encoding='utf-8')

@app.get('/', response_class=HTMLResponse)
def home():
    return read_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Error: No se ha enviado ninguna parte de archivo.', 'error')
        return redirect(url_for('home'))
        
    files = request.files.getlist('file')
    if not files or files[0].filename == '':
        flash('Error: No se seleccionó ningún archivo.', 'error')
        return redirect(url_for('home'))
        
    uploaded_count = 0
    for file in files:
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded_count += 1
            
    if uploaded_count > 0:
        flash(f'¡Subida completada! {uploaded_count} archivo(s) guardado(s) correctamente.', 'success')
    else:
        flash('Error: Hubo un problema al guardar los archivos.', 'error')
        
    return redirect(url_for('home'))

@app.route('/about', response_class=HTMLResponse)
def about():
    return read_template('about.html')

@app.get('/read-files', response_class=JSONResponse)
def read_files():
    # Obtener el JSON como string y parsearlo para retornarlo como diccionario
    json_data = ReadFiles.read_files()
    return json.loads(json_data)

@app.route('/buscador', response_class=HTMLResponse)
def buscador():
    return read_template('Buscador.html')

@app.route('/api/buscar', methods=['GET'])
def api_buscar():
    query = request.args.get('q', '').strip()
    
    if query:
        # Aquí conectamos tú lógica de búsqueda que separaste en buscador_logica.py
        resultados = buscar_informacion(query)
    else:
        resultados = []
        
    return jsonify(resultados)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)

