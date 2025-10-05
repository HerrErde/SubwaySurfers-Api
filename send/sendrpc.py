import base64
import os

import httpx
from dotenv import load_dotenv
from google.protobuf.any_pb2 import Any
from google.rpc import error_details_pb2, status_pb2


def statusmessage(r):
    hrbin = r.headers.get("grpc-status-details-bin")

    def fix_base64_padding(b64string):
        return b64string + "=" * (-len(b64string) % 4)

    if not hrbin:
        return "No grpc-status-details-bin header present."

    hrbin_fixed = fix_base64_padding(hrbin)
    s = status_pb2.Status()
    s.ParseFromString(base64.b64decode(hrbin_fixed))

    out = [f"Code: {s.code}", f"Message: {s.message}"]

    for detail in s.details:
        any_msg = Any()
        any_msg.CopyFrom(detail)

        if any_msg.Is(error_details_pb2.BadRequest.DESCRIPTOR):
            bad_req = error_details_pb2.BadRequest()
            any_msg.Unpack(bad_req)
            for violation in bad_req.field_violations:
                out.append(f"Field violation: {violation.description}")
        else:
            out.append(f"Unknown detail type: {any_msg.type_url}")

    return "\n".join(out)


api_url = "https://subway.prod.sybo.net"
game = "subway"

load_dotenv()
identityToken = str(os.environ.get("IDENTITYTOKEN", ""))

headers = {
    "User-Agent": "grpc-dotnet/2.63.0 (Mono Unity; CLR 4.0.30319.17020; netstandard2.0; arm64) com.kiloo.subwaysurf/3.47.0",
    "TE": "trailers",
    "grpc-accept-encoding": "identity,gzip",
    "Content-Type": "application/grpc-web",
    "genuine_app": "Genuine"
    #"genuine_app": "SignatureMismatch"
    "Authorization": f"Bearer {identityToken}",
    # "SYBO-Vendor-Id": "7683d9dfb27fd5f5a86ca36bbdd78ccf",
    # "SYBO-Bundle-Id": "com.kiloo.subwaysurf",
    # "SYBO-Device-Model": "",
    # "SYBO-Game-Version": "3.47.0_0x28820420x29",
    # "Client-Version": "3.47.0",
}
uuid_pattern = "\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b"
tag_pattern = "^[A-Z0-9]{14}$"


def grpc_status_name(code: int) -> str:
    grpc_status_codes = {
        0: "OK",
        1: "CANCELLED",
        2: "UNKNOWN",
        3: "INVALID_ARGUMENT",
        4: "DEADLINE_EXCEEDED",
        5: "NOT_FOUND",
        6: "ALREADY_EXISTS",
        7: "PERMISSION_DENIED",
        8: "RESOURCE_EXHAUSTED",
        9: "FAILED_PRECONDITION",
        10: "ABORTED",
        11: "OUT_OF_RANGE",
        12: "UNIMPLEMENTED",
        13: "INTERNAL",
        14: "UNAVAILABLE",
        15: "DATA_LOSS",
        16: "UNAUTHENTICATED",
    }
    try:
        return grpc_status_codes[int(code)]
    except (ValueError, TypeError, KeyError):
        return f"UNKNOWN_STATUS({code})"


def get_player_by_tag(playertag: str):
    from player_pb2 import PlayerResponse, PlayerRequest

    url = api_url + "/rpc/player.ext.v1.PrivateService/GetPlayerByTag"

    msg = PlayerRequest(
        player=playertag,
    )

    payload = msg.SerializeToString()

    # gRPC-Web framing
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload

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
    # print("gRPC payload (hex):", grpc_payload.hex())

    try:
        resp = PlayerResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())
        print("No valid response received.")


def get_player_by_id(playeruuid: str):
    from player_pb2 import PlayerResponse, PlayerRequest

    url = api_url + "/rpc/player.ext.v1.PrivateService/GetPlayerById"

    msg = PlayerRequest(
        player=playeruuid,
    )

    payload = msg.SerializeToString()

    # gRPC-Web framing
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload

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
    # print("gRPC payload (hex):", grpc_payload.hex())

    try:
        resp = PlayerResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())
        print("No valid response received.")


def get_player():
    from player_pb2 import Empty, PlayerResponse

    url = api_url + "/rpc/player.ext.v1.PrivateService/GetPlayer"

    msg = Empty()

    payload = msg.SerializeToString()

    # gRPC-Web framing
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    # print(grpc_status_name(r.headers.get("grpc-status")))

    raw = r.content

    if len(raw) < 5:
        print("Response too short")
        return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    try:
        resp = PlayerResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())


def create_player():
    from player_pb2 import CreatePlayerRequest, PlayerResponse

    url = api_url + "/rpc/player.ext.v1.PrivateService/CreatePlayer"

    msg = CreatePlayerRequest(
        name="CoolNiko",
        selected_board="default",
        selected_board_upgrades="default",
        selected_character="jake.default",
        selected_country="de",
        selected_background="default_background",
        selected_frame="default_frame",
        selected_portrait="jake_portrait",
        stat_total_visited_destinations=1,
        stat_total_games=1,
    )

    payload = msg.SerializeToString()

    # gRPC-Web framing
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload

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
        resp = PlayerResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())
        print("No valid response received.")


def update_player():
    from player_pb2 import UpdatePlayerRequest, PlayerResponse

    url = api_url + "/rpc/player.ext.v1.PrivateService/UpdatePlayer"

    msg = UpdatePlayerRequest(
        name="StylingeDino",
        level=1,
        highscore=1,
        metadata={
            "stat_total_visited_destinations": "1",
            "stat_total_games": "1",
            "stat_owned_characters": "1",
            "stat_owned_characters_outfits": "1",
            "stat_owned_boards": "1",
            "stat_owned_boards_upgrades": "1",
            "stat_achievements": "1",
            "stat_total_top_run_medals_bronze": "1",
            "stat_total_top_run_medals_silver": "1",
            "stat_total_top_run_medals_gold": "1",
            "stat_total_top_run_medals_diamond": "1",
            "stat_total_top_run_medals_champion": "1",
            "selected_character": "jake.default",
            "selected_portrait": "boombox_graffiti_portrait",
            # "selected_frame": "jake_portrait",
            # "selected_background": "default_background",
            # "selected_board_upgrades": "default,trail",
            # "selected_board": "default",
            # "selected_country": "de",
            # "highscore_default": "1",
            "equipped_badge_tier_1": "0",
            "equipped_badge_1": "achievement_03",
        },
    )

    payload = msg.SerializeToString()
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    print(statusmessage(r))

    raw = r.content

    if len(raw) < 5:
        print("Response too short")
        return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]
    # print("payload bytes:", resp.SerializeToString().hex())

    try:
        resp = PlayerResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())


def get_friends():
    from player_pb2 import Empty, GetFriendsResponse

    url = api_url + "/rpc/friends.ext.v1.PrivateService/GetFriends"

    msg = Empty()

    payload = msg.SerializeToString()

    # gRPC-Web framing
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    if "text/html" in r.headers.get("Content-Type", ""):
        print("Received HTML instead of protobuf. Something went wrong.")
        return

    if r.status_code != 200:
        print(f"HTTP error {r.status_code}: {r.text}")
        return

    raw = r.content
    if len(raw) < 5:
        print("gRPC-Web response too short")
        return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]
    # print("gRPC payload (hex):", grpc_payload.hex())

    grpc_status = r.headers.get("grpc-status", "0")
    if grpc_status != "0":
        print("gRPC Error:", r.headers.get("grpc-message", "Unknown error"))
        return

    try:
        resp = GetFriendsResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        message = r.headers.get("grpc-message")
        print("gRPC message:", message)
        print("gRPC payload (hex):", grpc_payload.hex())


def get_invites():
    from player_pb2 import Empty, GetInvitesResponse

    url = api_url + "/rpc/friends.ext.v1.PrivateService/GetInvites"

    msg = Empty()

    payload = msg.SerializeToString()

    # gRPC-Web framing
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    if "text/html" in r.headers.get("Content-Type", ""):
        print("Received HTML instead of protobuf. Something went wrong.")
        return

    if r.status_code != 200:
        print(f"HTTP error {r.status_code}: {r.text}")
        return

    raw = r.content
    if len(raw) < 5:
        print("gRPC-Web response too short")
        return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]
    # print("gRPC payload (hex):", grpc_payload.hex())

    try:
        resp = GetInvitesResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        message = r.headers.get("grpc-message")
        print("gRPC message:", message)
        print("gRPC payload (hex):", grpc_payload.hex())


def get_friendsandinvites():
    from player_pb2 import Empty, GetFriendAndInvitesResponse

    url = api_url + "/rpc/friends.ext.v1.PrivateService/GetFriendsAndInvites"

    msg = Empty()

    payload = msg.SerializeToString()

    # gRPC-Web framing
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    if "text/html" in r.headers.get("Content-Type", ""):
        print("Received HTML instead of protobuf. Something went wrong.")
        return

    if r.status_code != 200:
        print(f"HTTP error {r.status_code}: {r.text}")
        return

    raw = r.content
    if len(raw) < 5:
        print("gRPC-Web response too short")
        return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]
    # print("gRPC payload (hex):", grpc_payload.hex())

    grpc_status = r.headers.get("grpc-status", "0")
    if grpc_status != "0":
        print("gRPC Error:", r.headers.get("grpc-message", "Unknown error"))
        return

    try:
        resp = GetFriendAndInvitesResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        message = r.headers.get("grpc-message")
        print("gRPC message:", message)
        print("gRPC payload (hex):", grpc_payload.hex())


def send_invite(playeruuid: str):
    from player_pb2 import PlayerRequest, SendInviteResponse

    url = api_url + "/rpc/friends.ext.v1.PrivateService/SendInvite"

    msg = PlayerRequest(
        player=playeruuid,
    )

    payload = msg.SerializeToString()

    # gRPC-Web framing
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    print(statusmessage(r))

    status = r.headers.get("grpc-status")
    if status == "0":
        print("Invite sent successfully")
    elif status == "8":
        print("INVITES_THROTTLED/INVITE_QUEUE_FULL")
        return

    raw = r.content
    if len(raw) < 5:
        print("Response too short")
        return
    elif r.content:
        if "text/html;" in r.headers.get("Content-Type"):
            print("Content is html")
            return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]
    # print("gRPC payload (hex):", grpc_payload.hex())

    try:
        resp = SendInviteResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        message = r.headers.get("grpc-message")
        print("gRPC message:", message)
        print("gRPC payload (hex):", grpc_payload.hex())


def cancel_invite(playeruuid: str):
    from player_pb2 import PlayerRequest

    url = api_url + "/rpc/friends.ext.v1.PrivateService/CancelInvite"

    msg = PlayerRequest(
        player=playeruuid,
    )

    payload = msg.SerializeToString()

    # gRPC-Web framing
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    grpc_status = r.headers.get("grpc-status", "0")
    if grpc_status != "0":
        print(f"Cancel failed. gRPC status: {grpc_status}")
    else:
        print("Cancel invite successful.")


def accept_invite(playeruuid: str):
    from player_pb2 import PlayerRequest, StatusResponse

    url = api_url + "/rpc/friends.ext.v1.PrivateService/AcceptInvite"

    msg = PlayerRequest(
        player=playeruuid,
    )

    payload = msg.SerializeToString()

    # gRPC-Web framing
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers={
                **headers,
                "Content-Type": "application/grpc-web",
            },
            content=body,
        )

    if "text/html" in r.headers.get("Content-Type", ""):
        print("Received HTML instead of protobuf. Something went wrong.")
        return

    if r.status_code != 200:
        print(f"HTTP error {r.status_code}: {r.text}")
        return

    raw = r.content
    if len(raw) < 5:
        print("gRPC-Web response too short")
        return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    grpc_status = r.headers.get("grpc-status", "0")
    if grpc_status != "0":
        print("gRPC Error:", r.headers.get("grpc-message", "Unknown error"))
        return

    try:
        resp = StatusResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        message = r.headers.get("grpc-message")
        print("gRPC message:", message)
        print("gRPC payload (hex):", grpc_payload.hex())


def decline_invite(playeruuid: str):
    from player_pb2 import PlayerRequest

    url = api_url + "/rpc/friends.ext.v1.PrivateService/DeclineInvite"

    msg = PlayerRequest(
        player=playeruuid,
    )

    payload = msg.SerializeToString()

    # gRPC-Web framing
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    grpc_status = r.headers.get("grpc-status", "0")
    if grpc_status != "0":
        print(f"Decline failed. gRPC status: {grpc_status}")
    else:
        print("Declined invite successful.")


def remove_friend(playeruuid: str):
    from player_pb2 import PlayerRequest

    url = api_url + "/rpc/friends.ext.v1.PrivateService/RemoveFriend"

    msg = PlayerRequest(
        player=playeruuid,
    )

    payload = msg.SerializeToString()

    # gRPC-Web framing
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    grpc_status = r.headers.get("grpc-status", "0")
    if grpc_status != "0":
        print(f"Removing friend failed. gRPC status: {grpc_status}")
    else:
        print("Removing Friend successful.")


def get_relationship(playeruuid: str):
    from player_pb2 import PlayerRequest, StatusResponse

    url = api_url + "/rpc/friends.ext.v1.PrivateService/GetRelationship"

    msg = PlayerRequest(
        player=playeruuid,
    )

    payload = msg.SerializeToString()

    # gRPC-Web framing
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload

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
    elif r.content:
        if "text/html;" in r.headers.get("Content-Type"):
            print("Content is html")
            return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]
    # print("gRPC payload (hex):", grpc_payload.hex())

    try:
        resp = StatusResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        message = r.headers.get("grpc-message")
        print("gRPC message:", message)
        print("gRPC payload (hex):", grpc_payload.hex())


def get_wallet():
    from player_pb2 import Empty, GetWalletResponse

    url = api_url + "/rpc/wallet.ext.v1.PrivateService/GetWallet"

    msg = Empty()

    payload = msg.SerializeToString()
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload

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


def init_energy(kindId: str):
    url = api_url + "/rpc/energy.ext.v1.PrivateService/InitializeEnergy"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {identityToken}",
    }

    body = {"kindId": kindId}

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            json=body,
        )

    try:
        print(r.json())
    except Exception as e:
        print("Failed to get response:", e)


def get_energies():
    url = api_url + "/rpc/energy.ext.v1.PrivateService/GetEnergies"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {identityToken}",
    }

    body = {}

    with httpx.Client(http2=True) as client:
        r = client.post(url, headers=headers, json=body)

    try:
        print(r.json())
    except Exception as e:
        print("Failed to get response:", e)


def use_energy(kindId: str, value: int):
    url = api_url + "/rpc/energy.ext.v1.PrivateService/UseEnergy"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {identityToken}",
    }

    body = {"energyDiff": {"kindId": kindId, "value": value}}

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            json=body,
        )

    try:
        print(r.json())
    except Exception as e:
        print("Failed to get response:", e)


def add_energy(kindId: str, value: int):
    url = api_url + "/rpc/energy.ext.v1.PrivateService/AddEnergy"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {identityToken}",
    }

    body = {"energyDiff": {"kindId": kindId, "value": value}}

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            json=body,
        )

    try:
        print(r.json())
    except Exception as e:
        print("Failed to get response:", e)


def match():
    from player_pb2 import Empty, MatchPlayerResponse

    url = api_url + "/rpc/player.ext.v1.PrivateService/Match"

    msg = Empty()

    payload = msg.SerializeToString()

    # gRPC-Web framing
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    if "text/html" in r.headers.get("Content-Type", ""):
        print("Received HTML instead of protobuf. Something went wrong.")
        return

    if r.status_code != 200:
        print(f"HTTP error {r.status_code}: {r.text}")
        return

    raw = r.content
    if len(raw) < 5:
        print("gRPC-Web response too short")
        return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    grpc_status = r.headers.get("grpc-status", "0")
    if grpc_status != "0":
        print("gRPC Error:", r.headers.get("grpc-message", "Unknown error"))
        return

    try:
        resp = MatchPlayerResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        message = r.headers.get("grpc-message")
        print("gRPC message:", message)
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


# get_player_by_tag("N99635VZB9NFPD")
# get_player_by_id("fca24390-4e4e-4994-a02a-3aab323129a2")
# create_player()
# get_player()
# update_player()
# get_friends()
# get_invites()
# get_friendsandinvites()
# send_invite("0197554e-7bd0-7061-818a-32f59e3254f5")
# accept_invite("019758f7-4f56-72e4-86e3-7fc950e1d5c2")
# cancel_invite("0196ea6a-b6e1-7293-8576-260bd1bb294b")
# decline_invite("019716b9-7517-75f5-8734-f0b207ae1c2d")
# remove_friend("0196d7d9-6632-7267-a1be-df82225311a8")
# get_relationship("0196ea6a-b6e1-7293-8576-260bd1bb294b")
# get_wallet()
# get_wallet_json()
# use_consume("44c48dba-68a0-4ef6-9df4-e8aa3b1bd913")
# init_energy("0197780a-77bc-7bb8-bf9b-687fa58a53c0")
# get_energies()
# use_energy("0197780a-77bc-7bb8-bf9b-687fa58a53c0", 1)
# add_energy("0197780a-77bc-7bb8-bf9b-687fa58a53c0", 1)
