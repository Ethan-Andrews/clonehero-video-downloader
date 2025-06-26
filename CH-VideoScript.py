# filepath: [VideoDownload.py](http://_vscodecontentref_/0)
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from yt_dlp import YoutubeDL
from googlesearch import search

HOME = Path(r"C:\Users\Andre\OneDrive\Documents\Clone Hero\Songs")
YDL_OPTS = {
    "nooverwrites": False,
    "noplaylist": True,
    # format could be parameterized per‐quality
}

def find_song_dirs(base: Path):
    return [p for p in base.iterdir() if p.is_dir()]

def get_youtube_url(song_name: str) -> str | None:
    query = f"Youtube {song_name} (Official Music Video)"
    return next(search(query, tld="com", lang="en", num=1, stop=1), None)

def download_to_folder(folder: Path, url: str):
    opts = YDL_OPTS.copy()
    opts["outtmpl"] = str(folder / "video.mp4")
    with YoutubeDL(opts) as ydl:
        ydl.download([url])

def process_folder(folder: Path) -> tuple[str,bool]:
    url = get_youtube_url(folder.name)
    if not url:
        return folder.name, False
    try:
        download_to_folder(folder, url)
        return folder.name, True
    except Exception:
        return folder.name, False

def main():
    folders = find_song_dirs(HOME)
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(process_folder, f): f.name for f in folders}
        for fut in as_completed(futures):
            name, ok = fut.result()
            status = "✅" if ok else "❌"
            print(f"{status} {name}")

if __name__ == "__main__":
    main()