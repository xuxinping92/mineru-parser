# uploader.py
import hashlib
import os

from .client import post, put


def make_data_id(path: str, length: int = 32) -> str:
    """
    生成安全、稳定、短的 data_id
    - ASCII
    - <= 128 chars
    - 基于完整路径，避免同名冲突
    """
    return hashlib.md5(path.encode("utf-8")).hexdigest()[:length]


def apply_upload_urls(file_paths, model_version="vlm"):
    payload = {
        "files": [
            {
                "name": os.path.basename(p),
                "data_id": make_data_id(p),
            }
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
