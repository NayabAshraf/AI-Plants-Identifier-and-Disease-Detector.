import os
import json
import time
import requests
from duckduckgo_search import DDGS
from PIL import Image
from io import BytesIO
from functools import lru_cache

CACHE_FILE = "plant_cache.json"
IMAGE_DIR = "downloaded_images"
MAX_IMAGES = 3

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

os.makedirs(IMAGE_DIR, exist_ok=True)


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)


CACHE = load_cache()


@lru_cache(maxsize=128)
def search_duckduckgo(query):
    with DDGS() as ddgs:
        return list(ddgs.images(query, max_results=12))


def download_image(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=8)
        img = Image.open(BytesIO(r.content)).convert("RGB")
        return img
    except Exception:
        return None


def get_plant_images(plant_name):
    plant_key = plant_name.lower().strip()

    if plant_key in CACHE:
        return CACHE[plant_key]

    results = search_duckduckgo(f"{plant_name} plant")
    saved_paths = []

    for item in results:
        if len(saved_paths) >= MAX_IMAGES:
            break

        img_url = item.get("image")
        if not img_url:
            continue

        img = download_image(img_url)
        if img is None:
            continue

        filename = f"{plant_key.replace(' ', '_')}_{len(saved_paths)+1}.jpg"
        filepath = os.path.join(IMAGE_DIR, filename)

        img.save(filepath)
        saved_paths.append(filepath)
        time.sleep(1)

    CACHE[plant_key] = saved_paths
    save_cache(CACHE)

    return saved_paths
