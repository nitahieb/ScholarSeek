from flask import Flask, render_template, request, jsonify
import subprocess
import json
import sys
import os
import threading
from constants import APPLICATION_OUTPUT_OPTIONS, PUBMED_SORT_OPTIONS

app = Flask(__name__, template_folder='templates', static_folder='static')

def safe_search(searchterm, mode, email, searchnumber, sortby):
    """
    Safely execute search, handling signal handler issues when not in main thread.
    Uses subprocess approach to completely isolate entrezpy from Flask's threading.
    """
    # Build command for CLI
    cmd = [sys.executable, 'main.py', searchterm, '-m', mode, '-n', str(searchnumber), '-s', sortby]
    if email:
        cmd.extend(['-e', email])
    
    # Run in same directory as webapp
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
    
    if result.returncode != 0:
        # Check if it's a network error (common in sandboxed environments)
        if "No address associated with hostname" in result.stderr:
            return {
                'error': 'Network access to PubMed is currently blocked. This is common in sandboxed environments. In production, ensure eutils.ncbi.nlm.nih.gov is accessible.',
                'details': 'The web application requires access to eutils.ncbi.nlm.nih.gov to fetch PubMed data.'
            }
        else:
            return {'error': f'Search failed: {result.stderr}'}
    
    return {'success': True, 'result': result.stdout.strip()}

@app.route('/')
def index():
    """Main web interface"""
    return render_template('index.html',
                         output_options=APPLICATION_OUTPUT_OPTIONS,
                         sort_options=PUBMED_SORT_OPTIONS)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'version': '0.1.0'})

@app.route('/api/search', methods=['POST'])
def search():
    """Main search API endpoint - uses subprocess to avoid signal handler issues"""
    try:
        data = request.get_json()

        # Validate required fields
        if not data or 'searchterm' not in data:
            return jsonify({'error': 'searchterm is required'}), 400

        # Extract parameters with defaults
        searchterm = data['searchterm']
        mode = data.get('mode', 'overview')
        email = data.get('email', '')
        searchnumber = int(data.get('searchnumber', 10))
        sortby = data.get('sortby', 'relevance')

        # Validate parameters
        if mode not in APPLICATION_OUTPUT_OPTIONS:
            return jsonify({
                'error': f'Invalid mode. Must be one of: {APPLICATION_OUTPUT_OPTIONS}'
            }), 400

        if sortby not in PUBMED_SORT_OPTIONS:
            return jsonify({'error': f'Invalid sortby. Must be one of: {PUBMED_SORT_OPTIONS}'}), 400

        if searchnumber <= 0 or searchnumber > 100:
            return jsonify({'error': 'searchnumber must be between 1 and 100'}), 400

        # Execute search using safe subprocess approach
        result = safe_search(searchterm, mode, email, searchnumber, sortby)
        
        if 'error' in result:
            return jsonify(result), 500

        return jsonify({
            'success': True,
            'mode': mode,
            'result': result['result'],
            'parameters': {
                'searchterm': searchterm,
                'mode': mode,
                'email': email,
                'searchnumber': searchnumber,
                'sortby': sortby
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Development server
    # Note: The subprocess approach eliminates the need for threading restrictions
    app.run(debug=True, host='0.0.0.0', port=5000)
