from playwright.sync_api import sync_playwright

TARGET = "https://ppv.to/live/wc/2026-06-15/esp-cpv"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox"
        ]
    )

    page = browser.new_page(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
    )

    page.add_init_script("""
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
});

Object.defineProperty(navigator, 'platform', {
    get: () => 'Win32'
});

Object.defineProperty(navigator, 'languages', {
    get: () => ['en-US','en']
});
""")

    found = set()

    def on_response(resp):
        url = resp.url

        if ".m3u8" in url:
            found.add(url)
            print("M3U8:", url)

    page.on("response", on_response)

    page.goto(TARGET, wait_until="domcontentloaded")

    page.wait_for_timeout(30000)

    print("\nTOTAL:", len(found))

    browser.close()
