from flask import Flask, render_template, request, jsonify
from python.buscador_logica import buscar_informacion

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/buscador')
def buscador():
    return render_template('Buscador.html')

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
    app.run(debug=True, host='0.0.0.0', port=8080)
