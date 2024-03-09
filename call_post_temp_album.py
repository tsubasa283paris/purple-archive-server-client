import argparse
import base64

import requests

from tools import get_auth_token, print_response


EP_DEV = "http://localhost:8000"
EP_PROD = "https://purple-archive-server.onrender.com"


def call_post_temp_album(
    token: str, gif_path: str, endpoint: str
) -> requests.Response:
    # open gif file
    with open(gif_path, "rb") as f:
        raw_data = f.read()

    url = f"{endpoint}/albums/temp"
    print("=" * 79)
    print(f"POST {url}", flush=True)
    resp = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "data": base64.b64encode(raw_data).decode()
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
    args = ap.parse_args()

    a_gif: str = args.gif

    endpoint = EP_DEV
    if args.environ == "prod":
        endpoint = EP_PROD

    # authorization
    token = get_auth_token(endpoint)

    call_post_temp_album(token, a_gif, endpoint)
