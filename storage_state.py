from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    def hard_remove_ads(page):
        page.evaluate("""
            document.querySelectorAll('div, iframe').forEach(el => {
                const rect = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                if (
                    (rect.width >= window.innerWidth * 0.8 &&
                    rect.height >= window.innerHeight * 0.8) &&
                    (style.position === "fixed" || style.position === "absolute")
                ) {
                    el.remove();
                }
            });
        """)

        page.evaluate("""
            document.body.onclick = null;
            document.body.onmousedown = null;
            document.body.onmouseup = null;
            document.documentElement.onclick = null;
            document.documentElement.onmousedown = null;
            document.documentElement.onmouseup = null;
        """)

    browser = p.chromium.launch(
        headless=False,
        args=["--disable-blink-features=AutomationControlled"]
    )
    context = browser.new_context(
        # storage_state="state.json",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36"
    )
    page = context.new_page()

    # page.on("popup", lambda popup: popup.close())
    # page.add_init_script("window.open = () => null;")

    page.goto("https://manhuatop.org/home")

    # for _ in range(5):
    #     hard_remove_ads(page)
    #     time.sleep(1)

    # signin_btn = page.locator('//div[@class="c-modal_item"]/a[1]')
    # signin_btn.click()

    # page.locator('//*[@id="loginform"]/p[1]/label/input').fill("Quan064")
    # page.locator('//*[@id="loginform"]/p[2]/label/input').fill("MinhQuan12345")
    # page.keyboard.press("Enter")
    # time.sleep(2)
    # page.reload()
    # time.sleep(2)

    context.storage_state(path="state.json")
    time.sleep(5)
    context.close()
    browser.close()