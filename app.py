from flask import Flask, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='frontend/dist/assets', template_folder='frontend/dist')
app.secret_key = 'grimoire_super_secret'
app.config['UPLOAD_FOLDER'] = 'testfiles'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    # Servir el index.html construido de React
    return send_from_directory('frontend/dist', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No se ha enviado ninguna parte de archivo.'}), 400
        
    files = request.files.getlist('file')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo.'}), 400
        
    uploaded_files = []
    for file in files:
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded_files.append(filename)
            
    if uploaded_files:
        return jsonify({
            'message': f'¡Subida completada! {len(uploaded_files)} archivo(s) guardado(s) correctamente.',
            'files': uploaded_files
        }), 200
    else:
        return jsonify({'error': 'Hubo un problema al guardar los archivos.'}), 500

# Añadir una ruta comodín para SPA routing si el usuario navega
@app.route('/<path:path>')
def serve_static(path):
    # Si piden un recurso que existe en dist lo damos, sino el index para que el router de React decida.
    dist_dir = os.path.join(app.root_path, 'frontend/dist')
    if os.path.exists(os.path.join(dist_dir, path)):
        return send_from_directory(dist_dir, path)
    return send_from_directory(dist_dir, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
