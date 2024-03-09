import argparse

import requests

from tools import get_auth_token, print_response


EP_DEV = "http://localhost:8000"
EP_PROD = "https://purple-archive-server.onrender.com"


def call_get_album(
    token: str, endpoint: str, id: int, increment_pv: bool,
    debug: bool = True,
) -> requests.Response:
    url = f"{endpoint}/albums/{id}"
    if debug:
        print("=" * 79)
        print(f"GET {url}", flush=True)
    resp = requests.get(
        url,
        params={
            "incrementPv": "true"
        } if increment_pv else {},
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
    ap.add_argument("-i", "--id", type=int, required=True,
                    help="Target album ID")
    ap.add_argument("--disable_pv", action="store_true",
                    help="Disable incrementing PV count")
    args = ap.parse_args()

    a_id: int = args.id
    a_disable_pv: bool = args.disable_pv

    endpoint = EP_DEV
    if args.environ == "prod":
        endpoint = EP_PROD

    # authorization
    token = get_auth_token(endpoint)

    call_get_album(token, endpoint, a_id, not a_disable_pv)
