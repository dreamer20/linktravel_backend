from fastapi import FastAPI, HTTPException
import requests
import re
from fastapi.middleware.cors import CORSMiddleware
import tldextract as tld
from urllib.parse import urlparse
from bs4 import BeautifulSoup, SoupStrainer
from app.schemas import Options


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def main():
    return 'ok'

@app.post('/')
async def index(options: Options):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(options.url, headers=headers, timeout=5)
    except Exception:
        raise HTTPException(status_code=500, detail='Something went wrong')
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.reason)
    parsed_url = urlparse(options.url)
    only_links = SoupStrainer('a', href=re.compile(r'^https?://(?!{})'.format(parsed_url.hostname)))
    links = BeautifulSoup(response.text, 'html.parser', parse_only=only_links)
    url_list = set()
    for link in links:
        main = link['href']
        url = urlparse(link['href'])
        if options.only_root:
            main = f'{url.scheme}://{url.hostname}'
            if options.without_subdomain:
                tld_obj = tld.extract(url.hostname)
                main = f'{url.scheme}://{tld_obj.domain}.{tld_obj.suffix}'
        url_list.add(main)
    d = []
    for l in url_list:
        d.append({'url': l, 'links': []})
    return d
