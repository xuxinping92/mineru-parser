# downloader.py
import os

import requests


def download_results(results, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for r in results:
        if r["state"] != "done":
            continue

        resp = requests.get(r["full_zip_url"])
        resp.raise_for_status()

        name = r["file_name"].rsplit(".", 1)[0] + ".zip"
        with open(os.path.join(output_dir, name), "wb") as f:
            f.write(resp.content)
