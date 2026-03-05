import json
import os
import random
import re
from datetime import UTC, datetime
from pathlib import Path

import httpx

api_url = "https://subway.prod.sybo.net"
user_agent = "grpc-dotnet/2.63.0 (Mono Unity; CLR 4.0.30319.17020; netstandard2.0; arm64) com.kiloo.subwaysurf/3.46.9"


def auth_register():
    url = api_url + "/v2.0/auth/register"
    with httpx.Client(http2=True) as client:
        r = client.post(url, headers={"Content-Type": "application/json"})
        r.raise_for_status()
        return r.json()


def abtesting(
    payer: bool = True,
    level: int = 39,
    age: int = 69,
    language: str = "en",
    platform: str = "android",
    coppa: bool = True,
    version: str = "3.47.0",
    identityToken: str = None,
):
    url = api_url + "/v1.0/abtesting/match"

    data = {
        "metrics": {
            "payer": str(payer),
            "level": str(level),
            "age": str(age),
            "language": language,
            "platform": platform,
            "coppa": str(coppa),
            "gameVersion": version,
        }
    }

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers={
                "Authorization": f"Bearer {identityToken}",
            },
            json=data,
        )

        r.raise_for_status()

        print(r.status_code)
        if r.status_code == 200:
            return r.json()


def main(version: str, amount: int):
    created = []
    remaining = amount

    for _ in range(amount):
        try:
            auth = auth_register()
            authtoken = auth.get("idToken")
            refresh_token = auth.get("refreshToken")

            experiment = abtesting(
                payer=random.choice([True, False]),
                level=random.choice([0, 20]),
                age=random.choice(range(100)),
                language="de",
                platform=random.choice(["android", "ios"]),
                coppa=random.choice([True, False]),
                version=version.replace("-", "."),
                identityToken=authtoken,
            )
            if experiment:
                created.append(
                    {
                        "experiment": experiment,
                        "idToken": authtoken,
                        "refreshToken": refresh_token,
                    }
                )
        except Exception as e:
            print(f"Error: {e}")
            continue

        remaining -= 1
        print(f"Remaining: {remaining}")

    with open(os.path.join("accounts.json"), "w", encoding="utf-8") as f:
        json.dump(created, f, indent=2)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python script.py <version> <amount>")
        exit(1)
    version = str(sys.argv[1])
    amount = int(sys.argv[2])
    try:
        main(version, amount)
    except KeyboardInterrupt:
        print("\nExiting on user request.")
        exit(0)
