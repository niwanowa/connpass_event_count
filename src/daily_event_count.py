"""
daily_event_count.py
GHAでcronを回す際の指標を取得するため、connpassで1日に何件イベントが作成されているかを取得する
csvとして出力したらそれっぽく見れたりするかもしれない
"""

import csv
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

import connpass_api


def output_csv(event_count: int, hour: str) -> None:
    """
    イベント数と時間をCSVファイルに追記します。

    この関数は、出力ディレクトリが存在しない場合に作成し、
    提供されたイベント数と時間を"outputs/event_count"ディレクトリ内の
    "event_count.csv"という名前のCSVファイルに追記します。CSVファイルが
    存在しない場合、ファイルを作成し、ヘッダー行を書き込みます。

    引数:
        hour (str): イベント数が記録された時間。
        event_count (int): 記録されたイベント数。

    例外:
        OSError: 出力ディレクトリの作成やCSVファイルへの書き込みに
                 問題がある場合に発生します。
    """
    # CSVファイルに追記または更新
    csv_file_path: Path = Path("outputs/event_count") / "event_count.csv"
    file_exists: bool = csv_file_path.is_file()

    # 読み込み用のリスト
    rows: list = []

    if file_exists:
        with csv_file_path.open(mode="r", newline="") as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader, None)
            if header:
                rows.append(header)
            for row in csv_reader:
                if row[0] == hour:
                    row[1] = str(max(int(row[1]), event_count))
                rows.append(row)

    if not any(row[0] == hour for row in rows):
        rows.append([hour, event_count])

    with csv_file_path.open(mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        if not file_exists:
            csv_writer.writerow(["datetime", "event_count"])
        csv_writer.writerows(rows)


if __name__ == "__main__":
    load_dotenv()

    # 環境変数から値を取得
    CONNPASS_HOST: str | None = os.getenv("URL")

    if CONNPASS_HOST is None:
        error_message = "URL is not set"
        raise ValueError(error_message)

    # connpass api呼び出し
    res: dict | None = connpass_api.fetch_events(CONNPASS_HOST, order=1, count=100)

    if res is None:
        error_message = "Failed to fetch events from connpass API"
        raise ValueError(error_message)

    # json形式のレスポンスからevents.eventsを取得
    events: list[dict[str, str]] = res["events"]

    summary: dict = {}

    for event in events:
        updated: datetime = datetime.strptime(event["updated_at"], "%Y-%m-%dT%H:%M:%S%z")
        # dictに日付と時間ごとのイベント数を格納
        date_hour = updated.strftime("%Y-%m-%d %H:00")
        if date_hour in summary:
            summary[date_hour] += 1
        else:
            summary[date_hour] = 1

    # 日付と時間ごとのイベント数を出力
    for date_hour, count in summary.items():
        print(f"{date_hour} : {count}件")
        output_csv(count, date_hour)
