"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
DEPRECATED
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Replace all player name with the given pattern, accross all albums.
"""
import argparse
import math
from typing import List, Dict

from call_get_album import call_get_album
from call_get_albums import call_get_albums
from tools import get_auth_token


EP_DEV = "http://localhost:8000"
EP_PROD = "https://purple-archive-server.onrender.com"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--environ", choices=("dev", "prod"),
                    default="dev",
                    help="Server environment to which call API")
    ap.add_argument("-o", "--old", required=True,
                    help="Existing player name string to replace")
    ap.add_argument("-n", "--new", required=True,
                    help="New string to set as player name")
    args = ap.parse_args()

    a_old: str = args.old
    a_new: str = args.new

    endpoint = EP_DEV
    if args.environ == "prod":
        endpoint = EP_PROD

    # authorization
    token = get_auth_token(endpoint)

    # first, check number of album pages
    r = call_get_albums(token, endpoint,
                        debug=False, partialPlayerName=a_old)
    count = r.json()["albumsCountAll"]

    match_count = 0

    # pagination by 100
    for i in range(math.ceil(count / 100)):
        print(f"Page {i + 1}", flush=True)
        r = call_get_albums(token, endpoint,
                            debug=False, partialPlayerName=a_old,
                            limit=100, offset=i * 100)
        albums: List[Dict[str, any]] = r.json()["albums"]

        for album in albums:
            r = call_get_album(token, endpoint, album["id"],
                               increment_pv=False, debug=False)
            pages: List[Dict[str, any]] = r.json()["pageMetaData"]
            for page in pages:
                if page["playerName"] == a_old:
                    match_count += 1
                    break # do not care multi turn case
    
    print(match_count)
