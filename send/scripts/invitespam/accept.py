import os

import httpx
from dotenv import load_dotenv
from player_pb2 import PlayerResponse, StatusResponse, Empty

load_dotenv()
identityToken = str(os.environ.get("IDENTITYTOKEN", ""))

api_url = "https://subway.prod.sybo.net"
user_agent = "grpc-dotnet/2.63.0 (Mono Unity; CLR 4.0.30319.17020; netstandard2.0; arm64) com.kiloo.subwaysurf/3.44.2"

headers = {
    "User-Agent": user_agent,
    "grpc-accept-encoding": "identity,gzip",
    "Authorization": f"Bearer {identityToken}",
    "Content-Type": "application/grpc-web",
}


def get_invites():
    url = f"{api_url}/rpc/friends.ext.v1.PrivateService/GetInvites"
    msg = Empty()
    payload = msg.SerializeToString()
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload

    with httpx.Client(http2=True) as client:
        r = client.post(url, headers=headers, content=body)

    if "text/html" in r.headers.get("Content-Type", ""):
        print("Received HTML instead of protobuf. Something went wrong.")
        return []

    if r.status_code != 200:
        print(f"HTTP error {r.status_code}: {r.text}")
        return []

    raw = r.content
    if len(raw) < 5:
        print("gRPC-Web response too short")
        return []

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    try:
        resp = PlayerResponse()
        resp.ParseFromString(grpc_payload)
        return resp.invite
    except Exception as e:
        print("Failed to parse response:", e)
        return []


def accept_invite(action_uuid: str):
    url = f"{api_url}/rpc/friends.ext.v1.PrivateService/AcceptInvite"
    encoded_uuid = action_uuid.encode("utf-8")
    protobuf_payload = b"\x0a" + len(encoded_uuid).to_bytes(1, "big") + encoded_uuid
    prefix = b"\x00" + len(protobuf_payload).to_bytes(4, "big")
    body = prefix + protobuf_payload

    with httpx.Client(http2=True) as client:
        r = client.post(url, headers=headers, content=body)

    if r.status_code != 200 or "text/html" in r.headers.get("Content-Type", ""):
        print(f"Error accepting invite {action_uuid}: {r.status_code}")
        return

    raw = r.content
    if len(raw) < 5:
        print("gRPC-Web response too short")
        return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    try:
        resp = StatusResponse()
        resp.ParseFromString(grpc_payload)
        print(f"✅ Accepted invite: {action_uuid}")
    except Exception as e:
        print(f"❌ Failed to parse AcceptInvite response for {action_uuid}: {e}")


def main():
    invites = get_invites()
    if not invites:
        print("No invites found.")
        return

    for invite in invites:
        action_uuid = getattr(invite, "action_uuid", None)
        if action_uuid:
            print(
                f"Processing invite from: {invite.user_info.details.name} (UUID: {action_uuid})"
            )
            accept_invite(action_uuid)
        else:
            print("Invite missing action_uuid. Skipping.")


if __name__ == "__main__":
    main()
