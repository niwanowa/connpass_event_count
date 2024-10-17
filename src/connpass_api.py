"""
connpass_api.py
"""

from http import HTTPStatus

import requests


def fetch_events(  # noqa: PLR0913
    hostname: str = "https://connpass.com",
    event_id: str | None = None,
    keyword: str | None = None,
    keyword_or: str | None = None,
    ym: int | None = None,
    ymd: int | None = None,
    nickname: str | None = None,
    owner_nickname: str | None = None,
    series_id: int | None = None,
    start: int | None = None,
    order: int | None = None,
    count: int | None = None,
    response_format: str | None = None,
) -> dict | None:
    """
    ConnpassのイベントサーチAPIを使用して指定されたホスト名からイベントを取得します。

    この関数は指定されたホスト名を使用してURLを構築し、GETリクエストを送信してイベントデータを取得します。
    403エラーを回避するためにUser-Agentヘッダーを設定します。

    引数:
        hostname (str): Connpass APIのホスト名。

    戻り値:
        list: リクエストが成功した場合(ステータスコード200)、イベントのリストを返します。
                参考(イベントサーチAPI) : https://connpass.com/about/api/
        None: リクエストが失敗した場合。

    例外:
        requests.exceptions.RequestException: HTTPリクエストに問題がある場合に発生します。
    """

    url: str = f"{hostname}/api/v1/event/"

    if event_id is not None:
        url = url + event_id + "/"

    params: dict[str, str | int | None] = {
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
        "format": response_format,
    }
    # Remove keys with None values
    params = {k: v for k, v in params.items() if v is not None}

    # User-Agentがpython/requestsになっていると403エラーが発生するため、curlに変更
    headers: dict[str, str] = {"User-Agent": "curl/7.81.0"}
    response: requests.Response = requests.get(url, params=params, headers=headers, timeout=10)

    if response.status_code == HTTPStatus.OK:
        events: dict[str, str] = response.json()
        return events

    error_message = f"Error: Received status code {response.status_code}\nResponse content: {response.text}"
    raise requests.exceptions.RequestException(error_message)
