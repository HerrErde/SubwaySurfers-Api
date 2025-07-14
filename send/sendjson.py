import base64
import json
import os
import re
import urllib.parse
from typing import Optional, Tuple, Union

import httpx
from dotenv import load_dotenv

api_url = "https://subway.prod.sybo.net"
manifest_api_url = "https://manifest.tower.sybo.net"
gamedata_api_url = "https://gamedata.tower.sybo.net"
game = "subway"
helpshift_api_url = "https://api.helpshift.com"


load_dotenv()
identityToken = os.getenv("IDENTITYTOKEN", "")

headers = {
    "User-Agent": "Subway Surf/3.47.0 (Android OS 13 / API-33 (TKQ1.230127.002/TP2R)) Android)",
    "TE": "trailers",
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip",
    # "SYBO-Vendor-Id": "7683d9dfb27fd5f5a86ca36bbdd78ccf",
    # "SYBO-Bundle-Id": "com.kiloo.subwaysurf",
    # "SYBO-Device-Model": "",
    # "SYBO-Game-Version": "3.47.0_0x28820420x29",
    # "Client-Version": "3.47.0",
}


def auth_register():
    url = api_url + "/v2.0/auth/register"

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers={"Content-Type": "application/json"},
        )

        response_json = r.json()

        print(response_json)


# Needs Authtoken
def auth_refresh(refreshToken: str):
    url = api_url + "/v2.0/auth/refresh"

    data = {"refreshToken": refreshToken, "fbAccessToken": None}

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers={
                **headers,
                "Authorization": f"Bearer {identityToken}",
            },
            json=data,
        )

        response_json = r.json()
        idToken = response_json.get("idToken", "idToken not found")
        idTokenTtl = response_json.get("idTokenTtl", "idToken not found")
        refreshToken = response_json.get("refreshToken", "idToken not found")
        user = response_json.get("user", "user not found")
        user_id = user.get("id", "id not found")
        links = user.get("links", "links not found")

        print(response_json)


# Needs Authtoken
def get_mail(
    payer: bool = False,
    level: int = 0,
    age: int = 65,
    language: str = "en",
    platform: str = "android",
    coppa: bool = True,
    version: str = "3.47.0",
):
    url = api_url + "/v2.0/mail"

    data = {
        "language": language,
        "metrics": {
            "payer": str(payer),
            "level": str(level),
            "language": language,
            "age": str(age),
            "platform": platform,
            "coppa": str(coppa),
            "gameVersion": version,
        },
    }
    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers={
                **headers,
                "Authorization": f"Bearer {identityToken}",
            },
            json=data,
        )

        print(r.json())


# Needs Authtoken
def get_tournament():
    url = api_url + "/v3.0/tournament/group"

    with httpx.Client(http2=True) as client:
        r = client.get(
            url,
            headers={
                **headers,
                "Authorization": f"Bearer {identityToken}",
            },
        )

        print(r.json())


# Needs Authtoken
def send_tournament(tournamentId: str, gamedataHash: str):
    url = api_url + "/v3.0/tournament/group"

    data = {
        "tournamentId": tournamentId,
        "gamedataHash": gamedataHash,
    }

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers={
                **headers,
                "Authorization": f"Bearer {identityToken}",
            },
            json=data,
        )

        print(r.json())


def get_manifest(
    manifestSecret: str,
    version: str,
    game: str = "subway",
    type: str = "android",
    experiment: Optional[str] = None,
):
    if type not in ["android", "ios"]:
        raise ValueError("Invalid type. Must be 'android' or 'ios'.")
    if not manifestSecret:
        raise ValueError("manifestSecret is required.")
    if not version:
        raise ValueError("version is required.")

    experiment_path = f"/{experiment}" if experiment else ""
    url = f"{manifest_api_url}/v1.0/{game}/{version}/{type}/{manifestSecret}{experiment_path}/manifest.json"

    with httpx.Client(http2=True) as client:
        r = client.get(url, headers=headers)
        r.raise_for_status()
        print(r.json())


def get_gamedata(
    game: str = "subway",
    gamedataSecret: Optional[str] = None,
    file: Optional[str] = None,
):
    if not game:
        raise ValueError("game is required.")
    if not gamedataSecret:
        raise ValueError("manifestSecret is required.")
    if not file:
        raise ValueError("file is required.")

    filename = file.replace(".json", "")
    url = gamedata_api_url + f"/v1.0/{game}/{gamedataSecret}/{filename}.json"

    with httpx.Client(http2=True) as client:
        r = client.get(
            url,
            headers=headers,
        )

        r.raise_for_status()

        print(r.json())


def get_media(promotion: str, image: str):
    url = f"https://media.sybo.net/{game}/cross_promotion/{promotion}/Image/{image}"

    file_name = url.replace("https://", "").replace("/", "_")

    with httpx.Client(http2=True) as client:
        r = client.get(
            url,
            headers=headers,
        )

        if r.status_code == 200:
            with open(file_name, "wb") as f:
                f.write(r.content)
            print(f"Image {file_name} saved successfully.")
        else:
            print(f"Failed to fetch image: {r.status_code}")


# TODO
# Needs Authtoken
def events(
    gameId: int = 3447644,
    orgId: int = 176648,
    analyticsUserId: Union[None, Tuple[Optional[str], re.Pattern]] = (
        None,
        re.compile(r"^[a-f0-9]{32}$"),
    ),
    analyticsSessionId: Union[None, Tuple[Optional[str], re.Pattern]] = (
        None,
        re.compile(r"^\d{12}$"),
    ),
    sessionId: Union[None, Tuple[Optional[str], re.Pattern]] = (
        None,
        re.compile(r"^[a-f0-9]{32}$"),
    ),
    platform: str = "ANDROID",
    adsSdkVersion: str = "4.13.1",
    limitAdTracking: bool = True,
    coppaFlagged: bool = True,
    connectionType: str = "wifi",
    projectId: Union[None, Tuple[Optional[str], re.Pattern]] = (
        None,
        re.compile(r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"),
    ),
    gdprEnabled: bool = True,
    optOutRecorded: bool = True,
    optOutEnabled: bool = True,
    storeId: str = "com.kiloo.subwaysurf",
    installHour: Union[None, Tuple[Optional[str], re.Pattern]] = (
        None,
        re.compile(r"^\d{10}$"),
    ),
):
    if (
        installHour is not None
        and not installHour[1] is not None
        and not installHour[1].match(installHour[0])
    ):
        raise ValueError("Invalid installHour format")

    if (
        analyticsUserId is not None
        and not analyticsUserId[1] is not None
        and not analyticsUserId[1].match(analyticsUserId[0])
    ):
        raise ValueError("Invalid analyticsUserId format")

    if (
        analyticsSessionId is not None
        and not analyticsSessionId[1] is not None
        and not analyticsSessionId[1].match(analyticsSessionId[0])
    ):
        raise ValueError("Invalid analyticsSessionId format")

    if (
        sessionId is not None
        and not sessionId[1] is not None
        and not sessionId[1].match(sessionId[0])
    ):
        raise ValueError("Invalid sessionId format")

    if (
        projectId is not None
        and not projectId[1] is not None
        and not projectId[1].match(projectId[0])
    ):
        raise ValueError("Invalid projectId format")

    if platform not in ["android", "ios"]:
        raise ValueError("Invalid sessionId format")

    if connectionType not in ["wifi", "data"]:
        raise ValueError("Invalid connectionType")

    url = api_url + "/v1/events"

    data = {
        "common": {
            "gameId": str(gameId),
            "organizationId": str(orgId),
            "analyticsUserId": analyticsUserId,
            "analyticsSessionId": analyticsSessionId,
            "sessionId": sessionId,
            "platform": platform.upper(),
            "adsSdkVersion": adsSdkVersion,
            "gamerToken": identityToken,
            "limitAdTracking": limitAdTracking,
            "coppaFlagged": coppaFlagged,
            "projectId": projectId,
            "gdprEnabled": gdprEnabled,
            "optOutRecorded": optOutRecorded,
            "optOutEnabled": optOutEnabled,
            "deviceMake": "",
            "deviceModel": "",
            "connectionType": connectionType,
            "country": "DE",
            "storeId": storeId,
            "privacy": {
                "permissions": {
                    "ads": False,
                    "external": False,
                    "gameExp": False,
                    "dataLeavesTerritory": False,
                },
                "method": "unity_consent",
            },
            "installHour": installHour,
        },
        "type": "ads.analytics.appStart.v2",
        "msg": {"nAppStartDay": 4, "nAppStartUser": 4, "ts": 1744491616923},
    }

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers={
                **headers,
                "Authorization": f"Bearer {identityToken}",
            },
            json=data,
        )
        r.raise_for_status()
        print("Response Status Code:", r.status_code)


def get_servertime():
    url = "https://server-time.sybo-aps.workers.dev/"

    with httpx.Client(http2=True) as client:
        r = client.get(
            url,
            headers=headers,
        )
        r.raise_for_status()

        print(r.json())


def get_cflocation():
    url = "https://cloudflare-location-check.sybo-aps.workers.dev/"

    with httpx.Client(http2=True) as client:
        r = client.get(
            url,
            headers=headers,
        )
        r.raise_for_status()

        print(r.json())


def get_networkcheck():
    url = "https://network-check.sybo.net/"

    with httpx.Client(http2=True, verify=False, follow_redirects=True) as client:
        r = client.get(url, headers=headers)
        print(r.url)
        print(r.status_code)


# Needs Authtoken
def abtesting(
    payer: bool = True,
    level: int = 39,
    age: int = 69,
    language: str = "en",
    platform: str = "android",
    coppa: bool = True,
    version: str = "3.47.0",
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
                **headers,
                "Authorization": f"Bearer {identityToken}",
            },
            json=data,
        )

        r.raise_for_status()

        print(r.status_code)


# Needs Authtoken
def crosspromo(
    test: bool = False,
    language: str = "en",
    payer: bool = True,
    level: int = 39,
    age: int = 69,
    platform: str = "android",
    coppa: bool = True,
    version: str = "3.44.0",
):
    url = api_url + "/v2.0/crosspromo/match"

    data = {
        "test": test,
        "language": language,
        "metrics": {
            "payer": str(payer),
            "level": str(level),
            "age": str(age),
            "language": language,
            "platform": platform,
            "coppa": str(coppa),
            "gameVersion": version,
        },
        "attribution": None,
    }

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers={
                **headers,
                "Authorization": f"Bearer {identityToken}",
            },
            json=data,
        )
        r.raise_for_status()

        print(r.json())


def assets(game: str, bundleId: str):
    headers = {
        "User-Agent": "UnityPlayer/2022.3.24f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
        "X-Unity-Version": "2022.3.24f1",
    }
    url = f"http://assets.tower.sybo.net/v1.0/{game}/{bundleId}"

    try:
        with httpx.Client(http2=True) as client:
            r = client.get(url, headers=headers)

            response_content = r.content

            file_name = bundleId.split("/")[-1]

            print(f"Saving asset as: {file_name}")
            with open(file_name, "wb") as f:
                f.write(response_content)
            print(f"Asset {file_name} saved successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Needs Authtoken
# TODO
def send_metrics():
    url = api_url + "/v1.0/metrics"

    data = {"metrics": [{"id": 0, "value": 14848}, {"id": 1, "value": 1}]}

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            json=data,
        )

        print(r.status_code)
        print(r.content)


# Needs Authtoken
def gdpr_delete():
    url = api_url + "/v1.0/gdpr/delete"

    data = {"gaid": "00000000-0000-0000-0000-000000000000"}

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers={
                **headers,
                "Authorization": f"Bearer {identityToken}",
            },
            json=data,
        )

        print(r.json())


# Needs Authtoken
def gdpr_status():
    url = api_url + "/v1.0/gdpr/status"

    with httpx.Client(http2=True) as client:
        r = client.get(
            url,
            headers={
                **headers,
                "Authorization": f"Bearer {identityToken}",
            },
        )

        print(r.json())


# Needs Authtoken
def get_profile(uuid: str):
    url = api_url + f"/v2.0/profile/{uuid}"

    with httpx.Client(http2=True) as client:
        response = client.get(
            url,
            headers={
                **headers,
                "Authorization": f"Bearer {identityToken}",
            },
        )

        try:
            response.raise_for_status()
            response_json = response.json()
            print(response_json)
        except httpx.HTTPStatusError as e:
            print(f"Request failed: {e}")
        except ValueError:
            print("Invalid JSON response")


# Needs Authtoken
def send_redeem(redeem_code: str, platform: int):
    url = api_url + f"/v1.0/promocode/redeem"

    data = {"code": redeem_code, "platform": platform}

    with httpx.Client(http2=True) as client:
        response = client.post(
            url,
            headers={
                **headers,
                "Authorization": f"Bearer {identityToken}",
            },
            json=data,
        )

        if response.status_code == 409:
            print("Promocode already redeemed")
            return

        try:
            response.raise_for_status()
            response_json = response.json()
            print(response_json)
        except httpx.HTTPStatusError as e:
            print(f"Request failed: {e}")
        except ValueError:
            print("Invalid JSON response")


def send_websdk():
    basic_auth = "c3lib19wbGF0Zm9ybV8yMDIzMDMwMjE0MjMxNDc2OS05YzcxN2E0NTg0YWNhNWQ6"

    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Accept": "application/vnd+hsapi-v2+json",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; Build/TKQ1.230127.002)",
        "Host": "api.helpshift.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }

    url = "https://api.helpshift.com/events/v1/sybo/websdk/"

    events = [
        {"ts": 1748019454970, "t": "a"},
        {"ts": 1748019962371, "t": "a"},
        {"ts": 1748019981454, "t": "a"},
        {"ts": 1748020009976, "t": "a"},
        {"ts": 1748020082834, "t": "a"},
        {"ts": 1748020099356, "t": "a"},
        {"ts": 1748021108077, "t": "a"},
        {"ts": 1748186617064, "t": "a"},
    ]

    payload = {
        "ln": "en-US",
        "os": "13",
        "e": json.dumps(events, separators=(",", ":")),
        "dln": "en",
        "dm": "",
        "platform-id": "sybo_platform_20230302142314769-9c717a4584aca5d",
        "uid": "hsft_anon_1748008727159-548a9fdcc4414fe",
        "s": "androidx",
        "av": "3.46.9",
        "v": "10.3.0",
        "id": "c408a4e2-8fa1-4047-90be-1cbe45ed7f33",
        "did": "c408a4e2-8fa1-4047-90be-1cbe45ed7f33",
        "timestamp": "1748186617096",
    }

    body = urllib.parse.urlencode(payload)

    with httpx.Client(http2=True) as client:
        r = client.post(url, headers=headers, content=body)

        r.raise_for_status()
        print(r.json())


def send_fbinstall():
    headers = {
        "X-Android-Package": "com.kiloo.subwaysurf",
        "x-firebase-client": "H4sIAAAAAAAA_6tWykhNLCpJSk0sKVayio7VUSpLLSrOzM9TslIyUqoFAFyivEQfAAAA",
        "X-Android-Cert": "92CB567B2CB421FA8CEE1B81B4ECCFA768BAB24A",
        "x-goog-api-key": "AIzaSyAIrgHn1QjOvdtW6AjpMUytqrLOCJN9al8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; Build/TKQ1.230127.002)",
    }

    url = "https://firebaseinstallations.googleapis.com/v1/projects/api-project-1055792361676/installations"

    rand_bytes = os.urandom(17)
    fid = base64.urlsafe_b64encode(rand_bytes).decode().rstrip("=")

    payload = {
        "fid": fid,
        "appId": "1:1055792361676:android:94e1faead5ee4c7281d269",
        "authVersion": "FIS_v2",
        "sdkVersion": "a:18.0.0",
    }

    with httpx.Client(http2=True) as client:
        r = client.post(url, headers=headers, json=payload)
        r.raise_for_status()
        print(r.json())


def get_challenge(challenge: str = "daily_challenge_en"):
    url = api_url + f"/v2.0/challenge/{challenge}/group"

    with httpx.Client(http2=True) as client:
        r = client.get(
            url,
            headers={
                **headers,
                "Authorization": f"Bearer {identityToken}",
            },
        )
        print(r.status_code)
        print(r.json())


def get_challenge(
    matchmakingStartValue: int,
    gamedataHash: str,
    challengeId: str,
    matchmakingId: str,
):
    url = api_url + f"/v2.0/challenge/group"

    body = {
        "matchmakingStartValue": matchmakingStartValue,
        "gamedataHash": gamedataHash,
        "challengeID": challengeId,
        "matchmakingId": matchmakingId,
    }

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers={
                **headers,
                "Authorization": f"Bearer {identityToken}",
            },
            json=body,
        )

        print(r.status_code)
        print(r.json())


# get_mail()
# crosspromo()
# auth_register()
# auth_refresh("")
# get_manifest(manifestSecret="s8B88pVbhzpKmvX6BV0u", game="subway",type="android",experiment="ab_google_play",version="3.44.2")
# get_gamedata("657db86da87f6e2625b1de17aaa7017975ff032f", "manifest")
# get_media("external", "SYBOxHipsterWhale/CrossyRoad/CSR_Static_FrankChicken.jpeg")
# assets("subway", "9917a9a0-0de9-40fb-bb80-392ee596f705/bundle/1.0.0/characters-remote_assets_pixeljake_default_outfit_config_7a3d5cbdbef0e42b386ceea8f110c324.bundle")
# gdpr_delete()
# gdpr_status()
# send_metrics()
# events()
# abtesting()
# send_tournament("de", "9174e7104115388308819319bdd411b0a11b1082")
# get_tournament()
# get_profile("01975933-cb36-7896-99c3-5ad6bd1a4dc2")
# get_networkcheck()
# get_cflocation()
# get_servertime()
# send_redeem("PrideFrame2025", 1)
# send_websdk()
# send_fbinstall()
# get_challenge("nl")
# get_challenge(39,"70409a79f9500482a5075052a93f15be22fc1383","daily_challenge_de","dailyChallenge")
