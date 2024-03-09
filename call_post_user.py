import argparse
import base64

import requests

from tools import get_auth_token, print_response


EP_DEV = "http://localhost:8000"
EP_PROD = "https://purple-archive-server.onrender.com"


def call_post_user(
    token: str, endpoint: str, id: str, display_name: str, password: str
) -> requests.Response:
    url = f"{endpoint}/users"
    print("=" * 79)
    print(f"POST {url}", flush=True)
    resp = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "id": id,
            "displayName": display_name,
            "password": password
        }
    )
    print_response(resp)

    return resp


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--environ", choices=("dev", "prod"),
                    default="dev",
                    help="Server environment to which call API")
    ap.add_argument("-i", "--id", required=True,
                    help="User id")
    ap.add_argument("-d", "--display_name", required=True,
                    help="User display name")
    ap.add_argument("-p", "--password", required=True,
                    help="User password")
    args = ap.parse_args()

    a_id: str = args.id
    a_display_name: str = args.display_name
    a_password: str = args.password

    endpoint = EP_DEV
    if args.environ == "prod":
        endpoint = EP_PROD

    # authorization
    token = get_auth_token(endpoint)

    call_post_user(token, endpoint, a_id, a_display_name, a_password)
