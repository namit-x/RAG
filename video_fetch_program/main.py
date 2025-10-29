from playwright.sync_api import sync_playwright
import yt_dlp
import os
from concurrent.futures import ThreadPoolExecutor

PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLu0W_9lII9agq5TrH9XLIKQvv0iaF2X3w"

def scrape_links():
    os.makedirs("youtube", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(PLAYLIST_URL, timeout=60000)

        # Scroll to the end (YouTube lazy-loads content)
        page.evaluate("window.scrollBy(0, 20000);")
        page.wait_for_timeout(3000)

        video_links = page.eval_on_selector_all(
            "ytd-thumbnail a#thumbnail", "els => els.map(e => e.href).filter(Boolean)"
        )

        os.makedirs("youtube", exist_ok=True)
        with open("youtube/links", "w", encoding="utf-8") as f:
            f.write("\n".join(video_links))

        browser.close()
    print(f"Found {len(video_links)} videos.")
    return video_links

def download_batch(video_links):
    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "outtmpl": "audios/%(title)s.%(ext)s",
        "noplaylist": True,
        "nooverwrites": True,
        "quiet": True,
        "external_downloader": "aria2c",
        "external_downloader_args": [
            "--max-connection-per-server=12",
            "--split=12",
            "--min-split-size=1M",
            "--download-result=hide"
        ],
        "concurrent_fragment_downloads": 12,
        "n_threads": 12,
        "nocheckcertificate": True,
    }

    os.makedirs("audios", exist_ok=True)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_links)

def parallel_download(video_links, workers=10, batch_size=10):
    batches = [video_links[i:i+batch_size] for i in range(0, len(video_links), batch_size)]
    with ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(download_batch, batches)

if __name__ == "__main__":
    # Uncomment this once to scrape playlist links
    # scrape_links()

    with open("youtube/links", encoding="utf-8") as f:
        video_links = f.read().splitlines()

    print(f"Starting downloads for {len(video_links)} videos...")
    parallel_download(video_links, workers=10, batch_size=10)
    print("All downloads complete.")


# import yt_dlp

# urls = [
#     "https://www.youtube.com/watch?v=SksvlZM-5Sk&list=PLu0W_9lII9agq5TrH9XLIKQvv0iaF2X3w&index=89&pp=iAQB",
#     "https://www.youtube.com/watch?v=VELNPK0dK84&list=PLu0W_9lII9agq5TrH9XLIKQvv0iaF2X3w&index=90&pp=iAQB",
#     "https://www.youtube.com/watch?v=sgNZcK8QIyc&list=PLu0W_9lII9agq5TrH9XLIKQvv0iaF2X3w&index=130&pp=iAQB"
# ]

# ydl_opts = {
#     "format": "bestaudio[ext=m4a]/bestaudio/best",
#     "outtmpl": "audios/%(title)s.%(ext)s",
#     "noplaylist": True,
#     "nooverwrites": True,
#     "quiet": True,
#     "external_downloader": "aria2c",
#     "external_downloader_args": [
#         "--max-connection-per-server=12",
#         "--split=12",
#         "--min-split-size=1M",
#         "--download-result=hide"
#     ],
#     "concurrent_fragment_downloads": 12,
#     "n_threads": 12,
#     "nocheckcertificate": True,
# }

# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     ydl.download(urls)
