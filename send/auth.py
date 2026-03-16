import time

import httpx
from player_pb2 import *

api_url = "https://subway.prod.sybo.net"

headers = {
    "User-Agent": "grpc-dotnet/2.63.0 (Mono Unity; CLR 4.0.30319.17020; netstandard2.0; arm64) com.kiloo.subwaysurf/3.44.2",
    "grpc-accept-encoding": "identity,gzip",
}


def framing(msg):
    payload = msg.SerializeToString()

    # gRPC-Web framing
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload

    return body


def deframing(raw):

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    return grpc_payload


def create_player(authtoken):
    url = api_url + "/rpc/player.ext.v1.PrivateService/CreatePlayer"

    msg = CreatePlayerRequest(
        name="CoolNikos",
        level=1,
        highscore=1,
    )

    body = framing(msg)

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers={
                **headers,
                "Content-Type": "application/grpc-web",
                "Authorization": f"Bearer {authtoken}",
            },
            content=body,
        )

    raw = r.content

    if len(raw) < 5:
        print("Response too short")
        return

    grpc_payload = deframing(raw)

    try:
        resp = CreatePlayerResponse()
        resp.ParseFromString(grpc_payload)
        print("Parsed response:", resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())
        print("No valid response received.")


def get_player(authtoken):
    url = api_url + "/rpc/player.ext.v1.PrivateService/GetPlayer"

    msg = GetPlayerRequest()

    body = framing(msg)

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers={
                **headers,
                "Content-Type": "application/grpc-web",
                "Authorization": f"Bearer {authtoken}",
            },
            content=body,
        )

    raw = r.content

    if len(raw) < 5:
        print("Response too short")
        return

    grpc_payload = deframing(raw)

    try:
        resp = GetPlayerResponse()
        resp.ParseFromString(grpc_payload)
        print("Parsed response:", resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())


def auth_register():
    url = api_url + "/v2.0/auth/register"

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers={"Content-Type": "application/json"},
        )

        response_json = r.json()
        id_token = response_json.get("idToken")
        print(id_token)
        return id_token


authtoken = auth_register()
time.sleep(1)
create_player(authtoken)
# get_player(authtoken)
