import argparse

import requests

from tools import get_auth_token, print_response


EP_DEV = "http://localhost:8000"
EP_PROD = "https://purple-archive-server.onrender.com"


def call_get_album_raw(
    token: str, endpoint: str, id: int
) -> requests.Response:
    url = f"{endpoint}/albums/{id}/raw"
    print("=" * 79)
    print(f"GET {url}", flush=True)
    resp = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {token}",
        }
    )
    print(resp.headers)
    with open("call_get_album_raw_result.gif", "wb") as f:
        f.write(resp.content)

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

    call_get_album_raw(token, endpoint, a_id)
