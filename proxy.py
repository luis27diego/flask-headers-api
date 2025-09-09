
from flask import Flask, request, jsonify, render_template
import requests
from flask_cors import CORS
#import subprocess

app = Flask(__name__, template_folder='templates')
CORS(app)  # Permite CORS para la API, pero no es necesario para servir HTML
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pagina1.html')
def pagina1():
    return render_template('pagina1.html')

@app.route('/pagina2.html')
def pagina2():
    return render_template('pagina2.html')

@app.route('/pagina3.html')
def pagina3():
    return render_template('pagina3.html')

@app.route('/servidores.html')
def servidores():
    return render_template('servidores.html')

@app.route('/comparar.html')
def comparar():
    return render_template('comparar.html')

@app.route('/api/headers')
def get_headers():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Falta el parámetro url'}), 400
    try:
        resp = requests.head(url, timeout=5, allow_redirects=True)
        # Solo devolvemos los encabezados más relevantes
        headers = {k: v for k, v in resp.headers.items()}
        return jsonify({'url': url, 'headers': headers})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
""" # Agregar este nuevo endpoint a tu proxy.py
@app.route('/api/curl-headers')
def get_curl_headers():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Falta el parámetro url'}), 400
    
    try:
        # MEJORADO: Agregar -L (follow redirects) y User-Agent
        cmd = [
            'curl', '-I', '-L',  # -L = seguir redirects
            '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            '--max-time', '10', 
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        
        if result.returncode != 0:
            return jsonify({
                'error': f'cURL falló: {result.stderr}',
                'raw_output': result.stdout,
                'command': ' '.join(cmd)
            }), 500
        
        # MEJORADO: Parsing más robusto
        lines = result.stdout.strip().split('\n')
        headers = {}
        
        # Buscar la última respuesta HTTP (en caso de redirects)
        start_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('HTTP/'):
                start_idx = i + 1
        
        # Parsear headers de la respuesta final
        for line in lines[start_idx:]:
            line = line.strip()
            if ':' in line and line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
        
        return jsonify({
            'url': url, 
            'headers': headers,
            'raw_output': result.stdout,
            'command': ' '.join(cmd)
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'cURL timeout'}), 500
    except Exception as e:
        return jsonify({'error': f'Error ejecutando cURL: {str(e)}'}), 500 """

if __name__ == '__main__':
    app.run(debug=True)
