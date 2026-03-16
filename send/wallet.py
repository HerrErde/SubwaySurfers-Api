import httpx

from utils import *
from wallet_pb2 import *


def get_wallet():
    url = api_url + "/rpc/wallet.ext.v1.PrivateService/GetWallet"

    msg = GetWalletRequest()

    body = framing(msg)

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    raw = r.content
    if len(raw) < 5:
        print("Response too short")
        return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    try:
        resp = GetWalletResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())


def get_wallet_json():
    url = api_url + "/rpc/wallet.ext.v1.PrivateService/GetWallet"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {identityToken}",
    }

    body = {}

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            json=body,
        )

    print(r.json())


def use_consume(offerId):
    url = api_url + "/rpc/wallet.ext.v1.PrivateService/Consume"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {identityToken}",
    }

    body = {"offerId": offerId}

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            json=body,
        )

    print(r.json())


# get_wallet()
# get_wallet_json()
# use_consume("44c48dba-68a0-4ef6-9df4-e8aa3b1bd913")
