import argparse
from typing import Union

import requests

from tools import get_auth_token, minimize_qparams, print_response


EP_DEV = "http://localhost:8000"
EP_PROD = "https://purple-archive-server.onrender.com"


def call_get_users(
    token: str, endpoint: str,
    offset: Union[int, None] = None,
    limit: Union[int, None] = None
) -> requests.Response:
    url = f"{endpoint}/users"
    print("=" * 79)
    print(f"GET {url}", flush=True)
    resp = requests.get(
        url,
        params=minimize_qparams({
            "offset": offset,
            "limit": limit
        }),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
    )
    print_response(resp)

    return resp


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--environ", choices=("dev", "prod"),
                    default="dev",
                    help="Server environment to which call API")
    ap.add_argument("-o", "--offset", type=int,
                    help="Value of the query parameter 'offset'")
    ap.add_argument("-l", "--limit", type=int,
                    help="Value of the query parameter 'limit'")
    args = ap.parse_args()

    a_offset: Union[int, None] = args.offset
    a_limit: Union[int, None] = args.limit

    endpoint = EP_DEV
    if args.environ == "prod":
        endpoint = EP_PROD

    # authorization
    token = get_auth_token(endpoint)

    call_get_users(token, endpoint, a_offset, a_limit)
