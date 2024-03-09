import argparse

import requests
import sys

from call_get_album import call_get_album
from tools import get_auth_token, print_response


EP_DEV = "http://localhost:8000"
EP_PROD = "https://purple-archive-server.onrender.com"


def call_put_album(
    token: str, endpoint: str, id: int
) -> requests.Response:
    album_response = call_get_album(token, endpoint, id, False)
    if album_response.status_code != 200:
        print_response(album_response)
        sys.exit(0)
    
    album = album_response.json()

    gamemode_id = album["gamemodeId"]
    # gamemode_id = 3

    tag_ids = [tag["id"] for tag in album["tags"]]
    tag_ids.append(2)
    # tag_ids.remove(2)
    # tag_ids = [3]

    page_meta_data = album["pageMetaData"]
    # page_meta_data[0]["description"] = "ヤバそうなパレオ！"
    # page_meta_data.append(
    #     {
    #         "description": "People70TP",
    #         "playerName": "PRECURE"
    #     }
    # )
    
    url = f"{endpoint}/albums/{id}"
    print("=" * 79)
    print(f"PUT {url}", flush=True)
    resp = requests.put(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "gamemodeId": gamemode_id,
            "tagIds": tag_ids,
            "pageMetaData": page_meta_data,
        }
    )
    print_response(resp)

    return resp


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--environ", choices=("dev", "prod"),
                    default="dev",
                    help="Server environment to which call API")
    ap.add_argument("-i", "--id", type=int, required=True,
                    help="Target album ID")
    args = ap.parse_args()

    a_id: int = args.id

    endpoint = EP_DEV
    if args.environ == "prod":
        endpoint = EP_PROD

    # authorization
    token = get_auth_token(endpoint)

    call_put_album(token, endpoint, a_id)
