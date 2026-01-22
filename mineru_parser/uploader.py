# uploader.py
import os

from .client import post, put


def apply_upload_urls(file_paths, model_version="vlm"):
    payload = {
        "files": [
            {"name": os.path.basename(p), "data_id": os.path.basename(p)}
            for p in file_paths
        ],
        "model_version": model_version,
    }

    res = post("/file-urls/batch", payload)
    if res["code"] != 0:
        raise RuntimeError(res)

    return res["data"]


def upload_files(file_paths, upload_urls):
    for path, url in zip(file_paths, upload_urls):
        with open(path, "rb") as f:
            put(url, f)
