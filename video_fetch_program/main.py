from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as page:
        browser = page.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://youtube.com/playlist?list=PLu0W_9lII9agq5TrH9XLIKQvv0iaF2X3w&si=9h2wc9iEXe8Up3u3')
        page.wait_for_load_state("networkidle")

        for _ in range(3):
            page.mouse.wheel(0, 5000)
            page.wait_for_timeout(1000)

        imgs = page.locator("ytd-playlist-video-renderer a#thumbnail")

        print(f"Found {imgs.count()} Thumbnails")

if __name__ == "__main__":
    run()