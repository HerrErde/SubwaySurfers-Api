import os

import httpx
from dotenv import load_dotenv

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


def framing(msg):
    payload = msg.SerializeToString()

    # gRPC-Web framing
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload

    return body


def get_invites():
    from player_pb2 import Empty, GetInvitesResponse

    url = f"{api_url}/rpc/friends.ext.v1.PrivateService/GetInvites"
    msg = Empty()

    body = framing(msg)

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
        resp = GetInvitesResponse()
        resp.ParseFromString(grpc_payload)
        return resp.received_invites
    except Exception as e:
        print("Failed to parse response:", e)
        return []


def accept_invite(action_uuid: str):
    from player_pb2 import PlayerRequest, Empty

    url = f"{api_url}/rpc/friends.ext.v1.PrivateService/AcceptInvite"

    msg = PlayerRequest(
        player=action_uuid,
    )

    body = framing(msg)

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
        resp = Empty()
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
                f"Processing invite from: {invite.user_info.user_data.name} (UUID: {action_uuid})"
            )
            accept_invite(action_uuid)
        else:
            print("Invite missing action_uuid. Skipping.")


if __name__ == "__main__":
    main()
