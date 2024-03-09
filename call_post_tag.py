import argparse
import base64

import requests

from tools import get_auth_token, print_response


EP_DEV = "http://localhost:8000"
EP_PROD = "https://purple-archive-server.onrender.com"


def call_post_tag(
    token: str, endpoint: str, name: str
) -> requests.Response:
    url = f"{endpoint}/tags"
    print("=" * 79)
    print(f"POST {url}", flush=True)
    resp = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "name": name
        }
    )
    print_response(resp)

    return resp


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--environ", choices=("dev", "prod"),
                    default="dev",
                    help="Server environment to which call API")
    ap.add_argument("-n", "--name", required=True,
                    help="Tag name")
    args = ap.parse_args()

    a_name: str = args.name

    endpoint = EP_DEV
    if args.environ == "prod":
        endpoint = EP_PROD

    # authorization
    token = get_auth_token(endpoint)

    call_post_tag(token, endpoint, a_name)
