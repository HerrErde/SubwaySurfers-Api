# Explanations

## Table of Contents

- [Explanations](#explanations)
  - [Table of Contents](#table-of-contents)
  - [Skip Ad Tickets](#skip-ad-tickets)

## Skip Ad Tickets

You will need a PC and your phone for this.

You can use a programm called [reqable](https://reqable.com) \
You'll need to have rooted your phone or ssl-bypassed the app, wich you can do with the [script](./ssl-bypass/apk-rebuild.py) or you can use [revanced.app](https://revanced.app) (in setting enable "Show universal patches"). \
Select in the patch "Override certificate pinning".

Install the required certificates from the client onto your Phone as a "CA Certificate". \
Connect the phone to the PC client.

After patching the app and installing it open the programm. \
Copy this code into a file called `reqable-rewrites.config` \
In "Tools" go to "Rewrite" click on the "Import" button and import the config.

<details>
  <summary>reqable-rewrites.config</summary>

```json
[
  {
    "id": "ccb4f210-6495-42ee-a660-f14e53a901a9",
    "name": "UseEnergy/GetEnergies",
    "method": "",
    "url": "https://subway.prod.sybo.net/rpc/energy.ext.v1.PrivateService/*",
    "wildcard": true,
    "action": {
      "type": 2,
      "code": 200,
      "headers": [],
      "body": {
        "type": 1,
        "payload": "{\"energy\":{\"kindId\":\"0197780a-77bc-7bb8-bf9b-687fa58a53c0\",\"value\":10,\"regenCap\":3,\"updatedAt\":\"2025-10-03T00:01:23.857500Z\",\"refillRate\":\"14400s\",\"refillCount\":1}}"
      },
      "statusLineEnabled": true,
      "headersEnabled": false,
      "bodyEnabled": true
    },
    "isEnabled": true
  },
  {
    "id": "65aca52c-e90e-48a6-b50a-73ca5b0ae145",
    "name": "GetWallet",
    "method": "",
    "url": "https://subway.prod.sybo.net/rpc/wallet.ext.v1.PrivateService/GetWallet",
    "wildcard": false,
    "action": {
      "type": 2,
      "code": 200,
      "headers": [],
      "body": {
        "type": 1,
        "payload": "{\n  \"wallet\": {\n    \"items\": {\n      \"skip_ad_ticket\": 10\n    },\n    \"updatedAt\": \"2025-09-29T11:42:16.550165Z\"\n  }\n}"
      },
      "statusLineEnabled": true,
      "headersEnabled": false,
      "bodyEnabled": true
    },
    "isEnabled": true
  },
  {
    "id": "f39206b9-b985-49cd-abf6-2e7203cb4801",
    "name": "Consume",
    "method": "",
    "url": "https://subway.prod.sybo.net/rpc/wallet.ext.v1.PrivateService/Consume",
    "wildcard": false,
    "action": {
      "type": 2,
      "code": 200,
      "headers": [],
      "body": {
        "type": 1,
        "payload": "{\n  \"wallet\": {\n    \"items\": { \"skip_ad_ticket\": 10 },\n    \"updatedAt\": \"2025-09-29T11:42:16.550165Z\"\n  }\n}"
      },
      "statusLineEnabled": true,
      "headersEnabled": false,
      "bodyEnabled": true
    },
    "isEnabled": true
  }
]
```

</details>

Open then app, it will then redirect the requests and return the tickets and will make buying with tickets available.

> [!IMPORTANT]
> Remember this bypassing only works when the client on both PC and phone are running.
