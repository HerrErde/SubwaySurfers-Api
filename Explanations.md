# Explanations

## Table of Contents

- [Explanations](#explanations)
  - [Table of Contents](#table-of-contents)
  - [General Notes](#general-notes)
    - [Expired identityToken](#expired-identitytoken)
    - [Protobuf Bodies](#protobuf-bodies)
    - [Identity File](#identity-file)
  - [RPC](#rpc)
    - [Friend Action](#friend-action)
      - [Get invites](#get-invites)
      - [Get FriendsAndInvites](#get-friendsandinvites)
      - [Sending Friend Request](#sending-friend-request)
      - [Cancel Friend Request](#cancel-friend-request)
      - [Get Relationship](#get-relationship)
    - [Get Player](#get-player)
      - [Get Player Data](#get-player-data)
      - [Get Player by Tag](#get-player-by-tag)
      - [Get Player by Id](#get-player-by-id)
      - [Get Wallet](#get-wallet)
    - [Update Player](#update-player)
      - [Inputs](#inputs)
      - [Name](#name)
      - [Badges](#badges)
    - [Energy](#energy)
      - [Init Energy](#init-energy)
      - [Get Energies](#get-energies)
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
    - [profile](#profile)
    - [Analytics](#analytics)
      - [Analytics Core](#analytics-core)
    - [Deep Links](#deep-links)
      - [Redeem](#redeem)
  - [Other](#other)
    - [Profile](#profile-1)

## General Notes

All knowledge is for versions `3.48.5`

> [!WARNING]
> Changes are expected to happen

grpc-status-details-bin content is base64

After registering an account, you'll have to create a player to use all the requests; otherwise, the account is 'empty' and can't perform player actions

You can only add abtesting to the account after adding crosspromo. This must be done in that order, else it will result in an error.

All time values are in epoch time

this is a player tag `BY1BJH84CVHHIX` \
this is a player uuid `0197351b-ae06-7a3f-8576-0e3d5b95a280`

sec means seconds \
nsec means nanoseconds

Some response bodies that contain repeating data or with minor changes will be truncated to avoid repetition.

### Expired identityToken

When refreshing a identity token but still making requests with the old token, it will seem to work just fine, but e.g. your game (with the now new refreshed token) will have no changes (send invite will only appear on the player with the token, not the new one). \
Make sure to keep your identityToken refreshed and the everywhere the same.

### Protobuf Bodies

<details>
  <summary>PlayerResponse</summary>

```
user_data {
  name: "StylingDino"
  tag: "BY1BJH84CVHHIX"
  level: 1
  highscore: 1
  metadata {
    key: "stat_total_visited_destinations"
    value: "1"
  }
  metadata {
    key: "stat_total_top_run_medals_silver"
    value: "1"
  }
  metadata {
    key: "stat_total_top_run_medals_gold"
    value: "1"
  }
  metadata {
    key: "stat_total_top_run_medals_diamond"
    value: "1"
  }
  metadata {
    key: "stat_total_top_run_medals_champion"
    value: "1"
  }
  metadata {
    key: "stat_total_top_run_medals_bronze"
    value: "1"
  }
  metadata {
    key: "stat_total_games"
    value: "1"
  }
  metadata {
    key: "stat_owned_characters"
    value: "1"
  }
  metadata {
    key: "stat_owned_characters_outfits"
    value: "1"
  }
  metadata {
    key: "stat_owned_boards"
    value: "1"
  }
  metadata {
    key: "stat_owned_boards_upgrades"
    value: "1"
  }
  metadata {
    key: "stat_achievements"
    value: "1"
  }
  metadata {
    key: "selected_portrait"
    value: "boombox_graffiti_portrait"
  }
  metadata {
    key: "selected_frame"
    value: "jake_portrait"
  }
  metadata {
    key: "selected_country"
    value: "de"
  }
  metadata {
    key: "selected_character"
    value: "jake.default"
  }
  metadata {
    key: "selected_board"
    value: "default"
  }
  metadata {
    key: "selected_board_upgrades"
    value: "default,trail"
  }
  metadata {
    key: "selected_background"
    value: "default_background"
  }
  metadata {
    key: "highscore_default"
    value: "1"
  }
  metadata {
    key: "equipped_badge_1"
    value: ""
  }
  metadata {
    key: "equipped_badge_2"
    value: ""
  }
  metadata {
    key: "equipped_badge_3"
    value: ""
  }
  metadata {
    key: "equipped_badge_4"
    value: ""
  }
  metadata {
    key: "equipped_badge_tier_1"
    value: "0"
  }
  metadata {
    key: "equipped_badge_tier_2"
    value: "0"
  }
  metadata {
    key: "equipped_badge_tier_3"
    value: "0"
  }
  metadata {
    key: "equipped_badge_tier_4"
    value: "0"
  }
  created_at {
    sec: 1748942697
    nsec: 178738000
  }
  update_player_at {
    sec: 1748945058
    nsec: 90790000
  }
  name_changed_at {
    sec: 1748945058
    nsec: 89156000
  }
  uuid: "0197351b-ae06-7a3f-8576-0e3d5b95a280"
  name_change_expires_at {
    sec: 1749549858
    nsec: 89156000
  }
}
```

</details>

<details>
  <summary>Quota</summary>

```
quota  {
  max_friends: 100
  friend_count: 1
  received_invite_count: 1
  send_invite_count: 1
  max_invites: 10
}
```

</details>

### Identity File

The identity file contains a dictionary with the user dict which contains id, name, picture, links list
and a refresh and identityToken dict that both contain a `token` value. \
A `expiresAt` value will tell the app when to refresh the token is expired.

All tokens are have 7 days ttl (time to live)

```json
{
  "user": {
    "id": "01968c3a-3fea-7abc-897c-e1a1814ba489",
    "name": null,
    "picture": null,
    "links": []
  },
  "refreshToken": {
    "token": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMTk2OGMzYS0zZmVhLTdhYmMtODk3Yy1lMWExO..."
  },
  "identityToken": {
    "token": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMTk2NzJiOS0yZThiLTc0NWEtOWQ1My1lMzg4MT...",
    "expiresAt": "2025-05-08T14:22:29.8031690Z"
  }
}
```

jwt (striped signatures)

Identity token

```json
{"alg":"PS256","typ":"JWT"}
{"sub":"019672b9-2e8b-745a-9d53-e3881534096c","iat":1745681460,"exp":1746286260}
```

refresh token

```json
{
  "sub": "01968c3a-3fea-7abc-897c-e1a1814ba489",
  "iat": 1746109349,
  "key": "44iuWfCHuem59orhD8RcZx4d6wmj2Zn3fvcpJ94lkFNqQfbrWequH364G8JUYfhN"
}
```

## RPC

### Friend Action

The max amount of Friends a User can have is 100 Friends.

A user can't have more than 10 friend requests at the same time. \
After limit has been reached, new friend requests will not be successful.

A user can send max 100 invites to other players. \
The amount of invites you can send to players is bound to the amount of friends you have. \
100 = Friends + Send Invites \
That means when you have 75 Friends ₘᵣ. ₚₒₚᵤₗₐᵣ... you can only send another 25 invites to players

A user's friend invite rate limit, is 2 accepted invites per user per 24 hours. \
e.g. you can send a friend request to User A, they decline, then repeat a second time.
On the third request you'll likely need to wait around 24 hours before being able to send a third invite to the same player. \
You will still be able to send 2 friend requests to User B.

#### Get invites

When requesting the list of received invites, you get a list of `invite` bodies with each body having an `action_uuid` with which you control actions like accept, reject and so on.
The `user_uuid` that got the invite (your own), and a `PlayerResponse` body which contains the whole player metadata with uuid, and player details (game stats, collectables) and the `quota` with `max_friends`, `max_invites`, friend_count and `received_invite_count`

<details>

```
received_invites {
  action_uuid: "01972f8a-5024-7218-bb95-73583e92edb8"
  user_uuid {
    uuid: "01972f81-3f5b-73ec-99ea-fa9c481ff4a6"
  }
  user_info {
    uuid: "01972f8a-4c30-723d-8d67-0ee30cf56335"
    user_data {
      name: "FunnyPins"
      tag: "7VY5K26493SHYG"
      level: 4
      highscore: 4622
      metadata {
        key: "stat_total_visited_destinations"
        value: "14"
      }
      truncated metadata...
      created_at {
        sec: 1748849282
        nsec: 424557000
      }
      update_player_at {
        sec: 1748849282
        nsec: 687280000
      }
      uuid: "01972f8a-4c30-723d-8d67-0ee30cf56335"
      name_change_expires_at {
        sec: 1749052404
        nsec: 666831000
      }
    }
  }
  invited_at {
    sec: 1748849283
    nsec: 105022000
  }
}
quota  {
  max_friends: 100
  friend_count: 1
  received_invite_count: 1
  max_invites: 10
}
```

</details>

<details>

```
sent_invites {
  action_uuid: "0197590f-df48-7105-b384-4a0c20be6a3e"
  user_info {
    uuid: "0197554e-7bd0-7061-818a-32f59e3254f5"
    user_data {
      name: "YoungIzzy"
      tag: "5SVU2KM3UPCUH7"
      level: 1
      highscore: 395
      metadata {
        key: "stat_total_visited_destinations"
        value: "1"
      }
      metadata {
        key: "stat_total_games"
        value: "1"
      }
      metadata {
        key: "stat_owned_characters"
        value: "1"
      }
      metadata {
        key: "stat_owned_boards"
        value: "1"
      }
      metadata {
        key: "selected_portrait"
        value: "jake_portrait"
      }
      metadata {
        key: "selected_frame"
        value: "default_frame"
      }
      metadata {
        key: "selected_country"
        value: "de"
      }
      metadata {
        key: "selected_character"
        value: "jake.default"
      }
      metadata {
        key: "selected_board"
        value: "default"
      }
      metadata {
        key: "selected_board_upgrades"
        value: "default"
      }
      metadata {
        key: "selected_background"
        value: "default_background"
      }
      metadata {
        key: "highscore_default"
        value: "395"
      }
      created_at {
        sec: 1749544255
        nsec: 228563000
      }
      update_player_at {
        sec: 1749544255
        nsec: 228563000
      }
      uuid: "0197554e-7bd0-7061-818a-32f59e3254f5"
    }
  }
  user_uuid {
    uuid: "0197590d-94b8-7955-a4f1-fd080532fcdf"
  }
  invited_at {
    sec: 1749545901
    nsec: 893330000
  }
}
quota {
  max_friends: 100
  max_invites: 10
}

```

</details>

When the invites list is empty, it will only show the quota

<details>

```
quota  {
  max_friends: 100
  friend_count: 1
  received_invite_count: 1
  max_invites: 10
}
```

</details>

#### Get FriendsAndInvites

This will get you, you guessed right, your Friends AND Invites

```
quota  {
  max_friends: 100
  friend_count: 1
  received_invite_count: 1
  send_invite_count: 1
  max_invites: 10
}
```

Even when not send or not received an invite, the data will still show, but empty, except your own uuid.

```
  received_uuid {
    user_uuid: "0197a0a6-9373-7e8c-b74b-6c55ebc1106b"
  }
```

#### Sending Friend Request

When sending a friends request to a user it will show the `action_uuid`, the truncated inviter userinfo (without metadata details) and invited user info

<details>

```
userinvite {
  action_uuid: "01972f9b-2f74-74fb-9625-6759350ee44c"
  invited {
    uuid: "01972f81-3f5b-73ec-99ea-fa9c481ff4a6"
    user_data {
      name: "CoolNikos"
      tag: "5NWP2S8G5AP5ZU"
      created_at {
        sec: 1748848690
        nsec: 190112000
      }
      update_player_at {
        sec: 1748848690
        nsec: 190112000
      }
      uuid: "01972f81-3f5b-73ec-99ea-fa9c481ff4a6"
    }
  }
  inviter {
    uuid: "01972f99-79aa-7149-9561-706998e2c455"
    user_data {
      name: "CoolNikos"
      tag: "115ULUMIQLQX45"
      created_at {
        sec: 1748850277
        nsec: 993517000
      }
      update_player_at {
        sec: 1748850277
        nsec: 993517000
      }
      uuid: "01972f99-79aa-7149-9561-706998e2c455"
    }
  }
  invited_at {
    sec: 1748850388
    nsec: 849272000
  }
}
```

</details>

#### Cancel Friend Request

To cancel a send pending friend request, use the `action_uuid` from the invite or the invites list response. This `action_uuid` is unique for each player and friend request, and cannot be replaced by the original player UUID.

#### Get Relationship

`GetRelationship` returns the relationship status between the user and another player:

Status Codes:

1. The player is a friend
2. The other player has sent a friend request to the user
3. The user has sent a friend request to the other player
4. No friend relationship exists

The relationship status

```
status {
  status: 2
}
```

### Get Player

#### Get Player Data

This will get data of the own player \
It will just return the `PlayerResponse` body

The fields do not show up directly after generating the Player \
All metadata fields will not exist until they are set with UpdatePlayer

Additionally, the `update_player_at`, `name_change_expires_at` and`name_changed_at` only show when the name is changed from the name the player was created with to a new one.

#### Get Player by Tag

This gets a player by their invite Tag \
It returns the `PlayerResponse` body

#### Get Player by Id

This gets a player by their uuid \
It returns the `PlayerResponse` body

to get the data from a player via their uuid
you need first the uuid of the player which you can get via the tag (invite id) or your own from the auth/subway-prod/identity file, the `id` field

It is not possible to get the data via a `action_uuid`, it will result in an error

#### Get Wallet

The Get Wallet request outputs the time the wallet was last updated (probably)

```
walletdata {
  wallet_last_save_at {
    sec: 1748426414
    nsec: 222099082
  }
}
```

### Update Player

Update fields

Get all valid values [HerrErde/subway-source](https://github.com/HerrErde/subway-source)

| Id | Type | Limit | Special |
|---|---|---|---|
| name | string | 2-15 characters, only alphabet letters, no numeric | 604800 seconds (7 days) regex: `^[a-zA-Z]+$` |
| level | int | 100 |  |
| highscore | int | 2147483646 | 2147483647 is the int32 limit, also just -1 |
| stat_total_visited_destinations | int | 49 characters |  |
| stat_total_games | int | 49 characters | Once set, [this value should only be increased](#stat_total_games_error) for details |
| stat_owned_characters | int | 49 characters |  |
| stat_owned_characters_outfits | int | 49 characters |  |
| stat_owned_boards | int | 49 characters |  |
| stat_owned_boards_upgrades | int | 49 characters |  |
| selected_portrait | string | 49 characters |  |
| selected_frame | string | 49 characters |  |
| selected_country | string | 49 characters | Only ISO 3166-1 alpha-2 codes (e.g., de, en, nl). Using other values (e.g., `test`) will display `countries.test.name` ([country_iso.txt](./country_iso.txt)) |
| selected_character | string | 49 characters | Must follow the format `character.Outfit` (e.g., `jake.darkOutfit`) |
| selected_board_upgrades | string | 49 characters | Comma-separated list of upgrades (e.g., "default,trail") |
| selected_board | string | 49 characters |  |
| selected_background | string | 49 characters |  |
| highscore_default | int | 49 characters |  |
| stat_achievements | int | 49 characters |  |
| stat_total_top_run_medals_bronze | int | 49 characters |  |
| stat_total_top_run_medals_silver | int | 49 characters |  |
| stat_total_top_run_medals_gold | int | 49 characters |  |
| stat_total_top_run_medals_diamond | int | 49 characters |  |
| stat_total_top_run_medals_champion | int | 49 characters |  |
| equipped_badge_tier_`1-4` | int | the number 0-4 |  |
| equipped_badge_`1-4` | str | a valid achivements id that has a badgeIconId set |  |

all values inside the `metadata` dict have to be set in quotes even when they are integers e.g. \
stat_total_visited_destinations: "1" \
all values will allow strings but the values will then not show up in the the app correctly

when setting the key to value of 50 the error will say that the metadata values have a limit of 50 characters, which seems wrong, only 49 works

you can still try to apply values out of the specified range, but it will

1. return an error or
2. will just return the unmodified values. \
   e.g. when the `level` field value should be set to `101`, when before it is set `100` it only show 100.

`highscore` it will return an error.

When the fields `level` or `highscore` are set to 0, it will hide them in the response.

#### Inputs

the metadata map has a limit of at most 20 entries

When updating a players values, these will not be mirrored into the player's save files, but will only be shown on a player request e.g when wanting to send you an invite.
When requesting to see a profile via the Top Run list it will get the data from the `/profile` not the `GetPlayer` \
When you look at your own Player Profile, the data won't appear there. (data is from your save file)

Only the name field is needed for any request \
`level`, `highscore`, `metadata` are all optional and do not have to be included to make a successful request

Field ids are not required to have a valid value to make a successful request \
When an invalid value is set, in the app users will be shown the default values e.g jake.default, jake_portrait ...

you can set any valid value you want, and they are not restricted by having to unlock the cosmetic (e.g., dino_portrait).

<h4 id="stat_total_games_error">stat_total_games error</h4>
When setting the field <code>stat_total_games</code> to a value and then decrease the value <br>
it will then show it as a minus value, by how ever much you have decreased it <br>
e.g. when setting the value to <code>10</code> and then changing it to <code>9</code>, it will show in the response as <code>-1/25</code> (25 runs until a new level)
<br><br>
when setting the the field e.g. <code>selected_portrait</code> to a invalid value, it will show in the player preview the `jake_portrait` image and in the pop out, profile as a white box.
<br><br>
sometimes it can take 1-5 seconds until the change is visibile in the app

#### Name

You can rename yourself by only changing the name value \
This is the name value that shows everywhere up e.g. Player Profile, Top Run list
After the change, all your requests have to use that new name until the `604800` second (7 days) refresh period expires and you can change it again

#### Badges

You can set badges to your player

the key `equipped_badge_` has the value of the achievement id e.g `achievement_08` here is a [list]() \
`equipped_badge_tier_` will show the "tier" of the badge, which is the `claimState` of the achievements list and gives it just a different style

```json
"claimState": [
   true,
   true,
   true,
   true,
   true
   ],
```

You can set the badges by setting the `equipped_badge_1`, `equipped_badge_2`, `equipped_badge_3`, `equipped_badge_4` to a valid badge id. \
The values are also stored in the achivements.json file in a list, under the `equippedProfileBadges` key.

```json
  "equippedProfileBadges": [
    {
      "ID": "achievement_08",
      "TierIndex": 3
    },
    {}, // when no badge set
    {},
    {}
  ]
```

but since the value is stored locally in the file, changing it through the API won't make the change visible in the app, only in how others see your profile.

Additionally there is a error where it is not possible to clear the badges, the app can send a empty `equipped_badge_` value, while i have not found out how to replicate that

### Energy

#### Init Energy

Despite that they are in the `/rpc/` endpoints, they are able to be send and receive json.

When a _Energie_ was initialized (added), it will return the _Energie_ with the used uuid, a `value` and `regenCap`and the time it was updated.

It is unknown where this uuid is from, but it seems like its season dependent \
This request happends after the _GetWallet_ request

**When setting the _Energie_**

```json
{
  "energy": {
    "kindId": "0197780a-77bc-7bb8-bf9b-687fa58a53c0",
    "value": 3,
    "regenCap": 3,
    "updatedAt": "2025-07-04T16:43:31.298610Z"
  }
}
```

**When not using a valid uuid**

```json
{
  "code": "invalid_argument",
  "message": "bad request",
  "details": [
    {
      "type": "google.rpc.BadRequest",
      "value": "CiUKB2tpbmRfaWQSGnZhbHVlIG11c3QgYmUgYSB2YWxpZCBVVUlE",
      "debug": {
        "fieldViolations": [
          { "field": "kind_id", "description": "value must be a valid UUID" }
        ]
      }
    }
  ]
}
```

**When a uuid was found**

```json
{ "code": "not_found", "message": "request failed" }
```

**When applying the same uuid again**

```json
{ "code": "already_exists", "message": "request failed" }
```

#### Get Energies

**When no energie is set**

```json
{ "energies": {} }
```

**Default Response**

```json
{
  "energies": {
    "0197780a-77bc-7bb8-bf9b-687fa58a53c0": {
      "kindId": "0197780a-77bc-7bb8-bf9b-687fa58a53c0",
      "value": 3,
      "regenCap": 3,
      "updatedAt": "2025-07-04T16:43:31.298610Z"
    }
  }
}
```

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

### profile

This request returns the complete save data for a player.

the response will output the save data in escaped json that you can decode using this [script](./send/scripts/profile_decode.py)

All players listed in the tournament (Top Run) will return successfully. \
This profile data can be requested using the `uid`, which is simply the player's uuid.

when the id doesn't exist then it will return with 404 error

**truncated version with only wallet, dataConsent, missedRewar**dsModels

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

### Analytics

There are many different types of events

the vendor_id is the same as in the `SYBO-Vendor-Id` in the header of all the other requests \
which changes every version

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
5. Promocode doesn't exist
6. Promocode Expired

Redeem codes

PrideFrame2025 \
StPatricksDay5000 \
Istanbul_Giveaway_2024 \
VeggieHunt24_1 \
discord10

```
https://subway-surfers.sng.link/A8yjk/ucg6?_dl=subwaysurfers://&pcn=default&_p={"subway_promo_code":"{promoCode}"}
```

## Other

### Profile

Finding out how the `/profile` gets its data

One scenario I consider is that, since i have not seen the the app send the profile data directly to the server, \
and the save data is needed to make the `/profile` request, \
that they instead collect via the analytics, over time, about what you buy, collect, choose, and play, then generate your profile from that data.

For example, ecn_inventory send some inventory data, although this is quite unlikely.

<details>

```json
"custom": {
  "itm_balance": {
    "Hoverboards": 20,
    "Keys": 8,
    "HeadStarts": 3,
    "ScoreBoosters": 7,
    "Coins": 9175,
    "EventCoins": 500,
    "SprayCan": 15
  },
  "dur_balance": [
    "character.jake",
    "outfit.jake.default",
    "character.dino",
    "outfit.dino.default",
    "board.default",
    "board_upgrade.default.default",
    "board.birthday2025",
    "board_upgrade.birthday2025.default",
    "profile_frame.default_frame",
    "profile_frame.default_background",
    "profile_frame.jake_portrait",
    "profile_frame.tricky_portrait",
    "profile_frame.fresh_portrait",
    "profile_frame.yutani_portrait",
    "profile_frame.spike_portrait",
    "profile_frame.ella_portrait",
    "profile_frame.king_portrait",
    "profile_frame.tagbot_portrait",
    "profile_frame.dino_portrait"
  ]
}
```

</details>
