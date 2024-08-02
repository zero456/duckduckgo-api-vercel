import os

from duckduckgo_search import DDGS
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

# Retrieve SECRET_KEY and SAFESEARCH from environment variables
SECRET_KEY = os.getenv('SECRET_KEY')
SAFESEARCH = os.getenv('SAFESEARCH', 'moderate')  # Default to 'ON' if not set

def check_authorization(request: Request):
    # Get the Authorization header from the request
    auth_header = request.headers.get('Authorization')

    # Validate the Authorization header format and content
    if auth_header != f'Bearer {SECRET_KEY}':
        return False
    return True

async def run(request: Request):
    # Perform authorization check before processing the request
    if not check_authorization(request):
        raise HTTPException(status_code=403, detail="Unauthorized access")

    data = await request.json()
    keywords = data.get('q', '')
    max_results = int(data.get('max_results', 10))
    model = data.get('model', 'claude-3-haiku')  # Default model if not specified
    return keywords, max_results, model

@app.post('/search')
async def search(request: Request):
    keywords, max_results, _ = await run(request)
    if keywords is None:  # If authorization fails
        raise HTTPException(status_code=403, detail="Missing required parameter: q")
    
    results = []
    with DDGS() as ddgs:
        ddgs_gen = ddgs.text(keywords, safesearch=SAFESEARCH, timelimit='y', max_results=max_results)
        results.append(ddgs_gen)

    return JSONResponse(content={'results': results})

@app.post('/searchNews')
async def search_news(request: Request):
    keywords, max_results, _ = await run(request)
    if keywords is None:  # If authorization fails
        raise HTTPException(status_code=403, detail="Missing required parameter: q")
    
    results = []
    with DDGS() as ddgs:
        ddgs_gen = ddgs.news(keywords, safesearch=SAFESEARCH, timelimit='y', max_results=max_results)
        results.append(ddgs_gen)

    return JSONResponse(content={'results': results})

@app.post('/searchAnswers')
async def search_answers(request: Request):
    keywords, max_results, _ = await run(request)
    if keywords is None:  # If authorization fails
        raise HTTPException(status_code=403, detail="Missing required parameter: q")

    results = []
    with DDGS() as ddgs:
        ddgs_gen = ddgs.answers(keywords)
        results.append(ddgs_gen)

    return JSONResponse(content={'results': results})

@app.post('/searchImages')
async def search_images(request: Request):
    keywords, max_results, _ = await run(request)
    if keywords is None:  # If authorization fails
        raise HTTPException(status_code=403, detail="Missing required parameter: q")
    
    results = []
    with DDGS() as ddgs:
        ddgs_gen = ddgs.images(keywords, safesearch=SAFESEARCH, timelimit='y', max_results=max_results)
        results.append(ddgs_gen)

    return JSONResponse(content={'results': results})

@app.post('/searchVideos')
async def search_videos(request: Request):
    keywords, max_results, _ = await run(request)
    if keywords is None:  # If authorization fails
        raise HTTPException(status_code=403, detail="Missing required parameter: q")
    
    results = []
    with DDGS() as ddgs:
        ddgs_gen = ddgs.videos(keywords, safesearch=SAFESEARCH, timelimit='y', max_results=max_results)
        results.append(ddgs_gen)

    return JSONResponse(content={'results': results})

@app.post('/aichat')
async def aichat(request: Request):
    keywords, _, model = await run(request)
    if keywords is None:  # If authorization fails
        raise HTTPException(status_code=403, detail="Missing required parameter: q")

    results = []
    with DDGS() as ddgs:
        ddgs_gen = ddgs.chat(keywords, model=model)
        results.append(ddgs_gen)

    return JSONResponse(content={'results': results})
