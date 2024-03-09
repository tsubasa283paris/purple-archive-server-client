import json
from typing import Any, Dict

import requests


def get_auth_token(endpoint: str) -> str:
    with open("login.json", "r") as f:
        auth_params = json.load(f)
    
    resp = requests.post(
        f"{endpoint}/auth",
        data=auth_params,
    )
    return resp.json()["accessToken"]


def print_response(response: requests.Response):
    print("-" * 79)
    print(f"Status code: {response.status_code} {response.reason}")
    print("-" * 79)
    print("Response body:")
    rbody_str = response.text
    try:
        resp_json = response.json()
    except json.JSONDecodeError:
        pass
    else:
        rbody_str = json.dumps(resp_json, indent=4, ensure_ascii=False)
    print(rbody_str)


def minimize_qparams(d: Dict[str, Any]) -> Dict[str, Any]:
    d_tmp = d.copy()
    for key in d.keys():
        if d[key] is None:
            d_tmp.pop(key)
    return d_tmp
