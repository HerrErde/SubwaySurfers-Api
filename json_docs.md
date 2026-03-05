# Explanations

## Table of Contents

<details>
  <summary>Table of Contents</summary>

- [Explanations](#explanations)
  - [Table of Contents](#table-of-contents)
  - [General Notes](#general-notes)
      - [Auth](#auth)
      - [Register](#register)
      - [Refresh](#refresh)
      - [Play](#play)
        - [Play Connect](#play-connect)
        - [Play Login](#play-login)
        - [Play disconnect](#play-disconnect)
    - [Abtesting](#abtesting)
    - [Crosspromo](#crosspromo)
    - [Content](#content)
      - [Manifest](#manifest)
      - [Gamedata](#gamedata)
      - [Media](#media)
      - [Assets](#assets)
    - [GDPR](#gdpr)
      - [GDPR delete](#gdpr-delete)
      - [GDPR status](#gdpr-status)
    - [Challenge](#challenge)
      - [Sent Challenge](#sent-challenge)
      - [Get Challenge](#get-challenge)
      - [Sent Challenge Score](#sent-challenge-score)
    - [Tournament](#tournament)
      - [Send Tournament](#send-tournament)
      - [Get Tournament](#get-tournament)
    - [Profile](#profile)
      - [Get Profile](#get-profile)
      - [Get Player Profile](#get-player-profile)
      - [Send Profile](#send-profile)
    - [Mail](#mail)
      - [Get](#get)
      - [Read](#read)
      - [Claim](#claim)
    - [Analytics](#analytics)
      - [Analytics Core](#analytics-core)
    - [Deep Links](#deep-links)
      - [Redeem](#redeem)

</details>

## General Notes

All knowledge is for versions `3.59.2`

> [!WARNING]
> Changes are expected to happen

After registering an account, you'll have to create a player to use all the requests; otherwise, the account is 'empty' and can't perform player actions.

You can only add [abtesting](#abtesting) to the account after adding [crosspromo](#crosspromo). This must be done in that order, else it will result in an error.

this is a player tag `BY1BJH84CVHHIX` \
this is a player uid `0197351b-ae06-7a3f-8576-0e3d5b95a280`

Some response bodies that contain repeating data or with minor changes will be truncated to avoid repetition.

The default api url is `subway.prod.sybo.net`

#### Auth

#### Register

- POST `/v2.0/auth/register`
- Will register a player account
- Sample request (2025-12-19): \
  POST /v2.0/auth/register

- Sample response:

  ```json
  {
    "idToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMTk2OGMzYS0zZmVhLTdhYmMtODk3Yy1lMWExO...",
    "idTokenTtl": 604800,
    "refreshToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMTk2NzJiOS0yZThiLTc0NWEtOWQ1My1lMzg4MT...",
    "user": { "id": "01968c3a-3fea-7abc-897c-e1a1814ba489", "links": [] }
  }
  ```

This creates an empty account and returns an identity token and a refresh token. \
It generates a idenity and a refresh token, with a ttl (time to live). \
The account itself does not yet have a player profile. To initialize the player, you must send a request to [CreatePlayer](./grpc_docs.md#create-player) with data. \
Only after creating the player, other game-related requests, such as [UpdatePlayer](./grpc_docs.md#update-player), be used.

#### Refresh

- POST `/v2.0/auth/refresh`
- Refresh the accounts identity token
- Sample request (2025-12-19): \
  POST /v2.0/auth/refresh \
  Authorization: `Bearer <identityToken>`

  Body:

  ```json
  {
    "refreshToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMTk2NzJiOS0yZThiLTc0NWEtOWQ1My1lMzg4MT...",
    "fbAccessToken": null
  }
  ```

- Sample response:

  ```json
  {
    "idToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMTk2OGMzYS0zZmVhLTdhYmMtODk3Yy1lMWExO...",
    "idTokenTtl": 604800,
    "refreshToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMTk2NzJiOS0yZThiLTc0NWEtOWQ1My1lMzg4MT...",
    "user": { "id": "01968c3a-3fea-7abc-897c-e1a1814ba489", "links": [] }
  }
  ```

This refreshes the accounts identity token and returns a new token, allowing the account to continue making authenticated requests.

#### Play

##### Play Connect

- POST `/v1.0/auth/play/connect`
- Play connect
- Sample request (2026-02-26): \
  POST /v1.0/auth/play/connect \
  Authorization: `Bearer <identityToken>` \
  Body:

  ```json
  {
    "authcode": "4/0AfrIepArxA2nQmU1-..."
  }
  ```

<h5>Default Response</h5>

```json
{
  "idToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9...",
  "idTokenTtl": 604800,
  "refreshToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9..",
  "user": {
    "id": "0198836e-fb91-7900-9fa4-598349e4a77d",
    "links": [{ "type": "play", "id": "a_2520406209192914419" }]
  }
}
```

<h5>Error Response</h5>

```json
{ "error": "request failed", "kind": 6 }
```

##### Play Login

- POST `/v1.0/auth/play/login`
- Play login
- Sample request (2026-02-26): \
  POST /v1.0/auth/play/login \
  Authorization: `Bearer <identityToken>` \
  Body:

  ```json
  {
    "authcode": "4/0AfrIepDPZf2gwn0pDNzTbSYhKr8twvlo-a9U-9jVP7TPS-qoj_0jDmrlJyDQbFNUkzGH7Q"
  }
  ```

<h5>Default Response</h5>

```json
{
  "idToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9...",
  "idTokenTtl": 604800,
  "refreshToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9..",
  "user": {
    "id": "0198836e-fb91-7900-9fa4-598349e4a77d",
    "links": [{ "type": "play", "id": "a_2520406209192914419" }]
  }
}
```

##### Play disconnect

- POST `/v1.0/auth/play/disconnect`
- Play disconnect
- Sample request (2026-03-05): \
  POST /v1.0/auth/play/disconnect \
  Authorization: `Bearer <identityToken>` \
  Body:
  None

<h5>Default Response</h5>

```json
{
  "idToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9...",
  "idTokenTtl": 604800,
  "refreshToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9..",
  "user": {
    "id": "0198836e-fb91-7900-9fa4-598349e4a77d",
    "links": []
  }
}
```

### Abtesting

- GET `/v1.0/abtesting/match`
- Returns the accounts experiment
- Sample request (2025-02-23): \
  GET /v1.0/abtesting/match \
  Authorization: `Bearer <identityToken>`
  Body:

  ```json
  {
    "metrics": {
      "payer": "false",
      "level": "1",
      "genuine_app": "Genuine",
      "language": "en",
      "age": "69",
      "platform": "android",
      "coppa": "true",
      "install_source": "com.android.vending",
      "gameVersion": "3.59.0"
    }
  }
  ```

  <h5>Response without experiment</h5>

  Status: 204

  <h5>Response with experiemnt</h5>

  Status: 200

  ```json
  {
    "experimentId": "ex_interstitials_specs_v2",
    "variantId": "ab_interstitials_specifications_D",
    "endDate": "2026-08-29T13:58:00.107Z"
  }
  ```

This request returns the experiment assigned to the account. \
When you want to play with other experiments you can change them [here](./hacks.md#play-with-experiments). \
The app uses this information to determine which tower gamedata files to load.

### Crosspromo

- GET `/v2.0/crosspromo/match`
- Returns users crosspromo match
- Sample request (2025-02-23): \
  GET /v2.0/crosspromo/match \
  Authorization: `Bearer <identityToken>`
  Body:

  ```json
  {
    "test": "false",
    "language": "en",
    "metrics": {
      "payer": "false",
      "level": "1",
      "age": "69",
      "genuine_app": "Genuine",
      "language": "en",
      "platform": "android",
      "coppa": "true",
      "install_source": "com.android.vending",
      "gameVersion": "3.59.0"
    },
    "attribution": null
  }
  ```

- Sample response:

  ```json
  {
    "globalConf": {
      "impressionCap": { "count": 50, "interval": 86400000000000 },
      "frequencyCap": { "count": 25, "interval": 3600000000000 }
    },
    "campaigns": [],
    "attribution": {}
  }
  ```

### Content

#### Manifest

Url is <https://manifest.tower.sybo.net>

- GET `/v1.0/{game}/{version}/{type}/{secret}/{experiment}/manifest.json`
- Gets the manifest of a game version
- Sample request (2025-12-20): \
  GET /v1.0/{game}/{version}/{type}/{secret}/{experiment}/manifest.json

For specific experiments you can set `ab_google_play`, `ab_revive_codechange` else dont set it.

<details>
  <summary>Android production</summary>

```json
{
  "secret": "VNpc4sJF7jpOUyv2jaev",
  "game": "subway",
  "platform": "android",
  "version": "3.47.0",
  "lifecycle": "production",
  "addressables": null,
  "services": {
    "subway-dev": "https://subway.dev.sybo.net",
    "subway-prod": "https://subway.prod.sybo.net",
    "subway-staging": "https://subway.stage.sybo.net"
  },
  "metadata": {
    "analytics_sample": "100",
    "support_url": "https://sybo.helpshift.com/hc/app/5-subway-surfers"
  },
  "gamedata": "33c0f767cb91470fb47a1c68a8fc8f940a2f0084"
}
```

</details>

<details>
  <summary>Android development</summary>

```json
{
  "secret": "Z5CmrtIpfU7sJ3tssL6T",
  "game": "subway",
  "platform": "android",
  "version": "3.47.1",
  "lifecycle": "development",
  "addressables": null,
  "services": {
    "subway-dev": "https://subway.dev.sybo.net",
    "subway-prod": "https://subway.prod.sybo.net",
    "subway-staging": "https://subway.stage.sybo.net"
  },
  "metadata": {
    "analytics_sample": "100",
    "support_url": "https://sybo.helpshift.com/hc/app/5-subway-surfers"
  },
  "gamedata": "9174e7104115388308819319bdd411b0a11b1082"
}
```

</details>
<details>
  <summary>Apple deprecated</summary>

```json
{
  "secret": "4fPvIR1E1SnL1LRl9453",
  "game": "subway",
  "platform": "ios",
  "version": "3.36.0",
  "lifecycle": "deprecated",
  "addressables": null,
  "services": {
    "subway-dev": "https://subway.dev.sybo.net",
    "subway-prod": "https://subway.prod.sybo.net",
    "subway-staging": "https://subway.stage.sybo.net"
  },
  "metadata": {
    "analytics_sample": "100",
    "att_age": "16",
    "att_sampling": "false",
    "att_tracking": "true",
    "force_coppa_only": "true",
    "support_url": "https://sybo.helpshift.com/hc/app/5-subway-surfers",
    "version_expire_date": "2024-11-04T08:26:10Z"
  },
  "gamedata": "49dd76f61b88ad5ec0c370f29c040b38274601e8"
}
```

</details>

<br>

Notes: \
 From this data you get the version specific manifest data. \
 Which gives useful data like gamedata hash and lifecycle. \
 You get the secret by extracting it from the game file (apk or ipa). \
 The `assets/settings/sybo.tower.default.json` (ipa is `Payload/SubwaySurf.app/Data/Raw/settings/sybo.tower.default.json`) file contains a key called `Secret`, with the version specific secret.

**Url examples**

```
https://manifest.tower.sybo.net/v1.0/subway/3.36.0/ios/4fPvIR1E1SnL1LRl9453/manifest.json
https://manifest.tower.sybo.net/v1.0/subway/3.44.1/android/99fGW8FHpmAbQR4BqBwr/manifest.json
https://manifest.tower.sybo.net/v1.0/subway/3.44.2/ios/s8B88pVbhzpKmvX6BV0u/manifest.json
https://manifest.tower.sybo.net/v1.0/subway/3.44.2/android/s8B88pVbhzpKmvX6BV0u/ab_revive_codechange/manifest.json
https://manifest.tower.sybo.net/v1.0/subway/3.44.2/android/s8B88pVbhzpKmvX6BV0u/manifest.json
```

_Default Schema_

```
https://manifest.tower.sybo.net/v1.0/{game}/{version}/{platform}/{secret}/manifest.json
```

_Experiment Schema_

```
https://manifest.tower.sybo.net/v1.0/{game}/{version}/{platform}/{secret}/{experiment}/manifest.json
```

- GET `/v2.0/{game}/{version}/{type}/{secret}/{experiment}/archive.zip`
- Get the manifest of a game version
- Sample request (2025-12-20): \
  GET /v2.0/{game}/{version}/{type}/{secret}/{experiment}/archive.zip

When using the v2.0 schema, you can use the `archive.zip` endpoint to get a zip file of the game files. \
It seems like the v2.0 schema only has the `archive` endpoint, all other do not exist.

```
https://manifest.tower.sybo.net/v2.0/subway/3.49.1/android/junpNkV78FJxO4dlGAbO/archive.zip
```

The archive.zip contains the manifest.json aswell as a `data` folder with the gamedata files.

```
manifest.json
data/
   boards.json
   calendars.json
   ...
```

#### Gamedata

Url is <https://gamedata.tower.sybo.net>

- GET `/v1.0/{game}/{secret}/{filename}.json`
- Get gamedata files of manifest version
- Sample request (2025-12-20): \
  GET /v1.0/{game}/{secret}/{filename}.json

You can retrieve the gamedata/tower files using the hash value from the `gamedata` field in the manifest request, instead of the old deprecated method of extracting them from the APK or IPA (IPA extraction still works). \
(state 3.56.0)

You can request the `manifest.json`, which contains a list of all files included in the gamedata.

```json
{
  "experiment": "default",
  "game": "subway",
  "objects": {
    "achievements": {
      "filename": "achievements.json",
      "key": "2bed33daedf13ae310d90edff852600598e665e3"
    },
    "adplacements": {
      "filename": "adplacements.json",
      "key": "2010b70022bba2451310a6e60166a4b31f21fe0b"
    },
    "assemblyevents": {
      "filename": "assemblyevents.json",
      "key": "4fa66108ddd7f8bead20b40f6a8b505a9cdf098f"
    }
    (truncated)
  },
  "spec": "v1.0",
  "version": "3.46.0"
}
```

```
https://gamedata.tower.sybo.net/v1.0/subway/c84ca921a6249f9fa201444ed03f54238e8aaaa2/manifest.json
```

#### Media

Url is <https://media.sybo.net>

- GET `/{game}/cross_promotion/{promotion}/Image/{image}`
- Get media files
- Sample request (2025-12-20): \
  GET /{game}/cross_promotion/{promotion}/Image/{image}

```
https://media.sybo.net/{game}/cross_promotion/{promotion}/Image/{image}
```

known game promotions \
`ssmatch`, `ssblast`, `brim`, `external`

#### Assets

Url is <https://assets.tower.sybo.net>

- GET `/`
- Get game assets files
- Sample request (2025-12-20): \
  GET /

When getting the root of the url it shows what seems to be a list of a bucket

<details>
  <summary>Assets Response</summary>

```xml
<ListBucketResult>
<Name>sybogames-tower-assets</Name>
<Prefix/>
<Marker/>
<NextMarker>
v1.0/BRIM/20b6aac8-db25-45b7-b2e7-35efdf27a83d/catalog/1.0.0/catalog_2024.02.27.05.56.51.hash
</NextMarker>
<IsTruncated>true</IsTruncated>
<Contents>
<Key>
v1.0.0/ReleaseTesterApp/08ad4fa1-1fb6-4a8c-a782-de8c725f3e5e/addressable_data
</Key>
<Generation>1672672180447593</Generation>
<MetaGeneration>1</MetaGeneration>
<LastModified>2023-01-02T15:09:40.478Z</LastModified>
<ETag>"d41d8cd98f00b204e9800998ecf8427e"</ETag>
<Size>0</Size>
</Contents>
...
<Contents>
<Key>
v1.0/Atlas/a820cd4f-b422-4e04-8c46-b19db72f0b99/catalog/1.0.0/catalog_2021.11.25.10.14.22.json
</Key>
<Generation>1637836239952983</Generation>
<MetaGeneration>1</MetaGeneration>
<LastModified>2021-11-25T10:30:39.996Z</LastModified>
<ETag>"893cf305a3c4046801ffb92dc866f35d"</ETag>
<Size>9017</Size>
</Contents>
...
<Contents>
<Key>
v1.0/BRIM/0004b3b2-328d-40a6-8d5c-cdb07dbfa7bc/catalog/1.0.0/catalog_2023.11.15.10.18.13.hash
</Key>
<Generation>1700044260436100</Generation>
<MetaGeneration>1</MetaGeneration>
<LastModified>2023-11-15T10:31:00.468Z</LastModified>
<ETag>"fb9d3d1895d092d22581315f15d39373"</ETag>
<Size>32</Size>
</Contents>
```

</details>

<br>

- GET `v1.0/{game}/{bundleId}/{type}/{version}/{file}`
- Get game assets files
- Sample request (2025-12-20): \
  GET v1.0/{game}/{bundleId}/{type}/{version}/{file}

```
https://assets.tower.sybo.net/v1.0/subway/f78e0ec2-cd8a-4d77-8c25-ad227d468816/bundle/1.0.0/boardspreviews-remote_assets_meangreenmachine_default_preview_big_8e39610ba8a1458c7e1479316c158261.bundle
```

This request will return the asset in the UnityFs format

Inside the apk (`assets/aa/catalog.json`) or ios (`Payload/SubwaySurf.app/Data/Raw/aa/catalog.json`) `catalog.json` file, the `m_InternalIds` list contains all file entries. These are links starting with `sybo://`, such as:

```
sybo://9917a9a0-0de9-40fb-bb80-392ee596f705/bundle/1.0.0/characters-remote_assets_pixeljake_default_outfit_config_7a3d5cbdbef0e42b386ceea8f110c324.bundle
```

These entries reference the actual asset bundles used by the game.

### GDPR

#### GDPR delete

- POST `/v1.0/gdpr/delete`
- Requests a account deletion
- Sample request (2025-12-19): \
  POST /v1.0/gdpr/delete \
  Authorization: `Bearer <identityToken>`

- Sample response:

  ```json
  {
    "job": {
      "kind": 1,
      "state": 0,
      "url": "",
      "createdAt": "2025-12-10T18:02:01.581790628Z",
      "endetAt": null
    }
  }
  ```

This is the account deletion request that will delete your account.

It only deletes your public profile (that was is shown when other players look at your player) not your save data. \
When you are friends with a player, you will get removed from their friends list.

#### GDPR status

- GET `/v1.0/gdpr/status`
- Get the status of the player deletion
- Sample request (2025-12-19): \
  GET /v1.0/gdpr/status \
  Authorization: `Bearer <identityToken>` \
  Body:

  ```json
  { "gaid": "00000000-0000-0000-0000-000000000000" }
  ```

- Sample response:

  ```json
  {
    "job": {
      "kind": 1,
      "state": 1,
      "url": "",
      "createdAt": "2025-12-10T18:02:01.581790628Z",
      "endetAt": "2025-12-10T18:02:02.566636Z"
    }
  }
  ```

This is the account delete status request, with which you get the status of the current account delete request.

### Challenge

<details id="challenge_response">
  <summary>Challenge Response</summary>

```json
{
  "group": {
    "start": "2025-07-04T11:22:00Z",
    "end": "2025-07-05T11:22:00Z",
    "players": [
      {
        "uid": "00d2487c-8bc3-460d-aeb5-de8754878bd2",
        "matchmakingValue": 6,
        "name": "",
        "picture": "",
        "socialIds": [],
        "metadata": [
          { "key": "score", "value": "44333" },
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "default_frame" },
          { "key": "portrait", "value": "jake_portrait" },
          { "key": "character", "value": "tricky.default" },
          { "key": "board", "value": "default" }
        ]
      },
      {
        "uid": "0193b9de-e911-7d30-92e5-17d4e1798ddc",
        "matchmakingValue": 6,
        "name": "",
        "picture": "",
        "socialIds": [],
        "metadata": [
          { "key": "portrait", "value": "jake_portrait" },
          { "key": "character", "value": "tricky.default" },
          { "key": "board", "value": "default" },
          { "key": "score", "value": "95374" },
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "default_frame" }
        ]
      },
      (truncated 7x)
      {
        "uid": "0197d683-d0f4-7563-bcc6-b285ff6fa1f5",
        "matchmakingValue": 0,
        "name": "",
        "picture": "",
        "socialIds": [],
        "metadata": []
      }
    ]
  }
}
```

</details>

#### Sent Challenge

- POST `/v2.0/challenge/group`
- Sets the Challenge Group
- Sample request (2025-12-19): \
  POST /v2.0/challenge/group \
  Authorization: `Bearer <identityToken>` \
  Body:

  ```json
  {
    "matchmakingStartValue": 29,
    "gamedataHash": "70409a79f9500482a5075052a93f15be22fc1383",
    "challengeID": "daily_challenge_de",
    "matchmakingId": "dailyChallenge"
  }
  ```

- Sample response: \
   See above [challenge_response](#challenge_response)

This request is made when opening the view of a challenge in the Events tab

It is not known from what the `matchmakingStartValue` is from

<h5>Already send request</h5>

```json
{ "error": "request failed", "kind": 6 }
```

When setting the challengeID to `daily_challenge_nl`, you will only be able to use the get_challenge request with the challenge group for that country, here `nl`.

<h5>Requesting another challenge when already having send a challenge</h5>

```json
{ "error": "request failed", "kind": 5 }
```

#### Get Challenge

- GET `/v2.0/challenge/<challenge>/group`
- Gets the Challenge Group
- Sample request (2025-12-19): \
  GET /v2.0/challenge/<challenge\>/group \
  Authorization: `Bearer <identityToken>`

- Sample response: \
   See above [challenge_response](#challenge_response)

The Challenge name is build like this \
the challenge type like: `daily_challenge`, `staged_tta` \
and the country code: `en`, `nl`

```
<challenge>_<c>
```

the country code has to be the same as in the [send](#sent-challenge) request as `matchmakingId` value

#### Sent Challenge Score

- POST `/v2.0/challenge/score`
- Sends the Challenge Scores
- Sample request (2026-03-05): \
   POST /v2.0/challenge/score \
   Authorization: `Bearer <identityToken>` \
   Body:

  <details>

  ```json
  {
    "scores": [
      {
        "metadata": [
          {
            "key": "background",
            "value": "default_background"
          },
          {
            "key": "frame",
            "value": "plant_frame"
          },
          {
            "key": "portrait",
            "value": "tagbot_portrait"
          },
          {
            "key": "character",
            "value": "jake.default"
          },
          {
            "key": "board",
            "value": "default"
          },
          {
            "key": "score",
            "value": "2147483647"
          }
        ],
        "tournamentId": "marathon_de",
        "matchmakingValue": 1
      },
      {
        "metadata": [
          {
            "key": "background",
            "value": "default_background"
          },
          {
            "key": "frame",
            "value": "plant_frame"
          },
          {
            "key": "portrait",
            "value": "tagbot_portrait"
          },
          {
            "key": "character",
            "value": "jake.default"
          },
          {
            "key": "board",
            "value": "default"
          },
          {
            "key": "score",
            "value": "2147483647"
          }
        ],
        "tournamentId": "marathon_de",
        "matchmakingValue": 1
      },
      {
        "metadata": [
          {
            "key": "background",
            "value": "default_background"
          },
          {
            "key": "frame",
            "value": "plant_frame"
          },
          {
            "key": "portrait",
            "value": "tagbot_portrait"
          },
          {
            "key": "character",
            "value": "jake.default"
          },
          {
            "key": "board",
            "value": "default"
          },
          {
            "key": "score",
            "value": "2147483647"
          }
        ],
        "tournamentId": "mystery_hurdles_de",
        "matchmakingValue": 1
      },
      {
        "metadata": [
          {
            "key": "background",
            "value": "default_background"
          },
          {
            "key": "frame",
            "value": "plant_frame"
          },
          {
            "key": "portrait",
            "value": "tagbot_portrait"
          },
          {
            "key": "character",
            "value": "jake.default"
          },
          {
            "key": "board",
            "value": "default"
          },
          {
            "key": "score",
            "value": "20"
          }
        ],
        "tournamentId": "daily_challenge_de",
        "matchmakingValue": 39
      }
    ]
  }
  ```

  </details>

  <h5>Default Response</h5>

  `200 OK`

This request will send the scores and player metadata of each challenge

### Tournament

<details id="tournament_response">
  <summary>Tournament Response</summary>

```json
{
  "group": {
    "week": 51,
    "start": "2025-12-15T09:00:00Z",
    "end": "2025-12-22T09:00:00Z",
    "tournamentId": "de",
    "brackets": {
      "current": {
        "matchmaking": {
          "groupSize": 20,
          "bracketMaxUsers": { "champion": 1 },
          "bracketSort": {
            "bronze": 1,
            "diamond": 4,
            "gold": 3,
            "none": 0,
            "silver": 2
          },
          "bracketPercentage": {
            "bronze": 0.2,
            "diamond": 0.02,
            "gold": 0.05,
            "none": 0.63,
            "silver": 0.1
          },
          "bracketDistribution": {
            "bronze": {
              "bronze": 8,
              "diamond": 1,
              "gold": 3,
              "none": 3,
              "silver": 4
            },
            "diamond": {
              "bronze": 2,
              "diamond": 8,
              "gold": 6,
              "none": 0,
              "silver": 3
            },
            "gold": {
              "bronze": 2,
              "diamond": 4,
              "gold": 7,
              "none": 1,
              "silver": 5
            },
            "none": {
              "bronze": 5,
              "diamond": 1,
              "gold": 2,
              "none": 8,
              "silver": 3
            },
            "silver": {
              "bronze": 4,
              "diamond": 2,
              "gold": 4,
              "none": 2,
              "silver": 7
            }
          }
        },
        "bounds": {
          "bronze": 1111625,
          "diamond": 11671820,
          "gold": 5644449,
          "none": 1,
          "silver": 2978277
        }
      },
      "past": {
        "matchmaking": {
          "groupSize": 20,
          "bracketMaxUsers": { "champion": 1 },
          "bracketSort": {
            "bronze": 1,
            "diamond": 4,
            "gold": 3,
            "none": 0,
            "silver": 2
          },
          "bracketPercentage": {
            "bronze": 0.2,
            "diamond": 0.02,
            "gold": 0.05,
            "none": 0.63,
            "silver": 0.1
          },
          "bracketDistribution": {
            "bronze": {
              "bronze": 8,
              "diamond": 1,
              "gold": 3,
              "none": 3,
              "silver": 4
            },
            "diamond": {
              "bronze": 2,
              "diamond": 8,
              "gold": 6,
              "none": 0,
              "silver": 3
            },
            "gold": {
              "bronze": 2,
              "diamond": 4,
              "gold": 7,
              "none": 1,
              "silver": 5
            },
            "none": {
              "bronze": 5,
              "diamond": 1,
              "gold": 2,
              "none": 8,
              "silver": 3
            },
            "silver": {
              "bronze": 4,
              "diamond": 2,
              "gold": 4,
              "none": 2,
              "silver": 7
            }
          }
        },
        "bounds": {
          "bronze": 1015174,
          "diamond": 10872653,
          "gold": 5720604,
          "none": 1,
          "silver": 4009517
        }
      }
    },
    "players": [
      {
        "uid": "0199a69c-cab2-77b6-80c4-b5048650e431",
        "scores": { "current": 103251, "past": 0 },
        "socialIds": [],
        "metadata": [
          { "key": "score", "value": "103251" },
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "default_frame" },
          { "key": "portrait", "value": "amongusred_illustration_portrait" },
          { "key": "character", "value": "tricky.default" },
          { "key": "board", "value": "superhero" }
        ],
        "name": "",
        "picture": ""
      },
      {
        "uid": "019a4ab2-d099-7eea-a864-bd898f8f8b95",
        "scores": { "current": 121918, "past": 201291 },
        "socialIds": [],
        "metadata": [
          { "key": "score", "value": "121918" },
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "default_frame" },
          { "key": "portrait", "value": "tagbot_portrait" },
          { "key": "character", "value": "fresh.default" },
          { "key": "board", "value": "chillOut" }
        ],
        "name": "",
        "picture": ""
      },
      {
        "uid": "019b12ab-ce46-7b6a-9b12-ea664b18d8a0",
        "scores": { "current": 61545, "past": 108151 },
        "socialIds": [],
        "metadata": [
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "default_frame" },
          { "key": "portrait", "value": "jake_portrait" },
          { "key": "character", "value": "jake.default" },
          { "key": "board", "value": "sunset" },
          { "key": "score", "value": "61545" }
        ],
        "name": "",
        "picture": ""
      },
      {
        "uid": "44981f1f-16a8-44e5-b120-bf141e8cd820",
        "scores": { "current": 351149, "past": 0 },
        "socialIds": [],
        "metadata": [
          { "key": "character", "value": "jake.default" },
          { "key": "board", "value": "xmas2022" },
          { "key": "score", "value": "351149" },
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "default_frame" },
          { "key": "portrait", "value": "jake_portrait" }
        ],
        "name": "",
        "picture": ""
      },
      {
        "uid": "01948ea1-40ea-7787-a44e-0e42a545c33b",
        "scores": { "current": 192, "past": 258238 },
        "socialIds": [],
        "metadata": [
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "brawlstars_frame" },
          {
            "key": "portrait",
            "value": "eightball_jake_illustration_portrait"
          },
          { "key": "character", "value": "malik.default" },
          { "key": "board", "value": "bouncer" },
          { "key": "score", "value": "192" }
        ],
        "name": "",
        "picture": ""
      },
      {
        "uid": "819ffb4b-0cef-444b-92bc-14fbc2c7d5ed",
        "scores": { "current": 64327, "past": 0 },
        "socialIds": [],
        "metadata": [
          { "key": "character", "value": "tricky.default" },
          { "key": "board", "value": "starboard" },
          { "key": "score", "value": "64327" },
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "default_frame" },
          { "key": "portrait", "value": "jake_portrait" }
        ],
        "name": "",
        "picture": ""
      },
      {
        "uid": "0195486a-0e6d-7ae1-962f-0ae85c697040",
        "scores": { "current": 604963, "past": 3117635 },
        "socialIds": [],
        "metadata": [
          { "key": "frame", "value": "default_frame" },
          { "key": "portrait", "value": "jake_portrait" },
          { "key": "character", "value": "clockworkJohnny.default" },
          { "key": "board", "value": "starboard" },
          { "key": "score", "value": "604963" },
          { "key": "background", "value": "default_background" }
        ],
        "name": "",
        "picture": ""
      },
      {
        "uid": "b79d6980-1218-4119-936f-63b793a0ca11",
        "scores": { "current": 721837, "past": 1043417 },
        "socialIds": [],
        "metadata": [
          { "key": "board", "value": "boombastic" },
          { "key": "score", "value": "721837" },
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "default_frame" },
          { "key": "portrait", "value": "jake_portrait" },
          { "key": "character", "value": "bsToughGuy.default" }
        ],
        "name": "",
        "picture": ""
      },
      {
        "uid": "0193de86-0dec-7745-b1e8-ad5a5b02b105",
        "scores": { "current": 96327, "past": 223308 },
        "socialIds": [],
        "metadata": [
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "brawlstars_frame" },
          { "key": "portrait", "value": "amongusred_illustration_portrait" },
          { "key": "character", "value": "amongUsBlack.default" },
          { "key": "board", "value": "daredevil" },
          { "key": "score", "value": "96327" }
        ],
        "name": "",
        "picture": ""
      },
      {
        "uid": "0196c557-c905-734b-8657-484b53b53cae",
        "scores": { "current": 2147483647, "past": 0 },
        "socialIds": [],
        "metadata": [
          { "key": "board", "value": "default" },
          { "key": "score", "value": "2147483647" },
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "default_frame" },
          { "key": "portrait", "value": "jake_portrait" },
          { "key": "character", "value": "jake.default" }
        ],
        "name": "",
        "picture": ""
      },
      {
        "uid": "37a6ac9b-e0a9-4c8c-97ce-d12e182b08bf",
        "scores": { "current": 1099143, "past": 0 },
        "socialIds": [],
        "metadata": [
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "default_frame" },
          { "key": "portrait", "value": "tagbot_portrait" },
          { "key": "character", "value": "lucy.default" },
          { "key": "board", "value": "mapleLeaf" },
          { "key": "score", "value": "1099143" }
        ],
        "name": "",
        "picture": ""
      },
      {
        "uid": "b6e643d3-420d-4f8e-99f0-434675795022",
        "scores": { "current": 383132, "past": 1112872 },
        "socialIds": [],
        "metadata": [
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "default_frame" },
          { "key": "portrait", "value": "jake_portrait" },
          { "key": "character", "value": "lawrence.snowballerOutfit" },
          { "key": "board", "value": "chillOut" },
          { "key": "score", "value": "383132" }
        ],
        "name": "",
        "picture": ""
      },
      {
        "uid": "0199cf10-e729-7076-a3de-0caa0b1bbc7f",
        "scores": { "current": 1633, "past": 0 },
        "socialIds": [],
        "metadata": [
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "default_frame" },
          { "key": "portrait", "value": "jake_portrait" },
          { "key": "character", "value": "tricky.default" },
          { "key": "board", "value": "default" },
          { "key": "score", "value": "1633" }
        ],
        "name": "",
        "picture": ""
      },
      {
        "uid": "01973045-4be7-7290-b6ac-28b49eb844b7",
        "scores": { "current": 944045, "past": 1470331 },
        "socialIds": [],
        "metadata": [
          { "key": "board", "value": "fauxpunx" },
          { "key": "score", "value": "944045" },
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "gingerbread_frame" },
          { "key": "portrait", "value": "dino_portrait" },
          { "key": "character", "value": "gingerbot.wrapperOutfit" }
        ],
        "name": "",
        "picture": ""
      },
      {
        "uid": "0197a33e-02b6-779e-bff9-eb9361ad514b",
        "scores": { "current": 361453, "past": 940694 },
        "socialIds": [],
        "metadata": [
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "default_frame" },
          { "key": "portrait", "value": "amongusred_illustration_portrait" },
          { "key": "character", "value": "tricky.default" },
          { "key": "board", "value": "superhero" },
          { "key": "score", "value": "361453" }
        ],
        "name": "",
        "picture": ""
      },
      {
        "uid": "019afe53-24c2-7cd1-9560-be2590bb593c",
        "scores": { "current": 37706, "past": 321155 },
        "socialIds": [],
        "metadata": [
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "default_frame" },
          { "key": "portrait", "value": "dino_portrait" },
          { "key": "character", "value": "jake.default" },
          { "key": "board", "value": "greatWhite" },
          { "key": "score", "value": "37706" }
        ],
        "name": "",
        "picture": ""
      },
      {
        "uid": "4c52b9a9-fd0e-4ccb-9496-ca5ffaa075a2",
        "scores": { "current": 5914707, "past": 4216229 },
        "socialIds": [],
        "metadata": [
          { "key": "score", "value": "5914707" },
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "default_frame" },
          { "key": "portrait", "value": "amongusred_illustration_portrait" },
          { "key": "character", "value": "amongUsGreen.default" },
          { "key": "board", "value": "fauxpunx" }
        ],
        "name": "",
        "picture": ""
      },
      {
        "uid": "1673654b-9c1a-4d19-8a4c-ea05816c04ad",
        "scores": { "current": 297315, "past": 7826692 },
        "socialIds": [],
        "metadata": [
          { "key": "board", "value": "bigKahuna" },
          { "key": "score", "value": "297315" },
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "default_frame" },
          { "key": "portrait", "value": "jake_portrait" },
          { "key": "character", "value": "ella.default" }
        ],
        "name": "",
        "picture": ""
      },
      {
        "uid": "61f4fedd-3a85-43bb-92b4-6455f5684426",
        "scores": { "current": 87605, "past": 0 },
        "socialIds": [],
        "metadata": [
          { "key": "frame", "value": "default_frame" },
          { "key": "portrait", "value": "jake_portrait" },
          { "key": "character", "value": "jake.default" },
          { "key": "board", "value": "default" },
          { "key": "score", "value": "87605" },
          { "key": "background", "value": "default_background" }
        ],
        "name": "",
        "picture": ""
      },
      {
        "uid": "01950e8e-eddb-7cd8-803a-1b444a5f0bc6",
        "scores": { "current": 1919537, "past": 1191779 },
        "socialIds": [],
        "metadata": [
          { "key": "score", "value": "1919537" },
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "default_frame" },
          { "key": "portrait", "value": "amongusred_illustration_portrait" },
          { "key": "character", "value": "malik.default" },
          { "key": "board", "value": "jingles" }
        ],
        "name": "",
        "picture": ""
      },
      {
        "uid": "425ea9b4-2405-4028-abb0-5b461bf2d985",
        "scores": { "current": 153579, "past": 193191 },
        "socialIds": [],
        "metadata": [
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "default_frame" },
          { "key": "portrait", "value": "jake_portrait" },
          { "key": "character", "value": "lucy.gothOutfit" },
          { "key": "board", "value": "flyingHorse" },
          { "key": "score", "value": "153579" }
        ],
        "name": "",
        "picture": ""
      }
    ]
  }
}
```

</details>

#### Send Tournament

- POST `/v3.0/tournament/group`
- Registers the player for the tournament (leaderboard)
- Sample request (2025-12-19): \
  POST /v3.0/tournament/group \
  Authorization: `Bearer <identityToken>` \
  Body:

  ```json
  {
    "tournamentId": "de",
    "gamedataHash": "932032004ba8ca40ab8c07890b0300a5c2b171fe"
  }
  ```

- Sample response: \
   See above [tournament_response](#tournament_response)

#### Get Tournament

- GET `/v3.0/tournament/group`
- Returns the current tournament (leaderboard)
- Sample request (2025-12-19): \
  POST /v3.0/tournament/group \
  Authorization: `Bearer <identityToken>`

- Sample response: \
   See above [tournament_response](#tournament_response)

### Profile

**truncated version with only wallet, dataConsent, missedRewardsModels**

<details>
  <summary>Escaped Profile</summary>

```json
{
  "profile": "{\"wallet\":{\"version\":3,\"data\":\"{\\\"lastSaved\\\":\\\"2025-06-09T18:05:55.133242Z\\\",\\\"currencies\\\":{\\\"3\\\":{\\\"value\\\":278,\\\"expirationType\\\":0},\\\"2\\\":{\\\"value\\\":953,\\\"expirationType\\\":0},\\\"4\\\":{\\\"value\\\":184,\\\"expirationType\\\":0},\\\"5\\\":{\\\"value\\\":270,\\\"expirationType\\\":0},\\\"1\\\":{\\\"value\\\":945994,\\\"expirationType\\\":0},\\\"lootboxQueue\\\":{\\\"unopenedLootboxes\\\":[]},\\\"currencyAllowedInRun\\\":{\\\"5\\\":true,\\\"4\\\":true},\\\"lootBoxesOpened\\\":{\\\"mini_mystery_box\\\":2515,\\\"mystery_box\\\":4786,\\\"token_box\\\":7,\\\"super_mystery_box\\\":2130,\\\"red_character_consumables_box\\\":14,\\\"red_character_box\\\":1},\\\"LootTableInjectedEntryOverrides\\\":{},\\\"ownedOnlyBuyOnceProducts\\\":[\\\"free_token_box\\\"],\\\"productPurchaseTimeData\\\":{}}\"},\"dataConsent\":{\"version\":1,\"data\":\"{\\\"lastSaved\\\":\\\"2025-06-09T17:51:19.484944Z\\\",\\\"region\\\":\\\"de\\\",\\\"geoRegion\\\":\\\"de\\\",\\\"dataJobStatus\\\":0}\"},\"missedRewardsModels\":{\"version\":1,\"data\":\"{\\\"lastSaved\\\":\\\"2025-06-09T17:51:20.716964Z\\\",\\\"challenges\\\":{},\\\"admeters\\\":{},\\\"chainoffers\\\":{},\\\"citytours\\\":{}}\"},\"cityTour\":{\"version\":1,\"data\":\"{\\\"lastSaved\\\":\\\"2025-06-09T17:51:20.740989Z\\\",\\\"cityTourInstances\\\":{},\\\"completedCityTours\\\":[\\\"city_tour_1\\\"]}\"}}",
  "hash": "4d2bd1660d5428daf513c8339ee5e1a7bfabf12b",
  "updated": "2025-06-09T18:05:55.91008Z",
  "version": 2
}
```

</details>

#### Get Profile

- GET `/v2.0/profile`
- Returns the current player's profile files
- Sample request (2025-10-03): \
  GET /v2.0/profile \
  Authorization: `Bearer <identityToken>`
- Sample response:

  ```json
  {
    "profile": "{\"wallet\":{\"version\":3,...}}",
    "hash": "4d2bd1660d5428daf513c8339ee5e1a7bfabf12b",
    "updated": "2025-06-09T18:05:55.91008Z",
    "version": 2
  }
  ```

Returns the current player's profile files

When the player has never received profile data, it will return with a 404 error.

#### Get Player Profile

- GET `/v2.0/profile/<uuid>`
- Returns the given uuids player's profile files
- Sample request (2025-10-03): \
  GET /v2.0/profile/<uuid\> \
  Authorization: `Bearer <identityToken>`
- Sample response:

  ```json
  {
    "profile": "{\"wallet\":{\"version\":3,...}}",
    "hash": "4d2bd1660d5428daf513c8339ee5e1a7bfabf12b",
    "updated": "2025-06-09T18:05:55.91008Z",
    "version": 2
  }
  ```

This request returns the complete save data for a player from a uuid. \
This includes every save file.

The response will output the save data in escaped json that you can decode using this [script](./send/scripts/profile_decode.py)

When the id doesn't exist or it has never received profile data, then it will return with a 404 error.

#### Send Profile

- POST /v2.0/profile
- Send the current player's profile save files
- Request (2025-10-03): \
  POST /v2.0/profile \
  Authorization: `Bearer <identityToken>` \
  Body:

  ```json
  {
    "profile": "{\"wallet\":{\"version\":3,...}}",
    "version": 2
  }
  ```

- Response (2025-12-19):

  ```json
  { "hash": "6be3af7e1bb07f993dbf4f1bee233ddc99fdde1e" }
  ```

Notes:

- With this request you can send your escaped JSON save files. \
  The `profile` data and `version` number can be almost any values and will be accepted by the server. \
  Valid version range: -999999999 — 999999999. Values outside this range return HTTP 400. \
  The `profile` field may contain any amount of data; sending an empty string for `profile` results in a 500 error.

Request example:

```json
{
  "profile": "",
  "version": 2
}
```

Changes:

- Previously (2025-10-03) the endpoint returned the full escaped player profile together with metadata, timestamp and version:

  ```json
  {
    "profile": "{\"wallet\":{\"version\":3,\"data\":\"...\"}}",
    "hash": "4d2bd1660d5428daf513c8339ee5e1a7bfabf12b",
    "updated": "2025-06-09T18:05:55.91008Z",
    "version": 2
  }
  ```

- Current response (2025-12-19): the endpoint returns only the profile hash:

  ```json
  {
    "hash": "4d2bd1660d5428daf513c8339ee5e1a7bfabf12b"
  }
  ```

### Mail

> [!NOTE]  
> This data is from the game _Subway Surfers City_.\
> The Apis from both games are pretty much the same so it is included here.

#### Get

- POST `/v2.0/mail`
- Gets a Announcement
- Sample request (2025-01-25): \
  POST /v2.0/mail \
  Authorization: `Bearer <identityToken>` \
  Body:

  ```json
  {
    "language": "en",
    "metrics": {
      "age": "47",
      "language": "en",
      "platform": "android",
      "coppa": "false",
      "gameVersion": "1.29.1"
    }
  }
  ```

<h5>Default Response</h5>

```json
{ "mail": [] }
```

<h5>With a Announcement</h5>

```json
{
  "mail": [
    {
      "id": "f27141a8-b794-4cf8-9555-50bfac5c9b9d",
      "sender": { "uid": "1234", "name": "SYBO Games" },
      "header": "Your opinion matters!",
      "body": "We need your help making the game better by learning what's important to you! Help us fill out this survey and let us know what you think.\n\n",
      "expires": "2026-01-30T14:23:00Z",
      "metadata": [],
      "attachments": [],
      "actions": [
        {
          "type": "SurveyLink",
          "value": "https://subwaysurf.typeform.com/to/uPOujPGa",
          "metadata": []
        }
      ],
      "media": [],
      "receiver": { "uid": "019bfc8a-a7f9-79f2-995b-b1cd06b5e5ec" },
      "sent": "2026-01-26T23:18:00.783351Z",
      "read": null
    }
  ]
}
```

<h5>With a Announcement (read)</h5>

```json
{
  "mail": [
    {
      "id": "f27141a8-b794-4cf8-9555-50bfac5c9b9d",
      "sender": { "uid": "1234", "name": "SYBO Games" },
      "header": "Your opinion matters!",
      "body": "We need your help making the game better by learning what's important to you! Help us fill out this survey and let us know what you think.\n\n",
      "expires": "2026-02-24T15:12:11.864422Z",
      "metadata": [],
      "attachments": [],
      "actions": [
        {
          "type": "SurveyLink",
          "value": "https://subwaysurf.typeform.com/to/uPOujPGa",
          "metadata": []
        }
      ],
      "media": [],
      "receiver": { "uid": "019b364d-ab94-7620-bbb4-e026788dbf4a" },
      "sent": "2026-01-25T15:12:03.314419Z",
      "read": "2026-01-25T15:12:11.864422Z"
    }
  ]
}
```

#### Read

- POST `/v2.0/mail`
- Reads an Announcement
- Sample request (2025-01-25): \
  POST /v2.0/mail \
  Authorization: `Bearer <identityToken>` \
  Body:

  ```json
  {
    "id": "f27141a8-b794-4cf8-9555-50bfac5c9b9d"
  }
  ```

<h5>Default Response</h5>

`200 OK`

#### Claim

- POST `/v2.0/mail/claim`
- Claims Attached Rewards
- Sample request (2025-01-25): \
  POST /v2.0/mail/claim \
  Authorization: `Bearer <identityToken>` \
  Body:

  ```json
  {
    "id": "f27141a8-b794-4cf8-9555-50bfac5c9b9d"
  }
  ```

<h5>Default Response</h5>

`200 OK`

<h5>Mail uuid dosnt exist</h5>

```json
{ "error": "request failed", "kind": 3 }
```

### Analytics

There are many different types of events

the vendor_id is the same as in the `SYBO-Vendor-Id` in the header of all the other requests \
which changes every version.

#### Analytics Core

(3.47.0)

com.sybo.bootstrap@2.0.20 \
session_data \
bootstrap_start \
bootstrap_end \
bootstrap_step

com.sybo.analytics@1.9.10 \
user_engagement

com.sybo.ads@2.0.6 \
ad_request \
ad_loaded

com.sybo.analytics.wrapper@2.1.3 \
sdk_init

com.sybo.consent@3.2.2 \
data_resp

### Deep Links

```

https://subway-surfers.sng.link/A8yjk/diz7?_dl=subwaysurfers://&pcn=default&_p={"external_popup_request":"profile_view:{friendCode}"}

```

#### Redeem

```json
{
  "code": {
    "id": "PrideFrame2025",
    "used": 515,
    "campaignId": "PrideFrame2025"
  },
  "attachments": [{ "id": "pride_frame", "type": "ProfileFrame", "value": 1 }]
}
```

```json
{ "error": "request failed", "kind": 6 }
```

**Status codes**

`3` Already redeemed \
`4` Promocode doesn't exist \
`5` Promocode Expired

Redeem codes

PrideFrame2025 \
StPatricksDay5000 \
Istanbul_Giveaway_2024 \
VeggieHunt24_1 \
discord10

```
https://subway-surfers.sng.link/A8yjk/ucg6?_dl=subwaysurfers://&pcn=default&_p={"subway_promo_code":"{promoCode}"}
```
