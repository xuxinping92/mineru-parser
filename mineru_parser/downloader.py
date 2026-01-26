# downloader.py
import os
import shutil
import zipfile
from typing import Literal

import requests


def _resolve_conflict_dir(path: str, mode: Literal["overwrite", "rename"]) -> str:
    """
    处理目录重名问题

    Args:
        path (str): 目标目录路径
        mode (str): overwrite | rename

    Returns:
        str: 最终可用的目录路径
    """
    if not os.path.exists(path):
        return path

    if mode == "overwrite":
        shutil.rmtree(path)
        return path

    if mode == "rename":
        base = path
        idx = 1
        while True:
            new_path = f"{base} ({idx})"
            if not os.path.exists(new_path):
                return new_path
            idx += 1

    raise ValueError(f"未知的冲突处理策略: {mode}")


def download_results(
    results,
    output_dir: str,
    extract: bool = False,
    keep_zip: bool = False,
    on_conflict: Literal["overwrite", "rename"] = "rename",
):
    """
    下载解析结果

    Args:
        results (list): poll_batch_result 返回的结果列表
        output_dir (str): 输出目录
        extract (bool): 是否自动解压 zip
        keep_zip (bool): 解压后是否保留 zip（仅 extract=True 时生效）
        on_conflict (str): 解压目录重名处理策略
            - overwrite: 覆盖原目录
            - rename: 自动重命名（xxx (1), xxx (2)...）
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
            target_dir = os.path.join(output_dir, base_name)
            extract_dir = _resolve_conflict_dir(target_dir, on_conflict)
            os.makedirs(extract_dir, exist_ok=True)

            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(extract_dir)

            print(f"📂 已解压到: {extract_dir}")

            if not keep_zip:
                os.remove(zip_path)
                print(f"🗑️ 已删除压缩包: {zip_path}")
