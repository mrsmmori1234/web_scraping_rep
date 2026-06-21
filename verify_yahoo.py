import os
from playwright.sync_api import sync_playwright

user_data_dir = os.path.expanduser("~/web_scraping/chrome_profile")

def verify_yahoo_login():
    with sync_playwright() as p:
        print("🚀 保存されたプロファイルを使用して Yahoo Japan を開いています...")
        # headless=False でブラウザを表示
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            channel="chrome",
            headless=False,
            args=[
                "--profile-directory=Default",
                "--disable-gpu",
                "--disable-software-rasterizer"
            ]
        )
        page = context.new_page()
        
        # Yahoo Japan に移動
        try:
            # タイムアウトを60秒に延長し、解析完了時点で処理を続行
            page.goto("https://www.yahoo.co.jp/", timeout=60000, wait_until="domcontentloaded")
        except Exception as e:
            print(f"⚠️ 読み込み中にタイムアウトしましたが、続行します: {e}")
        
        print("✅ ブラウザが起動しました。")
        print("💡 ログイン状態を確認してください。ログインが必要な場合はこの画面で操作できます。")
        input("\n🏁 確認が終わったら、Enter キーを押すとブラウザを閉じて終了します...")
        context.close()

if __name__ == "__main__":
    verify_yahoo_login()