# client.py
import requests

from .config import API_BASE, HEADERS


def post(path: str, json: dict):
    r = requests.post(f"{API_BASE}{path}", headers=HEADERS, json=json)
    r.raise_for_status()
    return r.json()


def get(path: str):
    r = requests.get(f"{API_BASE}{path}", headers=HEADERS)
    r.raise_for_status()
    return r.json()


def put(url: str, data):
    r = requests.put(url, data=data)
    r.raise_for_status()
