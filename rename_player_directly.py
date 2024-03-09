"""
Replace all player name with the given pattern, accross all albums.
"""
import argparse
import json
import math
from typing import List, Dict

import psycopg2

from call_get_album import call_get_album
from call_get_albums import call_get_albums
from tools import get_auth_token


DB_CONF = "./db.json"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--environ", choices=("local", "prod"),
                    default="local",
                    help="Server environment to connect to DB")
    ap.add_argument("-o", "--old", required=True,
                    help="Existing player name string to replace")
    ap.add_argument("-n", "--new", required=True,
                    help="New string to set as player name")
    args = ap.parse_args()

    a_old: str = args.old
    a_new: str = args.new

    with open(DB_CONF, "r") as f:
        conf = json.load(f)[args.environ]
    
    with psycopg2.connect(
        host=conf["host"],
        user=conf["username"],
        password=conf["password"],
        database=conf["database"],
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM page WHERE player_name = %s",
                (a_old,)
            )
            res = cur.fetchall()
            print(f"Found {len(res)} records...")
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE page SET player_name = %s WHERE player_name = %s",
                (a_new, a_old)
            )
            conn.commit()
    
    print("Successfully finished.")
