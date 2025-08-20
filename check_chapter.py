from playwright.sync_api import sync_playwright
import shutil
import sqlite3
import subprocess

def check_link(name, chapter, full_name):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            storage_state="state.json",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36"
        )

        page = context.new_page()
        url = name.replace("<>", chapter)
        page.goto(url)

        for i in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1):
            newchapter = str(int(float(chapter) + i) if (float(chapter) + i).is_integer() else float(chapter) + i)

            for la in ["chapter", "chuong", "tap"]:
                # page.screenshot(path="screenshot.png")
                if page.locator(f'xpath=//a[contains(@href, "{la}-{newchapter}")]').count() > 0:

                    message = fr'''
                    $BlogButton = New-BTButton -Content "Mở trang" -Arguments "{name.replace("<>", newchapter)}"
                    New-BurntToastNotification -Text "Truyện mà bạn theo dõi đã có chapter mới", "{full_name} | Chapter {newchapter}" -Button $BlogButton -AppLogo "C:\Users\Hello\OneDrive\Code Tutorial\Python\Web_scrapping\webtoon\comic.ico"
                    '''

                    subprocess.run(["powershell", "-Command", message])
                    break
            else:
                continue
            break

        browser.close()

def check_history():
    history_path = r"C:\Users\Hello\AppData\Local\Microsoft\Edge\User Data\Default\History"
    temp_copy = "edge_history_copy.db"
    shutil.copy2(history_path, temp_copy)

    conn = sqlite3.connect(temp_copy)
    cursor = conn.cursor()

    with open(r"C:\Users\Hello\OneDrive\Code Tutorial\Python\Web_scrapping\webtoon\webtoon.txt", mode="r", encoding="utf-8") as f:
        comics = [i.split(maxsplit=2) for i in f.read().strip().split("\n")]
        new_comics = []
        for i in range(len(comics)):
            name, chapter, full_name = comics[i]
            result = True

            while result:
                for i in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1):
                    newchapter = str(int(float(chapter) + i) if (float(chapter) + i).is_integer() else float(chapter) + i)
                    url = name.replace("<>", newchapter)

                    cursor.execute("SELECT url, title FROM urls WHERE url = ?", (url,))
                    result = cursor.fetchone()
                    if result: break
                chapter = newchapter

            new_comics.append([name, str(int(float(chapter) - 1) if (float(chapter) - 1).is_integer() else float(chapter) - 1), full_name])

    with open(r"C:\Users\Hello\OneDrive\Code Tutorial\Python\Web_scrapping\webtoon\webtoon.txt", mode="w", encoding="utf-8") as f:
        f.write("\n".join(" ".join(i) for i in new_comics))

    conn.close()

def main():
    check_history()
    with open(r"C:\Users\Hello\OneDrive\Code Tutorial\Python\Web_scrapping\webtoon\webtoon.txt", mode="r", encoding="utf-8") as f:
        comics = [i.split(maxsplit=2) for i in f.read().strip().split("\n")]
        for name, chapter, full_name in comics:
            while True:
                try:
                    check_link(name, chapter, full_name)
                except:
                    continue
                break

if __name__ == "__main__":
    main()