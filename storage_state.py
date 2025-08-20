from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        args=["--disable-blink-features=AutomationControlled"]
    )
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36"
    )

    # Mở trang web và đăng nhập
    page = context.new_page()
    page.goto("https://manhuatop.org/home")  # Thay bằng URL đăng nhập

    # Chờ bạn đăng nhập bằng tay hoặc tự động đăng nhập
    print("Hãy đăng nhập, sau đó nhấn Enter trong terminal...")
    input()

    # Lưu trạng thái đăng nhập vào file JSON
    context.storage_state(path="state.json")
    input()
    context.close()
    browser.close()
