import argparse
from typing import Union

import requests

from tools import get_auth_token, minimize_qparams, print_response


EP_DEV = "http://localhost:8000"
EP_PROD = "https://purple-archive-server.onrender.com"


def call_get_albums(
    token: str, endpoint: str,
    debug: bool = True,
    partialDescription: Union[str, None] = None,
    partialPlayerName: Union[str, None] = None,
    playedFrom: Union[int, None] = None,
    playedUntil: Union[int, None] = None,
    gamemodeId: Union[int, None] = None,
    partialTag: Union[str, None] = None,
    myBookmark: Union[str, None] = None,
    offset: Union[int, None] = None,
    limit: Union[int, None] = None,
    orderBy: Union[str, None] = None,
    order: Union[str, None] = None,
) -> requests.Response:
    url = f"{endpoint}/albums"
    if debug:
        print("=" * 79)
        print(f"GET {url}", flush=True)
    resp = requests.get(
        url,
        params=minimize_qparams({
            "partialDescription": partialDescription,
            "partialPlayerName": partialPlayerName,
            "playedFrom": playedFrom,
            "playedUntil": playedUntil,
            "gamemodeId": gamemodeId,
            "partialTag": partialTag,
            "myBookmark": myBookmark,
            "offset": offset,
            "limit": limit,
            "orderBy": orderBy,
            "order": order,
        }),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
    )
    if debug:
        print_response(resp)

    return resp


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--environ", choices=("dev", "prod"),
                    default="dev",
                    help="Server environment to which call API")
    ap.add_argument("--pd",
                    help="Query parameter 'partialDescription'")
    ap.add_argument("--pp",
                    help="Query parameter 'partialPlayerName'")
    ap.add_argument("--pf", type=int,
                    help="Query parameter 'playedFrom'")
    ap.add_argument("--pu", type=int,
                    help="Query parameter 'playedUntil'")
    ap.add_argument("--gi", type=int,
                    help="Query parameter 'gamemodeId'")
    ap.add_argument("--pt",
                    help="Query parameter 'partialTag'")
    ap.add_argument("--mb",
                    help="Query parameter 'myBookmark'")
    ap.add_argument("-o", "--offset", type=int,
                    help="Query parameter 'offset'")
    ap.add_argument("-l", "--limit", type=int,
                    help="Query parameter 'limit'")
    ap.add_argument("--orderBy",
                    help="Query parameter 'orderBy'")
    ap.add_argument("--order",
                    help="Query parameter 'order'")
    args = ap.parse_args()

    a_pd: Union[str, None] = args.pd
    a_pp: Union[str, None] = args.pp
    a_pf: Union[int, None] = args.pf
    a_pu: Union[int, None] = args.pu
    a_gi: Union[int, None] = args.gi
    a_pt: Union[str, None] = args.pt
    a_mb: Union[str, None] = args.mb
    a_offset: Union[str, None] = args.offset
    a_limit: Union[str, None] = args.limit
    a_orderBy: Union[str, None] = args.orderBy
    a_order: Union[str, None] = args.order

    endpoint = EP_DEV
    if args.environ == "prod":
        endpoint = EP_PROD

    # authorization
    token = get_auth_token(endpoint)

    call_get_albums(token, endpoint, a_pd, a_pp, a_pf, a_pu, a_gi, a_pt,
                    a_mb, a_offset, a_limit, a_orderBy, a_order)
