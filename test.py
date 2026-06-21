# test.py の修正箇所
import os
from playwright.sync_api import sync_playwright

# Windows側ではなく、WSL（Linux）内のフォルダを指すように変更
user_data_dir = os.path.expanduser("~/web_scraping/chrome_profile")

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        channel="chrome",
        headless=True,  # WSLなのでTrue（ヘッドレス）
        args=["--profile-directory=Default"]
    ) 
    page = context.new_page()
    page.goto("https://www.google.com")
    print("ページタイトル:", page.title())
    
    context.close()