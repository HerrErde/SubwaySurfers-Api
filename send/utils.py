import base64
import os

from dotenv import load_dotenv
from google.protobuf.any_pb2 import Any
from google.rpc import error_details_pb2, status_pb2

api_url = "https://subway.prod.sybo.net"
game = "subway"

load_dotenv()
identityToken = str(os.environ.get("IDENTITYTOKEN", ""))

headers = {
    "User-Agent": "grpc-dotnet/2.63.0 (Mono Unity; CLR 4.0.30319.17020; netstandard2.0; arm64) com.kiloo.subwaysurf/3.47.0",
    "TE": "trailers",
    "grpc-accept-encoding": "identity,gzip",
    "Content-Type": "application/grpc-web",
    "genuine_app": "Genuine",
    # "genuine_app": "SignatureMismatch",
    "Authorization": f"Bearer {identityToken}",
    # "SYBO-Vendor-Id": "7683d9dfb27fd5f5a86ca36bbdd78ccf",
    # "SYBO-Bundle-Id": "com.kiloo.subwaysurf",
    # "SYBO-Device-Model": "",
    # "SYBO-Game-Version": "3.47.0_0x28820420x29",
    # "Client-Version": "3.47.0",
}
uuid_pattern = "\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b"
tag_pattern = "^[A-Z0-9]{14}$"


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


def framing(msg):
    payload = msg.SerializeToString()

    # gRPC-Web framing
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload

    return body
