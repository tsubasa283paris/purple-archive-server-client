import argparse
import glob
import os

from tqdm import tqdm

from tools import get_auth_token
from call_post_album import call_post_album


EP_DEV = "http://localhost:8000"
EP_PROD = "https://purple-archive-server.onrender.com"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dir", required=True,
                    help="Path to the directory where GIF files exist")
    ap.add_argument("-e", "--environ", choices=("dev", "prod"),
                    default="dev",
                    help="Server environment to which call API")
    ap.add_argument("-gi", "--gamemode_id", type=int, required=True,
                    help="Default gamemode ID to attach to albums")
    args = ap.parse_args()

    a_dir: str = args.dir
    a_gamemode_id: int = args.gamemode_id
    
    endpoint = EP_DEV
    if args.environ == "prod":
        endpoint = EP_PROD

    for gif_file in tqdm(glob.glob(os.path.join(a_dir, "*.gif"))):
        # authorization
        token = get_auth_token(endpoint)

        call_post_album(token, endpoint, gif_file, a_gamemode_id, [])
