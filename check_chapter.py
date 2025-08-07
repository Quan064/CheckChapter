from playwright.sync_api import sync_playwright
import shutil
import sqlite3
import subprocess

def check_link(url, chapter):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-web-security",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
            ]
        )
        context = browser.new_context(
            storage_state="state.json",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36"
        )

        page = context.new_page()

        page.goto(url)
        for la in ["chapter", "chuong", "tap"]:
            if (next := page.locator(f'xpath=//a[contains(@href, "{la}-{chapter}")]').count()) > 0:
                # page.screenshot(path="screenshot.png")
                browser.close()
                return next

    return 0

def check_history():
    history_path = r"C:\Users\Hello\AppData\Local\Microsoft\Edge\User Data\Default\History"
    temp_copy = "edge_history_copy.db"
    shutil.copy2(history_path, temp_copy)

    conn = sqlite3.connect(temp_copy)
    cursor = conn.cursor()

    with open(r"C:\Users\Hello\OneDrive\Code Tutorial\Python\Web_scrapping\webtoon\webtoon.txt", mode="r", encoding="utf-8") as f:
        comics = [i.split(maxsplit=2) for i in f.read().strip().split("\n")]
        for i in range(len(comics)):
            name, chapter, full_name = comics[i]
            result = True

            while result:
                chapter = str(int(chapter) + 1)
                url = name.replace("<>", chapter)

                cursor.execute("SELECT url, title FROM urls WHERE url = ?", (url,))
                result = cursor.fetchone()

            comics[i] = [name, str(int(chapter) - 1), full_name]

    with open(r"C:\Users\Hello\OneDrive\Code Tutorial\Python\Web_scrapping\webtoon\webtoon.txt", mode="w", encoding="utf-8") as f:
        f.write("\n".join(" ".join(i) for i in comics))

    conn.close()

def main():
    check_history()
    with open(r"C:\Users\Hello\OneDrive\Code Tutorial\Python\Web_scrapping\webtoon\webtoon.txt", mode="r", encoding="utf-8") as f:
        comics = [i.split(maxsplit=2) for i in f.read().strip().split("\n")]
        for name, chapter, full_name in comics:
            url = name.replace("<>", chapter)
            chapter = str(int(chapter) + 1)

            if check_link(url, chapter):
                try:
                    message = fr'''
                    $BlogButton = New-BTButton -Content "Mở trang" -Arguments "{name.replace('<>', chapter)}"
                    New-BurntToastNotification -Text "Truyện mà bạn theo dõi đã có chapter mới", "{full_name} | Chapter {chapter}" -Button $BlogButton -AppLogo "C:\Users\Hello\OneDrive\Code Tutorial\Python\Web_scrapping\webtoon\comic.ico"
                    '''

                    subprocess.run(["powershell", "-Command", message])
                except: pass

if __name__ == "__main__":
    main()