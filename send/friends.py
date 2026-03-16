import httpx

from friends_pb2 import *
from utils import *


def get_friends():
    url = api_url + "/rpc/friends.ext.v1.PrivateService/GetFriends"

    msg = GetFriendsRequest()

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
    elif r.content:
        if "text/html" in r.headers.get("Content-Type"):
            print("Content is html")
            return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

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
    url = api_url + "/rpc/friends.ext.v1.PrivateService/GetInvites"

    msg = GetInvitesRequest()

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
    elif r.content:
        if "text/html" in r.headers.get("Content-Type"):
            print("Content is html")
            return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

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
    url = api_url + "/rpc/friends.ext.v1.PrivateService/GetFriendsAndInvites"

    msg = GetFriendAndInvitesRequest()

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
    elif r.content:
        if "text/html" in r.headers.get("Content-Type"):
            print("Content is html")
            return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    try:
        resp = GetFriendAndInvitesResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        message = r.headers.get("grpc-message")
        print("gRPC message:", message)
        print("gRPC payload (hex):", grpc_payload.hex())


def send_invite(userId: str):
    url = api_url + "/rpc/friends.ext.v1.PrivateService/SendInvite"

    msg = SendInviteRequest(
        userId=userId,
    )

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
    elif r.content:
        if "text/html" in r.headers.get("Content-Type"):
            print("Content is html")
            return

    status = r.headers.get("grpc-status")
    if status == "0":
        print("Invite sent successfully")
    elif status == "8":
        print("INVITES_THROTTLED/INVITE_QUEUE_FULL")
        return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    try:
        resp = SendInviteResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        message = r.headers.get("grpc-message")
        print("gRPC message:", message)
        print("gRPC payload (hex):", grpc_payload.hex())


def cancel_invite(inviteId: str):
    url = api_url + "/rpc/friends.ext.v1.PrivateService/CancelInvite"

    msg = CancelInviteRequest(
        inviteId=inviteId,
    )

    body = framing(msg)

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    grpc_status = r.headers.get("grpc-status", "0")
    grpc_message = r.headers.get("grpc-message", "")

    if grpc_status != "0":
        print("Cancel failed:", grpc_message)
        return

    raw = r.content

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    try:
        resp = CancelInviteResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())


def decline_invite(inviteId: str):
    url = api_url + "/rpc/friends.ext.v1.PrivateService/DeclineInvite"

    msg = DeclineInviteRequest(
        inviteId=inviteId,
    )

    body = framing(msg)

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    grpc_status = r.headers.get("grpc-status", "0")
    grpc_message = r.headers.get("grpc-message", "")

    if grpc_status != "0":
        print("Cancel failed:", grpc_message)
        return

    raw = r.content

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    try:
        resp = DeclineInviteResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())


def remove_friend(playeruuid: str):
    url = api_url + "/rpc/friends.ext.v1.PrivateService/RemoveFriend"

    msg = RemoveFriendRequest(
        player=playeruuid,
    )

    body = framing(msg)

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    raw = r.content

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    try:
        resp = RemoveFriendResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())


def get_relationship(userId: str):
    url = api_url + "/rpc/friends.ext.v1.PrivateService/GetRelationship"

    msg = GetRelationshipRequest(
        userId=userId,
    )

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
    elif r.content:
        if "text/html" in r.headers.get("Content-Type"):
            print("Content is html")
            return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    try:
        resp = GetRelationshipResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        message = r.headers.get("grpc-message")
        print("gRPC message:", message)
        print("gRPC payload (hex):", grpc_payload.hex())


# get_friends()
# get_invites()
# get_friendsandinvites()
# send_invite("0197554e-7bd0-7061-818a-32f59e3254f5")
# accept_invite("019758f7-4f56-72e4-86e3-7fc950e1d5c2")
# cancel_invite("0196ea6a-b6e1-7293-8576-260bd1bb294b")
# decline_invite("019716b9-7517-75f5-8734-f0b207ae1c2d")
# remove_friend("0196d7d9-6632-7267-a1be-df82225311a8")
# get_relationship("0196ea6a-b6e1-7293-8576-260bd1bb294b")
