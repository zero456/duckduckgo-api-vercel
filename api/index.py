import os
from itertools import islice

from duckduckgo_search import DDGS
from flask import Flask, request, jsonify

app = Flask(__name__)

# Retrieve SECRET_KEY and SAFESEARCH from environment variables
SECRET_KEY = os.getenv('SECRET_KEY')
SAFESEARCH = os.getenv('SAFESEARCH', 'ON')  # Default to 'ON' if not set

# Print SECRET_KEY and SAFESEARCH (for debugging purposes only)
print(f"SECRET_KEY: {SECRET_KEY}")
print(f"SAFESEARCH: {SAFESEARCH}")

def check_authorization():
    # Get the Authorization header from the request
    auth_header = request.headers.get('Authorization')

    # Validate the Authorization header format and content
    if auth_header != f'Bearer {SECRET_KEY}':
        return False
    return True

def run():
    # Perform authorization check before processing the request
    if not check_authorization():
        return None, 403  # Return 403 Forbidden status code

    data = request.get_json()
    keywords = data.get('q', '')
    max_results = int(data.get('max_results', 10))
    return keywords, max_results

@app.route('/search', methods=['POST'])
async def search():
    keywords, max_results = run()
    if keywords is None:  # If authorization fails
        return jsonify({'error': 'Unauthorized access or missing required parameter: q'}), 403
    results = []
    with DDGS() as ddgs:
        ddgs_gen = ddgs.text(keywords, safesearch=SAFESEARCH, timelimit='y', backend="lite")
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    return jsonify({'results': results})

@app.route('/searchAnswers', methods=['POST'])
async def search_answers():
    keywords, max_results = run()
    if keywords is None:  # If authorization fails
        return jsonify({'error': 'Unauthorized access or missing required parameter: q'}), 403
    results = []
    with DDGS() as ddgs:
        ddgs_gen = ddgs.answers(keywords)
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    return jsonify({'results': results})

@app.route('/searchImages', methods=['POST'])
async def search_images():
    keywords, max_results = run()
    if keywords is None:  # If authorization fails
        return jsonify({'error': 'Unauthorized access or missing required parameter: q'}), 403
    results = []
    with DDGS() as ddgs:
        ddgs_gen = ddgs.images(keywords, safesearch=SAFESEARCH, timelimit=None)
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    return jsonify({'results': results})

@app.route('/searchVideos', methods=['POST'])
async def search_videos():
    keywords, max_results = run()
    if keywords is None:  # If authorization fails
        return jsonify({'error': 'Unauthorized access or missing required parameter: q'}), 403
    results = []
    with DDGS() as ddgs:
        ddgs_gen = ddgs.videos(keywords, safesearch=SAFESEARCH, timelimit=None, resolution="high")
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
