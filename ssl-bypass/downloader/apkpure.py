import sys
import requests
import re


def extract_strings(data):
    return re.findall(rb"[\x20-\x7E]{4,}", data)


def download_apk(app_id):
    url = "https://api.pureapk.com/m/v3/cms/app_version"
    headers = {
        "x-sv": "29",
        "x-abis": "arm64-v8a,armeabi-v7a,armeabi",
        "x-gp": "1",
    }
    params = {"hl": "en-US", "package_name": app_id}

    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()

    strings = extract_strings(resp.content)
    apk_paths = [s.decode() for s in strings if "/APK" in s.decode()]

    if not apk_paths:
        print("No APK path found.")
        return

    apk_url = apk_paths[0]
    print(f"Downloading from: {apk_url}")

    apk_resp = requests.get(apk_url, stream=True)
    apk_resp.raise_for_status()

    with open(f"{app_id}.apk", "wb") as f:
        for chunk in apk_resp.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Downloaded: {app_id}.apk")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <app_id>")
        sys.exit(1)
    download_apk(sys.argv[1])
