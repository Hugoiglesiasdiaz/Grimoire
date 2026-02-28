from flask import Flask, request, jsonify, send_from_directory
import os
import json
import uuid
import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='frontend/dist/assets', template_folder='frontend/dist')
app.secret_key = 'grimoire_super_secret'
app.config['UPLOAD_FOLDER'] = 'testfiles'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
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
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            file_size = os.path.getsize(filepath)
            file_ext = os.path.splitext(filename)[1].lower().replace('.', '') or 'unknown'

            metadata = {
                "id": str(uuid.uuid4()),
                "fileName": filename,
                "originalFileName": file.filename,
                "fileType": file_ext,
                "fileSize": file_size,
                "uploadDate": datetime.datetime.now().isoformat(),
                "filePath": filepath,
                "extractedText": "",
                "textLength": 0,
                "summary": "",
                "category": "Uncategorized",
                "tags": "[]",
                "aiProcessed": False,
                "aiProcessedDate": None
            }

            with open(f"{filepath}.metadata.json", 'w', encoding='utf-8') as mf:
                json.dump(metadata, mf, indent=4)

            uploaded_files.append(filename)

    if uploaded_files:
        return jsonify({
            'message': f'¡Subida completada! {len(uploaded_files)} archivo(s) guardado(s) correctamente.',
            'files': uploaded_files
        }), 200
    else:
        return jsonify({'error': 'Hubo un problema al guardar los archivos.'}), 500


@app.route('/api/search', methods=['POST'])
def search_api():
    req_data = request.get_json() or {}
    query = req_data.get('searchTerm', '').lower()
    current_page = req_data.get('current', 1)
    results_per_page = req_data.get('resultsPerPage', 20)
    sort = req_data.get('sort', [])

    # Read all metadata files from testfiles/
    all_files = []
    upload_folder = app.config['UPLOAD_FOLDER']
    for fname in os.listdir(upload_folder):
        if fname.endswith('.metadata.json'):
            meta_path = os.path.join(upload_folder, fname)
            with open(meta_path, 'r', encoding='utf-8') as f:
                try:
                    all_files.append(json.load(f))
                except json.JSONDecodeError:
                    pass

    # Text query filtering (empty query = return all)
    filtered = []
    for item in all_files:
        if query:
            searchable = f"{item.get('fileName', '')} {item.get('extractedText', '')} {item.get('summary', '')}".lower()
            if query not in searchable:
                continue
        filtered.append(item)

    # Sorting
    if sort:
        sort_field = sort[0].get('field', '')
        sort_dir = sort[0].get('direction', 'asc')
        reverse = sort_dir == 'desc'
        if sort_field in ['fileName', 'title']:
            filtered.sort(key=lambda x: x.get('fileName', '').lower(), reverse=reverse)
        elif sort_field in ['uploadDate', 'date']:
            filtered.sort(key=lambda x: x.get('uploadDate', ''), reverse=reverse)

    # Format for Elastic Search UI
    results_formatted = []
    for item in filtered:
        formatted_item = {k: {'raw': v} for k, v in item.items()}
        results_formatted.append(formatted_item)

    # Pagination
    start = (current_page - 1) * results_per_page
    end = start + results_per_page
    paged_results = results_formatted[start:end]

    return jsonify({
        'meta': {
            'page': {
                'current': current_page,
                'total_pages': max(1, (len(filtered) + results_per_page - 1) // results_per_page),
                'total_results': len(filtered),
                'size': results_per_page
            }
        },
        'results': paged_results,
        'facets': {}
    }), 200


@app.route('/files/<filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/<path:path>')
def serve_static(path):
    dist_dir = os.path.join(app.root_path, 'frontend/dist')
    if os.path.exists(os.path.join(dist_dir, path)):
        return send_from_directory(dist_dir, path)
    return send_from_directory(dist_dir, 'index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
