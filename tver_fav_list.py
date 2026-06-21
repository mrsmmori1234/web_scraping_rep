import os
import re
from playwright.sync_api import sync_playwright

# test.py と同じプロファイルディレクトリを使用
user_data_dir = os.path.expanduser("~/web_scraping/chrome_profile")

def fetch_tver_favorites():
    with sync_playwright() as p:
        # test.py の設定を参考に、ログイン済みのプロファイルで起動
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            channel="chrome",
            headless=False,  # ブラウザを表示する
            args=[
                "--profile-directory=Default",
                "--disable-gpu",
                "--disable-software-rasterizer"
            ]
        )
        page = context.new_page()

        print("🚀 TVer お気に入りページにアクセス中...")
        try:
            # 遷移中のエラーを避けるため、まずは移動を指示
            page.goto("https://tver.jp/mypage/fav", timeout=60000, wait_until="commit")

            # リダイレクト（地域制限エラーページへの遷移など）が落ち着くまで待機
            page.wait_for_load_state("load")
            page.wait_for_timeout(3000)

            # 現在のURLを確認
            current_url = page.url
            if "error" in current_url or "mypage/fav" not in current_url:
                print(f"⚠️ ページがリダイレクトされました: {current_url}")
                print("日本国外からのアクセスとして遮断されている可能性があります。")

            # 画面が表示されない場合のために、現在の画面を保存
            debug_img = "tver_debug.png"
            page.screenshot(path=debug_img)
            print(f"📸 画面の状態を {debug_img} に保存しました（表示されない場合はこれを確認してください）")

            content = page.content()

            # エピソードIDのパターン (/episodes/epXXXXXXXX) を抽出
            episode_ids = re.findall(r'/episodes/(ep[a-z0-9]+)', content)
            # 重複を除去してURLを生成
            urls = [f"https://tver.jp/episodes/{eid}" for eid in dict.fromkeys(episode_ids)]

            if urls:
                print(f"\n✅ {len(urls)} 件の動画が見つかりました:")
                for url in urls:
                    print(url)
            else:
                print("⚠️ お気に入りの動画が見つかりませんでした。")
                print("シンガポールからの接続の場合、VPNがオフだとコンテンツが読み込まれないことがあります。")

        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")
            print("💡 日本国内のIPアドレス（VPN等）がWSL側で有効になっているか確認してください。")
        finally:
            input("\n🏁 ブラウザを確認してください。Enterキーを押すとブラウザを閉じて終了します...")
            context.close()

if __name__ == "__main__":
    fetch_tver_favorites()