import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SERPER_URL = "https://google.serper.dev/search"


def search_mail_query(query: str) -> dict:
    if not SERPER_API_KEY:
        raise ValueError("Missing SERPER_API_KEY in .env")
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    resp = requests.post(SERPER_URL, headers=headers, json={"q": query})
    resp.raise_for_status()
    return resp.json()


