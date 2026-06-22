@app.route('/extract', methods=['POST'])
def extract():
    data = request.json
    url = data.get('url')
    
    # PASTE THIS RIGHT HERE:
    print(f"DEBUG: Received URL: {url}") 
    
    try:
        # ... your existing code ...
        print("DEBUG: Extraction successful") 
        return jsonify({"status": "success"})
    except Exception as e:
        # PASTE THIS RIGHT HERE:
        print(f"DEBUG: Error occurred: {str(e)}") 
        return jsonify({"status": "error", "message": str(e)}), 500
