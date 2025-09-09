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
      - [Use Energies](#use-energies)
      - [Add Energy](#add-energy)
    - [Match](#match)

## General Notes

All knowledge is for versions `3.52.1`

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

Despite that they are in the `/rpc/` endpoints, they are able to be send and receive json.

These endpoints are used for the Crossover of Subway Surfers and Brawl Stars Showdown gamemode. \
They will likely also be used for other Crossover evnts.

#### Init Energy

When a **Energie** was initialized (added?), it will return the **Energie** with the used uuid, a `value` and `regenCap`and the time it was updated.

It is unknown where this uuid is from, but it seems like its event (e.g event/crossover/collaboration ) dependent

**Default Response**

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

**When a uuid was not found**

```json
{ "code": "not_found", "message": "request failed" }
```

**When applying the same uuid again**

```json
{ "code": "already_exists", "message": "request failed" }
```

#### Get Energies

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

**When no energie is set**

```json
{ "energies": {} }
```

**Default Response**

#### Use Energies

**Default Response**

```json
{
  "energy": {
    "kindId": "0197780a-77bc-7bb8-bf9b-687fa58a53c0",
    "value": 2,
    "regenCap": 3,
    "nextAt": "2025-09-04T23:37:03.596076Z",
    "updatedAt": "2025-09-04T19:37:03.596076Z",
    "refillRate": "14400s",
    "refillCount": 1
  }
}
```

**When no energie is set**

```json
{ "energies": {} }
```

#### Add Energy

This is used for adding energy via watching Ads.
It has a limit of 10 times per 24 hours.

**Default Response**

```json
{
  "energy": {
    "kindId": "0197780a-77bc-7bb8-bf9b-687fa58a53c0",
    "value": 4,
    "regenCap": 3,
    "updatedAt": "2025-09-09T18:20:21.217957Z",
    "refillRate": "14400s",
    "refillCount": 1
  }
}
```

**When add energie limit is reached**

```json
{
  "code": "resource_exhausted",
  "message": "request failed",
  "details": [
    {
      "type": "google.rpc.QuotaFailure",
      "value": "CoIBCi9FbmVyZ3lLaW5kOjAxOTc3ODBhLTc3YmMtN2JiOC1iZjliLTY4N2ZhNThhNTNjMBJPWW91IGhhdmUgcmVhY2hlZCB5b3VyIGRhaWx5IGxpbWl0IGZvciBhZGRpbmcgZW5lcmd5LiBQbGVhc2UgdHJ5IGFnYWluIHRvbW9ycm93Lg",
      "debug": {
        "violations": [
          {
            "subject": "EnergyKind:0197780a-77bc-7bb8-bf9b-687fa58a53c0",
            "description": "You have reached your daily limit for adding energy. Please try again tomorrow."
          }
        ]
      }
    }
  ]
}
```

<details>
  <Summary>Limit</Summary>
  When firstly initializing via <code>init_energy()</code> and then using <code>add_energy()</code> 10 times,
  in the app it will display as <code>13/3</code>.
</details>

### Match

This is used for generating a Match or a Player game group.
It will output 5 random players as `PlayerResponse` bodies.
