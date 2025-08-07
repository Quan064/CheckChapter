from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()

    # Mở trang web và đăng nhập
    page = context.new_page()
    page.goto("https://example.com/login")  # Thay bằng URL đăng nhập

    # Chờ bạn đăng nhập bằng tay hoặc tự động đăng nhập
    print("Hãy đăng nhập, sau đó nhấn Enter trong terminal...")
    input()

    # Lưu trạng thái đăng nhập vào file JSON
    context.storage_state(path="state.json")

    browser.close()
