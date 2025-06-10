import pytest
import httpx

from send.player_pb2 import PlayerRequest, GetPlayerByTagResponse
from send.sendrpc import get_player_by_tag


def build_grpc_web_response(pb_msg, grpc_status="0"):
    payload = pb_msg.SerializeToString()
    framed = b"\x00" + len(payload).to_bytes(4, "big") + payload
    return framed, {"grpc-status": grpc_status}


def test_get_player_by_tag_success(monkeypatch, capsys):
    # Prepare mocked protobuf response
    mock_resp = GetPlayerByTagResponse()
    # Assuming userdata is a message inside GetPlayerByTagResponse
    mock_resp.userdata.name = "CoolNikos"
    mock_resp.userdata.tag = "LWVQZJZH65TN2R"
    mock_resp.userdata.uuid = "019711b2-26b5-79aa-a2b0-477f599bdcc3"

    raw_body, headers = build_grpc_web_response(mock_resp)

    # Mock httpx.Client.post to return a prepared response
    def mock_post(self, url, headers=None, content=None):
        return httpx.Response(
            status_code=200,
            headers=headers,
            content=raw_body,
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(httpx.Client, "post", mock_post)

    # Call the function that makes the grpc-web request and prints output
    get_player_by_tag("LWVQZJZH65TN2R")

    captured = capsys.readouterr()
    # Check printed output contains protobuf fields
    assert "userdata {" in captured.out
    assert 'name: "CoolNikos"' in captured.out
    assert 'tag: "LWVQZJZH65TN2R"' in captured.out
    assert 'uuid: "019711b2-26b5-79aa-a2b0-477f599bdcc3"' in captured.out
