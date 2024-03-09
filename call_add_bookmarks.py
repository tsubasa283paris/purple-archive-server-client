import argparse
from typing import List, Union

import requests

from tools import get_auth_token, print_response


EP_DEV = "http://localhost:8000"
EP_PROD = "https://purple-archive-server.onrender.com"


def call_add_bookmarks(
    token: str, endpoint: str, album_ids: List[int]
) -> requests.Response:
    url = f"{endpoint}/users/me/bookmarks"
    print("=" * 79)
    print(f"POST {url}", flush=True)
    resp = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "albumIds": album_ids,
        }
    )
    print_response(resp)

    return resp


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--environ", choices=("dev", "prod"),
                    default="dev",
                    help="Server environment to which call API")
    ap.add_argument("-i", "--ids", type=int, nargs="+",
                    help="Target album IDs")
    args = ap.parse_args()

    a_ids: Union[List[int], None] = args.ids
    if a_ids is None:
        a_ids = []

    endpoint = EP_DEV
    if args.environ == "prod":
        endpoint = EP_PROD

    # authorization
    token = get_auth_token(endpoint)

    call_add_bookmarks(token, endpoint, a_ids)
