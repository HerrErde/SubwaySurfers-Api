# Explanations

## Table of Contents

- [Explanations](#explanations)
  - [Table of Contents](#table-of-contents)
  - [General Notes](#general-notes)
  - [Json](#json)
    - [Register](#register)
    - [Refresh](#refresh)
    - [Manifest](#manifest)
    - [Gamedata](#gamedata)
    - [Media](#media)
    - [Assets](#assets)
    - [GDPR status](#gdpr-status)
    - [GDPR delete](#gdpr-delete)
    - [Get Challenge](#get-challenge)
    - [Sent Challenge](#sent-challenge)
    - [Send Tournament](#send-tournament)
    - [Get Tournament](#get-tournament)
    - [Profile](#profile)
      - [User Profile](#user-profile)
      - [Send Profile](#send-profile)
      - [Get Profile](#get-profile)
    - [Analytics](#analytics)
      - [Analytics Core](#analytics-core)
    - [Deep Links](#deep-links)
      - [Redeem](#redeem)

## General Notes

All knowledge is for versions `3.52.0`

> [!WARNING]
> Changes are expected to happen

After registering an account, you'll have to create a player to use all the requests; otherwise, the account is 'empty' and can't perform player actions

You can only add abtesting to the account after adding crosspromo. This must be done in that order, else it will result in an error.

this is a player tag `BY1BJH84CVHHIX` \
this is a player uuid `0197351b-ae06-7a3f-8576-0e3d5b95a280`

Some response bodies that contain repeating data or with minor changes will be truncated to avoid repetition.

## Json

### Register

This will create a "empty" account that only creates a user with which you populate with a player \
It generates a idenity and a refresh token, with a ttl (time to live)

```json
{
  "idToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMTk2OGMzYS0zZmVhLTdhYmMtODk3Yy1lMWExO...",
  "idTokenTtl": 604800,
  "refreshToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMTk2NzJiOS0yZThiLTc0NWEtOWQ1My1lMzg4MT...",
  "user": { "id": "01968c3a-3fea-7abc-897c-e1a1814ba489", "links": [] }
}
```

### Refresh

The Refresh request is used to refresh the Accounts identity token, and continue using the account after ttl.

It will return the same json as the register response

### Manifest

From the Manifest you get the version specific version data \
You get the secret by extracting it from the game file (apk or ipa) \
In the `assets/settings/sybo.tower.default.json` (ipa is `Payload/SubwaySurf.app/Data/Raw/settings/sybo.tower.default.json`) file contains a key `Secret` with the version specific secret.

For specific experiments you can set `ab_google_play`, `ab_revive_codechange`

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
https://manifest.tower.sybo.net/v1.0/{game}/{version}/{platform}/{secretToken}/manifest.json
```

_Experiment Schema_

```
https://manifest.tower.sybo.net/v1.0/{game}/{version}/{platform}/{secretToken}/{experiment}/manifest.json
```

When using the v2.0 schema, you can use the `archive` endpoint to get a zip of the game files. \
It seems like the v2.0 schmea has only the `archive` endpoint, all other do not exist

```
https://manifest.tower.sybo.net/v2.0/subway/3.49.1/android/junpNkV78FJxO4dlGAbO/archive.zip
```

```
manifest.json
data/
   boards.json
   calendars.json
   ...
```

### Gamedata

You can get the gamedata/tower files in bypass of the old depreciated method of extracting the apk gamefile or ipa gamefile (ipa still works), using from the manifest request contained `gamedata` hash value
(state 3.48.5)

You can request the `manifest.json`, which contains the manifest of all the existing files in gamedata.

```json
{"experiment":"default","game":"subway","objects":{"achievements":{"filename":"achievements.json","key":"2bed33daedf13ae310d90edff852600598e665e3"},"adplacements":{"filename":"adplacements.json","key":"2010b70022bba2451310a6e60166a4b31f21fe0b"},"assemblyevents":{"filename":"assemblyevents.json","key":"4fa66108ddd7f8bead20b40f6a8b505a9cdf098f"}truncated...},"spec":"v1.0","version":"3.46.0"}
```

```
https://gamedata.tower.sybo.net/v1.0/subway/c84ca921a6249f9fa201444ed03f54238e8aaaa2/manifest.json
```

```
https://gamedata.tower.sybo.net/v1.0/{game}/{gamedataSecret}/{filename}.json
```

### Media

```
https://media.sybo.net/{game}/cross_promotion/{promotion}/Image/{image}
```

known game promotions \
`ssmatch`, `ssblast`, `brim`, `external`

### Assets

This request will return the asset in the UnityFs format

```
http://assets.tower.sybo.net/v1.0/{game}/{bundleId}
```

It can have the User Agent `UnityPlayer/2022.3.24f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)`

Inside the `assets/aa/catalog.json` file, under the `m_InternalIds` list, you’ll find all the file entries. These are links starting with `sybo://`, such as:

`sybo://9917a9a0-0de9-40fb-bb80-392ee596f705/bundle/1.0.0/characters-remote_assets_pixeljake_default_outfit_config_7a3d5cbdbef0e42b386ceea8f110c324.bundle`

These entries reference the actual asset bundles used by the game.

### GDPR status

This is the account delete status request, with wich you get the status of the current account delete request.

```json
{
  "job": {
    "kind": 1,
    "state": 0,
    "url": "",
    "createdAt": "2025-05-22T05:14:26.561428058Z",
    "endedAt": null
  }
}
```

### GDPR delete

This is the account deletion request that will delete your account.

It only deletes your public profile (that was is shown when other players look at your player) not your save data \
when you are friends with a player you are removed from their friends list

it will only delete your `player` but not your `account`, that means you can just use `CreatePlayer` request again without the need of registering again.

```json
{
  "job": {
    "kind": 1,
    "state": 1,
    "url": "",
    "createdAt": "2025-05-22T05:14:26.561428Z",
    "endedAt": "2025-05-22T05:14:27.189561Z"
  }
}
```

### Get Challenge

<details>
<summary>Request details</summary>

`GET`

```
/v2.0/challenge/{challenge}_{c}/group
```

challenge like `daily_challenge_en`, `staged_tta_en`

the country code has to be the same as in the [send](#sent-challenge) request as `matchmakingId` value

</details>

<details>

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
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "default_frame" },
          { "key": "portrait", "value": "jake_portrait" },
          { "key": "character", "value": "tricky.default" },
          { "key": "board", "value": "default" },
          { "key": "score", "value": "44333" }
        ]
      },
      {
        "uid": "01961538-d5d2-74f3-953a-d4e13fdffa51",
        "matchmakingValue": 16,
        "name": "",
        "picture": "",
        "socialIds": [],
        "metadata": [
          { "key": "background", "value": "default_background" },
          { "key": "frame", "value": "default_frame" },
          { "key": "portrait", "value": "missmaia_illustration_portrait" },
          { "key": "character", "value": "jake.darkOutfit" },
          { "key": "board", "value": "fanTastic" },
          { "key": "score", "value": "170558" }
        ]
      },
      truncated 7x
    ]
  }
}
```

</details>

### Sent Challenge

<details>
<summary>Request details</summary>

`POST`

```
/v2.0/challenge/group
```

```json
{
  "matchmakingStartValue": ...,
  "gamedataHash": ...,
  "challengeID": ...,
  "matchmakingId": ...
}
```

</details>
    
This request is made when opening the view of a challenge in the Events tab

It is not known from what the `matchmakingStartValue` is from

<details>

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
      truncated 7x
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

**Already send request**

```json
{ "error": "request failed", "kind": 6 }
```

When setting the challengeID to `daily_challenge_nl`, you can only use the get_challenge request with the challenge group for that country, here `nl`

### Send Tournament

<details>

```json
{
   "group":{
      "week":24,
      "start":"2025-06-09T10:00:00Z",
      "end":"2025-06-16T10:00:00Z",
      "tournamentId":"nl",
      "brackets":{
         "current":{
            "matchmaking":{
               "groupSize":20,
               "bracketMaxUsers":{
                  "champion":1
               },
               "bracketSort":{
                  "bronze":1,
                  "diamond":4,
                  "gold":3,
                  "none":0,
                  "silver":2
               },
               "bracketPercentage":{
                  "bronze":0.2,
                  "diamond":0.02,
                  "gold":0.05,
                  "none":0.63,
                  "silver":0.1
               },
               "bracketDistribution":{
                  "bronze":{
                     "bronze":8,
                     "diamond":1,
                     "gold":3,
                     "none":3,
                     "silver":4
                  },
                  "diamond":{
                     "bronze":2,
                     "diamond":8,
                     "gold":6,
                     "none":0,
                     "silver":3
                  },
                  "gold":{
                     "bronze":2,
                     "diamond":4,
                     "gold":7,
                     "none":1,
                     "silver":5
                  },
                  "none":{
                     "bronze":5,
                     "diamond":1,
                     "gold":2,
                     "none":8,
                     "silver":3
                  },
                  "silver":{
                     "bronze":4,
                     "diamond":2,
                     "gold":4,
                     "none":2,
                     "silver":7
                  }
               }
            },
            "bounds":{
               "bronze":1508838,
               "diamond":11889620,
               "gold":6368082,
               "none":14728,
               "silver":3087864
            }
         },
         "past":{
            "matchmaking":{
               "groupSize":20,
               "bracketMaxUsers":{},
               "bracketSort":{
                  "bronze":1,
                  "diamond":4,
                  "gold":3,
                  "none":0,
                  "silver":2
               },
               "bracketPercentage":{
                  "bronze":0.2,
                  "diamond":0.02,
                  "gold":0.05,
                  "none":0.63,
                  "silver":0.1
               },
               "bracketDistribution":{
                  "bronze":{
                     "bronze":8,
                     "diamond":1,
                     "gold":3,
                     "none":3,
                     "silver":4
                  },
                  "diamond":{
                     "bronze":2,
                     "diamond":8,
                     "gold":6,
                     "none":0,
                     "silver":3
                  },
                  "gold":{
                     "bronze":2,
                     "diamond":4,
                     "gold":7,
                     "none":1,
                     "silver":5
                  },
                  "none":{
                     "bronze":5,
                     "diamond":1,
                     "gold":2,
                     "none":8,
                     "silver":3
                  },
                  "silver":{
                     "bronze":4,
                     "diamond":2,
                     "gold":4,
                     "none":2,
                     "silver":7
                  }
               }
            },
            "bounds":{
               "bronze":814870,
               "diamond":11364990,
               "gold":5607162,
               "none":3,
               "silver":2876725
            }
         }
      },
      "players":[
         {
            "uid":"019718f5-d1aa-7443-a8e2-26ebaf3d891e",
            "scores":{
               "current":1292646,
               "past":2045888
            },
            "socialIds":[],
            "metadata":[
               {
                  "key":"board",
                  "value":"monster"
               },
               {
                  "key":"score",
                  "value":"1292646"
               },
               {
                  "key":"background",
                  "value":"default_background"
               },
               {
                  "key":"frame",
                  "value":"default_frame"
               },
               {
                  "key":"portrait",
                  "value":"boombot_portrait"
               },
               {
                  "key":"character",
                  "value":"boombot.default"
               }
            ],
            "name":"",
            "picture":""
         },
         {
            "uid":"01974516-0105-7c57-b9e2-b91865bf206d",
            "scores":{
               "current":35062,
               "past":0
            },
            "socialIds":[],
            "metadata":[
               {
                  "key":"score",
                  "value":"35062"
               },
               {
                  "key":"background",
                  "value":"default_background"
               },
               {
                  "key":"frame",
                  "value":"default_frame"
               },
               {
                  "key":"portrait",
                  "value":"jake_portrait"
               },
               {
                  "key":"character",
                  "value":"jake.darkOutfit"
               },
               {
                  "key":"board",
                  "value":"starboard"
               }
            ],
            "name":"",
            "picture":""
         },
         {
            "uid":"8899c41a-1ba2-413c-b1ce-fe82e5597588",
            "scores":{
               "current":1257032,
               "past":0
            },
            "socialIds":[],
            "metadata":[
               {
                  "key":"portrait",
                  "value":"fresh_graffiti_portrait"
               },
               {
                  "key":"character",
                  "value":"finn.default"
               },
               {
                  "key":"board",
                  "value":"superhero"
               },
               {
                  "key":"score",
                  "value":"1257032"
               },
               {
                  "key":"background",
                  "value":"default_background"
               },
               {
                  "key":"frame",
                  "value":"default_frame"
               }
            ],
            "name":"",
            "picture":""
         },
         {
            "uid":"01952c98-1754-7e58-a63f-78e3f1574b0c",
            "scores":{
               "current":73016,
               "past":0
            },
            "socialIds":[],
            "metadata":[
               {
                  "key":"portrait",
                  "value":"tagbot_portrait"
               },
               {
                  "key":"character",
                  "value":"frank.clownOutfit"
               },
               {
                  "key":"board",
                  "value":"starboard"
               },
               {
                  "key":"score",
                  "value":"73016"
               },
               {
                  "key":"background",
                  "value":"default_background"
               },
               {
                  "key":"frame",
                  "value":"default_frame"
               }
            ],
            "name":"",
            "picture":""
         },
         {
            "uid":"8680a2cd-b59b-4852-984f-f1938d4a8608",
            "scores":{
               "current":1119541,
               "past":0
            },
            "socialIds":[],
            "metadata":[
               {
                  "key":"background",
                  "value":"default_background"
               },
               {
                  "key":"frame",
                  "value":"default_frame"
               },
               {
                  "key":"portrait",
                  "value":"alexandre_stanoutfit_portrait"
               },
               {
                  "key":"character",
                  "value":"diego.default"
               },
               {
                  "key":"board",
                  "value":"trickster"
               },
               {
                  "key":"score",
                  "value":"1119541"
               }
            ],
            "name":"",
            "picture":""
         },
         {
            "uid":"0197593c-8e07-70e4-bbab-9527aff30be1",
            "scores":{
               "current":0,
               "past":0
            },
            "socialIds":[],
            "metadata":[],
            "name":"",
            "picture":""
         }
      ]
   }
}
```

</details>

### Get Tournament

<details>

```json
{
   "group":{
      "week":24,
      "start":"2025-06-09T10:00:00Z",
      "end":"2025-06-16T10:00:00Z",
      "tournamentId":"de",
      "brackets":{
         "current":{
            "matchmaking":{
               "groupSize":20,
               "bracketMaxUsers":{
                  "champion":1
               },
               "bracketSort":{
                  "bronze":1,
                  "diamond":4,
                  "gold":3,
                  "none":0,
                  "silver":2
               },
               "bracketPercentage":{
                  "bronze":0.2,
                  "diamond":0.02,
                  "gold":0.05,
                  "none":0.63,
                  "silver":0.1
               },
               "bracketDistribution":{
                  "bronze":{
                     "bronze":8,
                     "diamond":1,
                     "gold":3,
                     "none":3,
                     "silver":4
                  },
                  "diamond":{
                     "bronze":2,
                     "diamond":8,
                     "gold":6,
                     "none":0,
                     "silver":3
                  },
                  "gold":{
                     "bronze":2,
                     "diamond":4,
                     "gold":7,
                     "none":1,
                     "silver":5
                  },
                  "none":{
                     "bronze":5,
                     "diamond":1,
                     "gold":2,
                     "none":8,
                     "silver":3
                  },
                  "silver":{
                     "bronze":4,
                     "diamond":2,
                     "gold":4,
                     "none":2,
                     "silver":7
                  }
               }
            },
            "bounds":{
               "bronze":1370621,
               "diamond":10386575,
               "gold":5511561,
               "none":2,
               "silver":3013690
            }
         },
         "past":{
            "matchmaking":{
               "groupSize":20,
               "bracketMaxUsers":{
               },
               "bracketSort":{
                  "bronze":1,
                  "diamond":4,
                  "gold":3,
                  "none":0,
                  "silver":2
               },
               "bracketPercentage":{
                  "bronze":0.2,
                  "diamond":0.02,
                  "gold":0.05,
                  "none":0.63,
                  "silver":0.1
               },
               "bracketDistribution":{
                  "bronze":{
                     "bronze":8,
                     "diamond":1,
                     "gold":3,
                     "none":3,
                     "silver":4
                  },
                  "diamond":{
                     "bronze":2,
                     "diamond":8,
                     "gold":6,
                     "none":0,
                     "silver":3
                  },
                  "gold":{
                     "bronze":2,
                     "diamond":4,
                     "gold":7,
                     "none":1,
                     "silver":5
                  },
                  "none":{
                     "bronze":5,
                     "diamond":1,
                     "gold":2,
                     "none":8,
                     "silver":3
                  },
                  "silver":{
                     "bronze":4,
                     "diamond":2,
                     "gold":4,
                     "none":2,
                     "silver":7
                  }
               }
            },
            "bounds":{
               "bronze":984764,
               "diamond":11652184,
               "gold":5610007,
               "none":1,
               "silver":2949876
            }
         }
      },
      "players":[
         {
            "uid":"d57d8759-f28e-4869-870f-4d288ddaff83",
            "scores":{
               "current":1279904,
               "past":10529983
            },
            "socialIds":[
            ],
            "metadata":[
               {
                  "key":"board",
                  "value":"glitterBlaster"
               },
               {
                  "key":"score",
                  "value":"1279904"
               },
               {
                  "key":"background",
                  "value":"default_background"
               },
               {
                  "key":"frame",
                  "value":"lava_frame"
               },
               {
                  "key":"portrait",
                  "value":"berta_illustration_portrait"
               },
               {
                  "key":"character",
                  "value":"riley.default"
               }
            ],
            "name":"",
            "picture":""
         },
         {
            "uid":"4f1f4146-9490-4e13-a638-aeff55ca12cf",
            "scores":{
               "current":585159,
               "past":3123567
            },
            "socialIds":[
            ],
            "metadata":[
               {
                  "key":"background",
                  "value":"default_background"
               },
               {
                  "key":"frame",
                  "value":"default_frame"
               },
               {
                  "key":"portrait",
                  "value":"dog_graffiti_portrait"
               },
               {
                  "key":"character",
                  "value":"tricky.default"
               },
               {
                  "key":"board",
                  "value":"smokingSlime"
               },
               {
                  "key":"score",
                  "value":"585159"
               }
            ],
            "name":"",
            "picture":""
         },
         {
            "uid":"8debc9f5-0ce1-42a9-8e7d-e0fc1bc1da2e",
            "scores":{
               "current":7375622,
               "past":7786878
            },
            "socialIds":[
            ],
            "metadata":[
               {
                  "key":"background",
                  "value":"default_background"
               },
               {
                  "key":"frame",
                  "value":"lava_frame"
               },
               {
                  "key":"portrait",
                  "value":"fresh_graffiti_portrait"
               },
               {
                  "key":"character",
                  "value":"bertaSummerEleganzaOutfit.default"
               },
               {
                  "key":"board",
                  "value":"bloomster"
               },
               {
                  "key":"score",
                  "value":"7375622"
               }
            ],
            "name":"",
            "picture":""
         },
         {
            "uid":"0197556e-508c-74d6-a267-c1e8585c5b44",
            "scores":{
               "current":62120,
               "past":0
            },
            "socialIds":[],
            "metadata":[
               {
                  "key":"score",
                  "value":"62120"
               },
               {
                  "key":"background",
                  "value":"default_background"
               },
               {
                  "key":"frame",
                  "value":"default_frame"
               },
               {
                  "key":"portrait",
                  "value":"tagbot_portrait"
               },
               {
                  "key":"character",
                  "value":"jake.default"
               },
               {
                  "key":"board",
                  "value":"default"
               }
            ],
            "name":"",
            "picture":""
         },
         {
            "uid":"796907fb-c0fc-470a-a9b4-a1286562efa5",
            "scores":{
               "current":210569,
               "past":1838165
            },
            "socialIds":[],
            "metadata":[
               {
                  "key":"background",
                  "value":"default_background"
               },
               {
                  "key":"frame",
                  "value":"default_frame"
               },
               {
                  "key":"portrait",
                  "value":"jake_portrait"
               },
               {
                  "key":"character",
                  "value":"kareem.default"
               },
               {
                  "key":"board",
                  "value":"scarab"
               },
               {
                  "key":"score",
                  "value":"210569"
               }
            ],
            "name":"",
            "picture":""
         },
         {
            "uid":"0197590d-94b8-7955-a4f1-fd080532fcdf",
            "scores":{
               "current":0,
               "past":0
            },
            "socialIds":[],
            "metadata":"None",
            "name":"",
            "picture":""
         }
      ]
   }
}
```

</details>

### Profile

#### User Profile

This request returns the complete save data for a player from a uuid. \
This includes every save file.

The response will output the save data in escaped json that you can decode using this [script](./send/scripts/profile_decode.py)

When the id doesn't exist then it will return with a 404 error.

**truncated version with only wallet, dataConsent, missedRewardsModels**

<details>

```json
{
  "profile": "{\"wallet\":{\"version\":3,\"data\":\"{\\\"lastSaved\\\":\\\"2025-06-09T18:05:55.133242Z\\\",\\\"currencies\\\":{\\\"3\\\":{\\\"value\\\":278,\\\"expirationType\\\":0},\\\"2\\\":{\\\"value\\\":953,\\\"expirationType\\\":0},\\\"4\\\":{\\\"value\\\":184,\\\"expirationType\\\":0},\\\"5\\\":{\\\"value\\\":270,\\\"expirationType\\\":0},\\\"1\\\":{\\\"value\\\":945994,\\\"expirationType\\\":0},\\\"lootboxQueue\\\":{\\\"unopenedLootboxes\\\":[]},\\\"currencyAllowedInRun\\\":{\\\"5\\\":true,\\\"4\\\":true},\\\"lootBoxesOpened\\\":{\\\"mini_mystery_box\\\":2515,\\\"mystery_box\\\":4786,\\\"token_box\\\":7,\\\"super_mystery_box\\\":2130,\\\"red_character_consumables_box\\\":14,\\\"red_character_box\\\":1},\\\"LootTableInjectedEntryOverrides\\\":{},\\\"ownedOnlyBuyOnceProducts\\\":[\\\"free_token_box\\\"],\\\"productPurchaseTimeData\\\":{}}\"},\"dataConsent\":{\"version\":1,\"data\":\"{\\\"lastSaved\\\":\\\"2025-06-09T17:51:19.484944Z\\\",\\\"region\\\":\\\"de\\\",\\\"geoRegion\\\":\\\"de\\\",\\\"dataJobStatus\\\":0}\"},\"missedRewardsModels\":{\"version\":1,\"data\":\"{\\\"lastSaved\\\":\\\"2025-06-09T17:51:20.716964Z\\\",\\\"challenges\\\":{},\\\"admeters\\\":{},\\\"chainoffers\\\":{},\\\"citytours\\\":{}}\"},\"cityTour\":{\"version\":1,\"data\":\"{\\\"lastSaved\\\":\\\"2025-06-09T17:51:20.740989Z\\\",\\\"cityTourInstances\\\":{},\\\"completedCityTours\\\":[\\\"city_tour_1\\\"]}\"}}",
  "hash": "4d2bd1660d5428daf513c8339ee5e1a7bfabf12b",
  "updated": "2025-06-09T18:05:55.91008Z",
  "version": 2
}
```

</details>

#### Send Profile

With this request you can send your escaped json save files. \
The profile data and version number can be anything and will get accepted.

Version value: \
`-999999999` - `999999999` values below or above the provided number range will result in a 400 error.

The profile data can have any amount of data, a empty string results in a 500 error.

The "profile" value is the same as the escaped json dict above.

```json
{
  "profile": "",
  "version": 2
}
```

#### Get Profile

This request returns the complete save data for the own player.

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

3. Already redeemed
4. Promocode doesn't exist
5. Promocode Expired

Redeem codes

PrideFrame2025 \
StPatricksDay5000 \
Istanbul_Giveaway_2024 \
VeggieHunt24_1 \
discord10

```
https://subway-surfers.sng.link/A8yjk/ucg6?_dl=subwaysurfers://&pcn=default&_p={"subway_promo_code":"{promoCode}"}
```
