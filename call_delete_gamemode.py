import argparse
import base64

import requests

from tools import get_auth_token, print_response


EP_DEV = "http://localhost:8000"
EP_PROD = "https://purple-archive-server.onrender.com"


def call_delete_gamemode(
    token: str, endpoint: str, id: int
) -> requests.Response:
    url = f"{endpoint}/gamemodes/{id}"
    print("=" * 79)
    print(f"DELETE {url}", flush=True)
    resp = requests.delete(
        url,
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
    ap.add_argument("-i", "--id", type=int, required=True,
                    help="Gamemode ID")
    args = ap.parse_args()

    a_id: int = args.id

    endpoint = EP_DEV
    if args.environ == "prod":
        endpoint = EP_PROD

    # authorization
    token = get_auth_token(endpoint)

    call_delete_gamemode(token, endpoint, a_id)
