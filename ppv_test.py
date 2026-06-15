from playwright.sync_api import sync_playwright
import json

EMBED_URL = "https://embedindia.st/embed/mlb/2026-06-15/mia-phi"

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-blink-features=AutomationControlled"
        ]
    )

    context = browser.new_context(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080}
    )

    page = context.new_page()

    page.goto(
        EMBED_URL,
        wait_until="domcontentloaded",
        timeout=60000
    )

    page.wait_for_timeout(15000)

    print("\nTITLE:")
    print(page.title())

    print("\nBROWSER INFO:")
    info = page.evaluate("""
    () => ({
        ua: navigator.userAgent,
        platform: navigator.platform,
        webdriver: navigator.webdriver,
        ready: document.readyState
    })
    """)
    print(json.dumps(info, indent=2))

    print("\nWINDOW KEYS:")
    keys = page.evaluate("""
    () => Object.keys(window).filter(x =>
        x.toLowerCase().includes('jw') ||
        x.toLowerCase().includes('wasm')
    )
    """)
    print(keys)

    print("\nWASM TYPE:")
    print(
        page.evaluate(
            "() => typeof window.__wasm_jw_player"
        )
    )

    print("\nJW TYPE:")
    print(
        page.evaluate(
            "() => typeof window.jwplayer"
        )
    )

    print("\nDIRECT M3U8:")
    m3u8 = page.evaluate("""
    () => {
        try {

            if (!window.__wasm_jw_player)
                return null;

            const p = window.__wasm_jw_player.getPlaylist();

            if (!p || !p.length)
                return null;

            if (p[0].file)
                return p[0].file;

            if (
                p[0].sources &&
                p[0].sources.length &&
                p[0].sources[0].file
            )
                return p[0].sources[0].file;

            return null;

        } catch(e) {
            return "ERROR: " + e.toString();
        }
    }
    """)
    print(m3u8)

    print("\nBODY SAMPLE:")
    body = page.evaluate(
        "() => document.body.innerText"
    )
    print(body[:2000])

    browser.close()
