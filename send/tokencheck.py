import base64
import datetime
import json
import sys


def base64url_decode(data):
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def parse_jws(token):
    try:
        header_b64, payload_b64, _ = token.split(".")
        header = json.loads(base64url_decode(header_b64).decode())
        payload = json.loads(base64url_decode(payload_b64).decode())
        return header, payload
    except Exception as e:
        print(f"Error parsing token: {e}")
        return None, None


def classify_token(payload):
    print(payload)
    if payload is None:
        return "Invalid token"
    if "key" in payload:
        print(payload.get("sub"))
        print(payload.get("key"))
        return "refresh token"
    elif "sub" in payload:
        print(payload.get("sub"))

        print(payload.get("exp"))
        print(
            datetime.datetime.fromtimestamp(payload.get("exp")).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
        print(payload.get("iat"))
        print(
            datetime.datetime.fromtimestamp(payload.get("iat")).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
        return "identtoken"
    else:
        return "unknown token"


def main():
    if len(sys.argv) != 2:
        print("Usage: python check_token.py <jws_token>")
        sys.exit(1)

    token = sys.argv[1]
    header, payload = parse_jws(token)
    kind = classify_token(payload)
    print(f"Token type: {kind}")


if __name__ == "__main__":
    main()
