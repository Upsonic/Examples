import os
import requests

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SERPER_URL = "https://google.serper.dev/search"

def search_company(query: str):
    if not SERPER_API_KEY:
        raise ValueError("Missing SERPER_API_KEY. Export it in your environment.")
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query}
    resp = requests.post(SERPER_URL, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()
