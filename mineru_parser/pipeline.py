# pipeline.py
from .auth import ensure_env
from .downloader import download_results
from .poller import poll_batch
from .scanner import InputType, collect_parsable_files
from .uploader import apply_upload_urls, upload_files
from .utils import chunk_list


def parse_folder(inputs: InputType, output_dir: str, batch_size: int = 50):
    ensure_env("MINERU_TOKEN")
    files = collect_parsable_files(inputs)

    for batch in chunk_list(files, batch_size):
        upload_info = apply_upload_urls(batch)
        upload_files(batch, upload_info["file_urls"])
        results = poll_batch(upload_info["batch_id"])
        download_results(results, output_dir, extract=True, keep_zip=False)
