# downloader.py
import os
import zipfile

import requests


def download_results(
    results,
    output_dir: str,
    extract: bool = False,
    keep_zip: bool = False,
):
    """
    下载解析结果

    Args:
        results (list): poll_batch_result 返回的结果列表
        output_dir (str): 输出目录
        extract (bool): 是否自动解压 zip（默认 False）
        keep_zip (bool): 解压后是否保留 zip（默认 False，仅在 extract=True 时生效）
    """
    os.makedirs(output_dir, exist_ok=True)

    for r in results:
        if r["state"] != "done":
            continue

        url = r["full_zip_url"]
        resp = requests.get(url)
        resp.raise_for_status()

        base_name = r["file_name"].rsplit(".", 1)[0]
        zip_path = os.path.join(output_dir, base_name + ".zip")

        # 1️⃣ 保存 zip
        with open(zip_path, "wb") as f:
            f.write(resp.content)

        print(f"📦 已下载: {zip_path}")

        # 2️⃣ 是否解压
        if extract:
            extract_dir = os.path.join(output_dir, base_name)
            os.makedirs(extract_dir, exist_ok=True)

            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(extract_dir)

            print(f"📂 已解压到: {extract_dir}")

            if not keep_zip:
                os.remove(zip_path)
                print(f"🗑️ 已删除压缩包: {zip_path}")
