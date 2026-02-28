from flask import Flask, request, jsonify, send_from_directory
import os
import json
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

@app.route('/api/search', methods=['POST'])
def search_api():
    req_data = request.get_json() or {}
    query = req_data.get('searchTerm', '').lower()
    filters = req_data.get('filters', [])
    current_page = req_data.get('current', 1)
    results_per_page = req_data.get('resultsPerPage', 20)

    try:
        with open('testfiles/mock_data.json', 'r', encoding='utf-8') as f:
            all_parks = json.load(f)
    except FileNotFoundError:
        return jsonify({'error': 'Mock data not found'}), 404

    filtered = []
    for park in all_parks:
        # Text query matching
        if query and query not in park.get('title', '').lower() and query not in park.get('description', '').lower():
            continue
            
        # Basic faceting matching (states, world_heritage_site)
        matches_filters = True
        for f in filters:
            field = f.get('field')
            values = f.get('values', [])
            
            if field == 'states' and not any(v in values for v in park.get('states', [])):
                matches_filters = False
                break
            if field == 'world_heritage_site' and str(park.get('world_heritage_site', False)).lower() not in [str(v).lower() for v in values]:
                matches_filters = False
                break
                
        if matches_filters:
            filtered.append(park)

    # Elastic Search UI Response Format
    # Need to wrap everything into {'raw': value} for Elastic compatibility
    results_formatted = []
    for item in filtered:
        formatted_item = {k: {'raw': v} for k, v in item.items()}
        formatted_item['id'] = {'raw': item['id']}
        results_formatted.append(formatted_item)

    # Calculate Facets for Sidebar dynamically
    states_count = {}
    whs_count = {'true': 0, 'false': 0}
    
    for item in all_parks: # Facets usually count all regardless of query or just within query. We'll do within query for accuracy
        item_states = item.get('states', [])
        for state in item_states:
            states_count[state] = states_count.get(state, 0) + 1
            
        is_whs = str(item.get('world_heritage_site', False)).lower()
        whs_count[is_whs] = whs_count.get(is_whs, 0) + 1

    facets = {
        'states': [
            {'type': 'value', 'data': [{'value': k, 'count': v} for k, v in states_count.items()]}
        ],
        'world_heritage_site': [
            {'type': 'value', 'data': [{'value': k, 'count': v} for k, v in whs_count.items()]}
        ]
    }

    # Pagination
    start = (current_page - 1) * results_per_page
    end = start + results_per_page
    paged_results = results_formatted[start:end]

    return jsonify({
        'meta': {
            'page': {
                'current': current_page,
                'total_pages': (len(filtered) + results_per_page - 1) // results_per_page,
                'total_results': len(filtered),
                'size': results_per_page
            }
        },
        'results': paged_results,
        'facets': facets
    }), 200

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
