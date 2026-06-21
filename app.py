from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import re

app = Flask(__name__)
CORS(app)

@app.route('/extract', methods=['POST'])
def extract_links():
    data = request.json
    channel_url = data.get('url', '').strip()

    if not channel_url:
        return jsonify({'success': False, 'error': 'No URL provided'}), 400

    try:
        # Run the extractor script with the URL as a direct argument
        process = subprocess.Popen(
            ['python3', 'extractor.py', channel_url],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # This simulates typing '2026', then '2025' if it asks again, to bypass the prompts
        stdout, stderr = process.communicate(input='2026\n2025\n\n')
        
        # Extract all matching youtube video URLs from the script output text
        links = re.findall(r'(https://www\.youtube\.com/watch\?v=[^\s\n\r"\'\)]+)', stdout)
        
        # Clean up any weird symbols from formatting glitches
        clean_links = []
        for url in links:
            cleaned = url.replace('~', '').strip()
            if cleaned not in clean_links:
                clean_links.append(cleaned)

        if not clean_links:
            return jsonify({
                'success': False,
                'message': 'Could not catch streaming links. Check if the script runs directly via terminal.'
            })

        return jsonify({
            'success': True,
            'videos_count': len(clean_links),
            'links': clean_links
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)