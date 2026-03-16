import httpx
from google.protobuf.timestamp_pb2 import Timestamp

from tournament_pb2 import *
from utils import *


def get_tournamentinfo(tournament_id: str, type: str, locale: str):
    url = api_url + "/rpc/tournament.ext.v2.PrivateService/GetTournamentInfo"

    msg = GetTournamentInfoRequest(
        tournament=TournamentInput(
            id=tournament_id,
        ),
        pool=PoolInput(
            partitionKey=type,
            countryCodePartitionKey=locale,
        ),
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

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    try:
        resp = GetTournamentInfoResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())


def jointournament(tournament_id: str, type: str, locale: str):
    url = api_url + "/rpc/tournament.ext.v2.PrivateService/JoinTournament"

    msg = JoinTournamentRequest(
        tournament=TournamentInput(
            id=tournament_id,
        ),
        pool=PoolInput(
            partitionKey=type,
            countryCodePartitionKey=locale,
        ),
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
        resp = JoinTournamentResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        message = r.headers.get("grpc-message")
        print("gRPC message:", message)
        print("gRPC payload (hex):", grpc_payload.hex())


def submitscore(
    tournament_id: str,
    score: int,
    gameplaysec: int,
    gameplaynsec: int,
    scoredsec: int,
    scorednsec: int,
    type: str,
    locale: str,
    # metadata: dict,
):

    url = api_url + "/rpc/tournament.ext.v2.PrivateService/SubmitScore"

    msg = SubmitScoreRequest(
        tournament=TournamentInput(id=tournament_id),
        score=ScoreInput(
            value=score,
            gameplayDuration=Duration(seconds=gameplaysec, nanos=gameplaynsec),
            scoredAt=Timestamp(seconds=scoredsec, nanos=scorednsec),
            # metadata=metadata,
        ),
        pool=PoolInput(partitionKey=type, countryCodePartitionKey=locale),
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
        resp = SubmitScoreResponse()
        resp.ParseFromString(grpc_payload)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())


def get_scores(tournament_id: str):
    url = api_url + "/rpc/tournament.ext.v2.PrivateService/GetScores"

    msg = GetScoresRequest(
        tournament=TournamentInput(
            id=tournament_id,
        ),
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

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    try:
        resp = GetScoresResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())


def get_results(tournament_id):
    url = api_url + "/rpc/tournament.ext.v2.PrivateService/GetResults"

    msg = GetResultsRequest(
        tournament=TournamentInput(
            id=tournament_id,
        ),
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

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    try:
        resp = GetResultsResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
        print("gRPC payload (hex):", grpc_payload.hex())
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())


def claimrewards(tournament_id):
    url = api_url + "/rpc/tournament.ext.v2.PrivateService/ClaimRewards"

    msg = ClaimRewardsRequest(
        tournament=TournamentInput(
            id=tournament_id,
        ),
    )

    body = framing(msg)

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    raw = r.content
    print(raw)
    if len(raw) < 5:
        print("Response too short")
        return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    try:
        resp = ClaimRewardsResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())


get_tournamentinfo("top_run_v1", "default", "de")
# jointournament("surfers_league_s114_v0", "default", "zz")
"""
submitscore(
    tournament_id="surfers_league_s115_v0",
    score=1772195592,
    gameplaysec=69,
    gameplaynsec=69,
    scoredsec=69,
    scorednsec=69,
    type="default",
    locale="zz",
)
"""
# get_scores("surfers_league_s114_v0")
# get_results("surfers_league_s114_v0")
# claimrewards("surfers_league_s114_v0")
