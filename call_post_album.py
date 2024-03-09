import argparse
import datetime
import os
import sys
from typing import List, Union

import requests

from tools import get_auth_token, print_response
from call_post_temp_album import call_post_temp_album


EP_DEV = "http://localhost:8000"
EP_PROD = "https://purple-archive-server.onrender.com"


def call_post_album(
    token: str, endpoint: str, gif_path: str, gamemode_id: int,
    tag_ids: List[int]
) -> Union[requests.Response, None]:
    # call POST /albums/temp API
    temp_album_resp = call_post_temp_album(token, gif_path, endpoint)

    if temp_album_resp.status_code != 200:
        return None

    temp_album_info = temp_album_resp.json()
    hash_match_result = temp_album_info["hashMatchResult"]
    temp_uuid: str = temp_album_info["temporaryAlbumUuid"]
    page_meta_data = temp_album_info["pageMetaData"]

    # check datetime of GIF
    played_at = datetime.datetime.strptime(
        os.path.basename(gif_path),
        "album_%Y-%m-%d_%H-%M-%S.gif"
    ).astimezone()
    
    if hash_match_result is not None:
        return None

    # call POST /albums API
    url = f"{endpoint}/albums"
    print("=" * 79)
    print(f"POST {url}", flush=True)
    resp = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "temporaryAlbumUuid": temp_uuid,
            "gamemodeId": gamemode_id,
            "tagIds": tag_ids,
            "playedAt": played_at.isoformat(),
            "pageMetaData": page_meta_data,
        }
    )
    print_response(resp)

    return resp


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-g", "--gif", required=True,
                    help="Path to the GIF file to upload")
    ap.add_argument("-e", "--environ", choices=("dev", "prod"),
                    default="dev",
                    help="Server environment to which call API")
    ap.add_argument("-gi", "--gamemode_id", type=int, required=True,
                    help="Gamemode ID")
    ap.add_argument("-t", "--tag_ids", type=int, nargs="+",
                    help="Tag IDs")
    args = ap.parse_args()

    a_gif: str = args.gif
    a_gamemode_id: int = args.gamemode_id
    a_tag_ids: Union[List[int], None] = args.tag_ids
    if a_tag_ids is None:
        a_tag_ids = []
    
    endpoint = EP_DEV
    if args.environ == "prod":
        endpoint = EP_PROD

    # authorization
    token = get_auth_token(endpoint)

    call_post_album(token, endpoint, a_gif, a_gamemode_id, a_tag_ids)
