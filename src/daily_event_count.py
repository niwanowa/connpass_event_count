"""
daily_event_count.py
GHAでcronを回す際の指標を取得するため、connpassで1日に何件イベントが作成されているかを取得する
csvとして出力したらそれっぽく見れたりするかもしれない？
"""

import os
from dotenv import load_dotenv

import connpass_api

if __name__ == "__main__":
    load_dotenv()

    # 環境変数から値を取得
    CONNPASS_API_KEY = os.getenv("URL")

    # connpass api呼び出し
    res = connpass_api.fetch_events(os.getenv("URL"), order=1, count=50)

    if res is None:
        raise ValueError("Failed to fetch events from connpass API")
    
    # json形式のレスポンスからevents.eventsを取得
    events = res["events"]

    for event in events:
        print(event["title"], event["updated_at"])