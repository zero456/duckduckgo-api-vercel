import os
from itertools import islice

from duckduckgo_search import DDGS
from flask import Flask, request

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

    if request.method == 'POST':
        data = request.get_json()
        keywords = data.get('q', '')
        max_results = int(data.get('max_results', 10))
    else:
        keywords = request.args.get('q')
        max_results = int(request.args.get('max_results', 10))
    return keywords, max_results


@app.route('/search', methods=['GET', 'POST'])
async def search():
    keywords, max_results = run()
    results = []
    with DDGS() as ddgs:
        ddgs_gen = ddgs.text(keywords, safesearch=SAFESEARCH, timelimit='y', backend="lite")
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    return {'results': results}


@app.route('/searchAnswers', methods=['GET', 'POST'])
async def search_answers():
    keywords, max_results = run()
    results = []
    with DDGS() as ddgs:
        ddgs_gen = ddgs.answers(keywords)
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    return {'results': results}


@app.route('/searchImages', methods=['GET', 'POST'])
async def search_images():
    keywords, max_results = run()
    results = []
    with DDGS() as ddgs:
        ddgs_gen = ddgs.images(keywords, safesearch=SAFESEARCH, timelimit=None)
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    return {'results': results}


@app.route('/searchVideos', methods=['GET', 'POST'])
async def search_videos():
    keywords, max_results = run()
    results = []
    with DDGS() as ddgs:
        ddgs_gen = ddgs.videos(keywords, safesearch=SAFESEARCH, timelimit=None, resolution="high")
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    return {'results': results}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
