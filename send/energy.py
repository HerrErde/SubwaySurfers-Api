import httpx

from utils import *


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


# init_energy("0197780a-77bc-7bb8-bf9b-687fa58a53c0")
# get_energies()
# use_energy("0197780a-77bc-7bb8-bf9b-687fa58a53c0", 1)
# add_energy("0197780a-77bc-7bb8-bf9b-687fa58a53c0", 1)
