"""
connpass_api.py
"""

import requests
from typing import Any, Optional


def fetch_events(
    hostname: str = "https://connpass.com",
    event_id: Optional[str] = None,
    keyword: Optional[str] = None,
    keyword_or: Optional[str] = None,
    ym: Optional[int] = None,
    ymd: Optional[int] = None,
    nickname: Optional[str] = None,
    owner_nickname: Optional[str] = None,
    series_id: Optional[int] = None,
    start: Optional[int] = None,
    order: Optional[int] = None,
    count: Optional[int] = None,
    format: Optional[str] = None,
) -> dict | None:
    """
    ConnpassのイベントサーチAPIを使用して指定されたホスト名からイベントを取得します。

    この関数は指定されたホスト名を使用してURLを構築し、GETリクエストを送信してイベントデータを取得します。
    403エラーを回避するためにUser-Agentヘッダーを設定します。

    引数:
        hostname (str): Connpass APIのホスト名。

    戻り値:
        list: リクエストが成功した場合（ステータスコード200）、イベントのリストを返します。
                参考(イベントサーチAPI) : https://connpass.com/about/api/
        None: リクエストが失敗した場合。

    例外:
        requests.exceptions.RequestException: HTTPリクエストに問題がある場合に発生します。
    """

    url: str = f"{hostname}/api/v1/event/"

    if event_id is not None:
        url = url + event_id + "/"

    params: dict[str, Optional[str | int]] = {
        "event_id": event_id,
        "keyword": keyword,
        "keyword_or": keyword_or,
        "ym": ym,
        "ymd": ymd,
        "nickname": nickname,
        "owner_nickname": owner_nickname,
        "series_id": series_id,
        "start": start,
        "order": order,
        "count": count,
        "format": format,
    }
    # Remove keys with None values
    params = {k: v for k, v in params.items() if v is not None}

    # User-Agentがpython/requestsになっていると403エラーが発生するため、curlに変更
    headers: dict[str, str] = {"User-Agent": "curl/7.81.0"}
    response: requests.Response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        events: dict[str, str] = response.json()
        return events
    else:
        raise requests.exceptions.RequestException(
            f"Error: Received status code {response.status_code}\nResponse content: {response.text}"
        )
