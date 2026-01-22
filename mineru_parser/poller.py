# poller.py
import time

import requests

from .config import API_BASE, HEADERS


def poll_batch(batch_id: str, interval: int = 5):
    """
    轮询解析任务状态，直到全部完成
    """
    url = f"{API_BASE}/extract-results/batch/{batch_id}"

    while True:
        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()

        if data["code"] != 0:
            raise RuntimeError(f"查询失败: {data}")

        results = data["data"]["extract_result"]

        all_done = True
        for r in results:
            state = r["state"]
            fname = r["file_name"]

            if state in ("pending", "running", "waiting-file", "converting"):
                all_done = False
                print(f"⏳ {fname} 状态: {state}")
            elif state == "failed":
                print(f"❌ {fname} 失败: {r.get('err_msg')}")
            elif state == "done":
                print(f"✅ {fname} 解析完成")

        if all_done:
            return results

        time.sleep(interval)
