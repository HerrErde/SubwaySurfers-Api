# Explanations

## Table of Contents

<details>
  <summary>Table of Contents</summary>

- [Explanations](#explanations)
  - [Table of Contents](#table-of-contents)
  - [General Notes](#general-notes)
    - [Expired identityToken](#expired-identitytoken)
    - [Protobuf Bodies](#protobuf-bodies)
    - [Identity File](#identity-file)
    - [Player](#player)
      - [Create Player](#create-player)
      - [Update Player](#update-player)
      - [Inputs](#inputs)
      - [Name](#name)
      - [Badges](#badges)
      - [Get Player](#get-player)
      - [Get Player by Tag](#get-player-by-tag)
      - [Get Player by Id](#get-player-by-id)
    - [Friend Action](#friend-action)
      - [Get Friends](#get-friends)
      - [Get Invites](#get-invites)
      - [Get FriendsAndInvites](#get-friendsandinvites)
      - [Send Invite](#send-invite)
      - [Accept Invite](#accept-invite)
      - [Decline Invite](#decline-invite)
      - [Cancel Invite](#cancel-invite)
      - [Remove Friend](#remove-friend)
      - [Get Relationship](#get-relationship)
    - [Wallet](#wallet)
      - [Get Wallet](#get-wallet)
      - [Get Wallet Json](#get-wallet-json)
      - [Consume](#consume)
    - [Energy](#energy)
      - [Init Energy](#init-energy)
      - [Get Energies](#get-energies)
      - [Use Energies](#use-energies)
      - [Add Energy](#add-energy)
    - [Match](#match)

</details>

## General Notes

All knowledge is for versions `3.52.1`

> [!WARNING]
> Changes are expected to happen

grpc-status-details-bin content is base64

After registering and getting an account, you'll have to create a player to use all the requests; otherwise, the account is 'empty' and can't perform player actions.

You can only add abtesting to the account after adding crosspromo. This must be done in that order, else it will result in an error.

All time values are in epoch time.

this is a player tag `BY1BJH84CVHHIX` \
this is a player uuid `0197351b-ae06-7a3f-8576-0e3d5b95a280`

sec means seconds \
nsec means nanoseconds

Some response bodies that contain repeating data or with minor changes will be truncated to avoid repetition.

Some endpoints also are able to be send and receive json.

### Expired identityToken

When refreshing a identity token but still making requests with the old token, it will seem to work just fine, but e.g. your game (with the now new refreshed token) will have no changes (send invite will only appear on the player with the token, not the new one). \
Make sure to keep your identityToken refreshed and the everywhere the same.

### Protobuf Bodies

<details id="player_response">
  <summary>PlayerResponse</summary>

```json
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
  updated_at {
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

<details id="invite_quota">
  <summary>Invite Quota</summary>

```json
quota  {
  max_friends: 100
  friend_count: 1
  received_invite_count: 1
  send_invite_count: 1
  max_invites: 50
}
```

</details>

The Quota for the `max_invites` was increased from 10 to 50. (2025-12-20)

### Identity File

The identity file contains a dictionary with the user dict which contains an id, name, picture and links list.
And a refreshToken and identityToken dict that both contain a `token` value. \
The `expiresAt` value tells the app when the token expires and needs to be refreshed.

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

With Google Play connected

```json
{
  "user": {
    "id": "01968c3a-3fea-7abc-897c-e1a1814ba489",
    "name": null,
    "picture": null,
    "links": [{ "provider": "play", "id": "a_6818139433947075674" }]
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

### Player

#### Create Player

- POST `/rpc/player.ext.v1.PrivateService/CreatePlayer`
- Creates a Player into the account
- Sample request (2025-12-20): \
  POST /rpc/player.ext.v1.PrivateService/CreatePlayer \
  Authorization: `Bearer <identityToken>` \
  msg: PlayerRequest \
  resp: PlayerResponse

[Player fields](#player_fields)

#### Update Player

- POST `/rpc/player.ext.v1.PrivateService/UpdatePlayer`
- Updates the Player Profile
- Sample request (2025-12-20): \
  POST /rpc/player.ext.v1.PrivateService/UpdatePlayer \
  Authorization: `Bearer <identityToken>` \
  msg: PlayerRequest \
  resp: PlayerResponse

Update fields

<details id="player_fields">
  <Summary>Player fields</Summary>

Get all valid values [HerrErde/subway-source](https://github.com/HerrErde/subway-source)

<!-- prettier-ignore-start -->

| Id | Type | Limit | Special |
|---|---|---|---|
| name | string | 2-15 characters, only alphabet letters, no numeric | 604800 seconds (7 days) regex: `^[a-zA-Z]+$` |
| level | int | 0-100 |  |
| highscore | int | 0-2500000000 | |
| selected_country | string | 50 characters | Only ISO 3166-1 alpha-2 codes (e.g., de, us, nl). Using other values e.g., `test` will display `countries.test.name` ([country_iso.txt](./country_iso.txt)) |
| selected_character | string | 50 characters | Must follow the format `character.outfitName` (e.g., `jake.darkOutfit`) |
| selected_board | string | 50 characters |  |
| selected_board_upgrades | string | 50 characters | Comma-separated list of upgrades from the board (e.g., "default,trail") |
| selected_portrait | string | 50 characters |  |
| selected_frame | string | 50 characters |  |
| selected_background | string | 50 characters |  |
| highscore_default | int | `-1` - `2147483647`, 50 characters | |
| stat_total_visited_destinations | int | 50 characters |  |
| stat_total_games | int | 50 characters | Once set, this value should only be increased, see [value_errors](#value_errors) for details |
| stat_owned_characters | int | 50 characters |  |
| stat_owned_characters_outfits | int | 50 characters |  |
| stat_owned_boards | int | 50 characters |  |
| stat_owned_boards_upgrades | int | 50 characters |  |
| stat_achievements | int | 50 characters | `-999999999` - `9999999999` values are shown correctly, above or below are shown as 0 |
| stat_total_top_run_medals_bronze | int | 50 characters |  |
| stat_total_top_run_medals_silver | int | 50 characters |  |
| stat_total_top_run_medals_gold | int | 50 characters |  |
| stat_total_top_run_medals_diamond | int | 50 characters |  |
| stat_total_top_run_medals_champion | int | 50 characters |  |
| equipped_badge_tier_`1-4` | int | the number 0-4 |  |
| equipped_badge_`1-4` | str | a valid achivement id that has a badgeIconId |  |

<!-- prettier-ignore-end -->

</details>

<br>

~~when setting the key to value of 50 the error will say that the metadata values have a limit of 50 characters, which seems wrong, only 49 works~~ \
they fixed it

all values inside the `metadata` dict have to be set in quotes even when they are integers \
(e.g. stat_total_visited_destinations: "1") \
All fields will allow any strings but the values will then not correctly show up in the the app.

you can still try to apply values out of the specified range, but it will

1. return an error or
2. will just return the unmodified values. \
   e.g. when the `level` field should be set to `101`, when before it is set `100` it only show `100`.

#### Inputs

The metadata map has a limit of at most 20 entries

When updating a players values, these will not be mirrored into the player's save files, but will only be shown on a player profile e.g searching a player via the player tag search. \
When you look at your own Player Profile, the data won't appear there. (data is from your save file) \
When requesting to see a profile via the Top Run list, it will get the data from the `/profile` not the `/GetPlayer`

Atleast the the name field is required for any request \
`level`, `highscore`, `metadata` are all optional and do not need to be included to make a successful request.

Field ids are not required to have a valid value to make a successful request \
When an invalid value is set, in the app users will be shown the default values e.g jake.default, jake_portrait ...

you can set any valid value you want, and they are not restricted by having to unlock the cosmetic in-game (e.g., dino_portrait).

<h4 id="value_errors">value errors</h4>
When setting the field <code>stat_total_games</code> to a value and then decreasing that value,<br>
it will show as a negative value, by how ever much you have decreased the previous value by.<br>
E.g. when setting the value to <code>10</code> and then changing it to <code>9</code>, it will show in the response as <code>-1/25</code> (25 runs until a new level)
<br><br>
when setting the the field e.g. <code>selected_portrait</code> to a invalid value, it will show in the player preview the `jake_portrait` image and in the pop out, profile as a white box.
<br><br>
sometimes it can take 1-5 seconds until the change is visibile in the app

#### Name

You can rename yourself by changing the `name` value. \
This is the name value that shows everywhere up e.g. Player Profile, Top Run list. \
After the change, all your requests have to use that new name in the requests. \
Changing the name has a `604800` seconds (7 days) refresh period, which you'll have to wait until it expires and you can change it again. \
The Name field only allowes letters, no numbers or special character

#### Badges

You can set badges to your player.

The key `equipped_badge_` has the value of the achievement id e.g `achievement_08` here is a [list](https://github.com/HerrErde/subway-source/releases/latest/download/achievements_data.json)

<details>
<Summary>Achievement Badge list</Summary>
Version: <code>3.56.0</code>

```json
[
  {
    "id": "achievement_03",
    "badgeIconId": "icon_helpinghand"
  },
  {
    "id": "achievement_04",
    "badgeIconId": "icon_themorethemerrier"
  },
  {
    "id": "achievement_06",
    "badgeIconId": "icon_letterchaser"
  },
  {
    "id": "achievement_07",
    "badgeIconId": "icon_boardrider"
  },
  {
    "id": "achievement_08",
    "badgeIconId": "icon_alwaysontop"
  },
  {
    "id": "achievement_11",
    "badgeIconId": "icon_coincautious"
  },
  {
    "id": "achievement_17",
    "badgeIconId": "icon_mysterymaestro"
  },
  {
    "id": "achievement_18",
    "badgeIconId": "icon_noacrobatics"
  },
  {
    "id": "achievement_21",
    "badgeIconId": "icon_luckyduck"
  },
  {
    "id": "achievement_24",
    "badgeIconId": "icon_straightahead"
  },
  {
    "id": "achievement_28",
    "badgeIconId": "icon_therecanonlybeone"
  },
  {
    "id": "achievement_29",
    "badgeIconId": "icon_worldtour"
  },
  {
    "id": "achievement_30",
    "badgeIconId": "icon_socialsurfer"
  },
  {
    "id": "achievement_31",
    "badgeIconId": "icon_sugarrush"
  },
  {
    "id": "achievement_32",
    "badgeIconId": "icon_raceagainsttheclock"
  },
  {
    "id": "achievement_33",
    "badgeIconId": "icon_pictureperfect"
  },
  {
    "id": "achievement_34",
    "badgeIconId": "icon_demystified"
  },
  {
    "id": "achievement_35",
    "badgeIconId": "icon_massivemultiplier"
  },
  {
    "id": "achievement_36",
    "badgeIconId": "icon_brawlbesties"
  },
  {
    "id": "achievement_37",
    "badgeIconId": "icon_staroftheleague"
  },
  {
    "id": "achievement_38",
    "badgeIconId": "icon_superrunnerbadge"
  },
  {
    "id": "achievement_39",
    "badgeIconId": "icon_infectiouslypopular"
  },
  {
    "id": "achievement_40",
    "badgeIconId": "icon_amongus"
  },
  {
    "id": "achievement_41",
    "badgeIconId": "icon_yougotframed"
  }
]
```

</details>
<br>

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

But since the value is stored locally in the file, changing it through the API won't make the change visible in the app, only in how others see your profile.

Additionally there is a error where it is not possible to clear the badges, the app can send a empty `equipped_badge_` value, while i have not found out how to replicate that.

#### Get Player

- POST `/rpc/player.ext.v1.PrivateService/GetPlayer`
- Gets 5 random players
- Sample request (2025-12-21): \
  POST /rpc/player.ext.v1.PrivateService/GetPlayer \
  Authorization: `Bearer <identityToken>` \
  msg: Empty \
  resp: PlayerResponse

This will get data of the own player \
It will just return the `PlayerResponse` body

The fields do not show up directly after generating the Player \
All metadata fields will not exist until they are set with UpdatePlayer

Additionally, the `updated_at`, `name_change_expires_at` and`name_changed_at` only show when the name is changed from the name the player was created with to a new one.

#### Get Player by Tag

- POST `/rpc/player.ext.v1.PrivateService/GetPlayerByTag`
- Gets 5 random players
- Sample request (2025-12-21): \
  POST /rpc/player.ext.v1.PrivateService/GetPlayerByTag
  Authorization: `Bearer <identityToken>` \
  msg: PlayerRequest \
  resp: PlayerResponse

This gets a player by their invite Tag \
It returns the `PlayerResponse` body

#### Get Player by Id

- POST `/rpc/player.ext.v1.PrivateService/GetPlayerById`
- Gets 5 random players
- Sample request (2025-12-21): \
  POST /rpc/player.ext.v1.PrivateService/GetPlayerById \
  Authorization: `Bearer <identityToken>` \
  msg: PlayerRequest \
  resp: PlayerResponse

This gets a player by their uuid \
It returns the `PlayerResponse` body

to get the data from a player via their uuid
you need first the uuid of the player which you can get via the tag (invite id) or your own from the auth/subway-prod/identity file, the `id` field

It is not possible to get the data via a `action_uuid`, it will result in an error

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

#### Get Friends

- POST `/rpc/energy.ext.v1.PrivateService/GetFriends`
- Gets the player wallet
- Sample request (2025-12-20): \
  POST /rpc/energy.ext.v1.PrivateService/GetFriends \
  Authorization: `Bearer <identityToken>` \
  msg: Empty \
  resp: GetFriendsResponse

#### Get Invites

- POST `/rpc/energy.ext.v1.PrivateService/GetInvites`
- Gets the player wallet
- Sample request (2025-12-20): \
  POST /rpc/energy.ext.v1.PrivateService/GetInvites \
  Authorization: `Bearer <identityToken>` \
  msg: Empty \
  resp: GetInvitesResponse

When requesting the list of received invites, you get a list of `invite` bodies with each body having an `action_uuid` with which you control actions like accept, reject and so on.
The `user_uuid` that got the invite (your own), and a `PlayerResponse` body which contains the whole player metadata with uuid, and player details (game stats, collectables) and the `quota` with `max_friends`, `max_invites`, friend_count and `received_invite_count`

<details>
  <Summary>Received invites</Summary>

```json
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
      updated_at {
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
  max_invites: 50
}
```

</details>

<details>
  <Summary>Sent invites</Summary>

```json
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
      updated_at {
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
  max_invites: 50
}

```

</details>

When the invites list is empty, it will only show the [quota](#invite_quota)

#### Get FriendsAndInvites

- POST `/rpc/energy.ext.v1.PrivateService/GetFriendsAndInvites`
- Gets the player wallet
- Sample request (2025-12-20): \
  POST /rpc/energy.ext.v1.PrivateService/GetFriendsAndInvites \
  Authorization: `Bearer <identityToken>` \
  msg: Empty \
  resp: GetFriendAndInvitesResponse

This will get you, you it guessed right, your Friends AND Invites

Even when not send or received an invite, the data will still show, but empty, except your own uuid.

```json
  received_uuid {
    user_uuid: "0197a0a6-9373-7e8c-b74b-6c55ebc1106b"
  }
```

#### Send Invite

- POST `/rpc/energy.ext.v1.PrivateService/SendInvite`
- Gets the player wallet
- Sample request (2025-12-21): \
  POST /rpc/energy.ext.v1.PrivateService/SendInvite \
  Authorization: `Bearer <identityToken>` \
  msg: Empty \
  resp: SendInviteResponse

When sending a friends request to a user it will show the `action_uuid`, the truncated inviter userinfo (without metadata details) and invited user info

<details>

```json
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
      updated_at {
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
      updated_at {
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

#### Accept Invite

- POST `/rpc/energy.ext.v1.PrivateService/AcceptInvite`
- Gets the player wallet
- Sample request (2025-12-21): \
  POST /rpc/energy.ext.v1.PrivateService/AcceptInvite \
  Authorization: `Bearer <identityToken>` \
  msg: Empty \
  resp: None

#### Decline Invite

- POST `/rpc/energy.ext.v1.PrivateService/DeclineInvite`
- Gets the player wallet
- Sample request (2025-12-21): \
  POST /rpc/energy.ext.v1.PrivateService/DeclineInvite \
  Authorization: `Bearer <identityToken>` \
  msg: Empty \
  resp: None

#### Cancel Invite

- POST `/rpc/energy.ext.v1.PrivateService/CancelInvite`
- Gets the player wallet
- Sample request (2025-12-21): \
  POST /rpc/energy.ext.v1.PrivateService/CancelInvite \
  Authorization: `Bearer <identityToken>` \
  msg: Empty \
  resp: None

To cancel a send pending friend request, use the `action_uuid` from the invite or the invites list response. This `action_uuid` is unique for each player and friend request, and cannot be replaced by the original player UUID.

#### Remove Friend

- POST `/rpc/energy.ext.v1.PrivateService/RemoveFriend`
- Gets the player wallet
- Sample request (2025-12-21): \
  POST /rpc/energy.ext.v1.PrivateService/RemoveFriend \
  Authorization: `Bearer <identityToken>` \
  msg: Empty \
  resp: None

#### Get Relationship

- POST `/rpc/energy.ext.v1.PrivateService/GetRelationship`
- Gets the player wallet
- Sample request (2025-12-21): \
  POST /rpc/energy.ext.v1.PrivateService/GetRelationship \
  Authorization: `Bearer <identityToken>` \
  msg: Empty \
  resp: GetRelationshipResponse

`GetRelationship` returns the relationship status between the user and another player:

Status Codes:

1. The player is a friend
2. The other player has sent a friend request to the current player
3. The current player has sent a friend request to the other player
4. No friend relationship exists

The relationship status

```
status {
  status: 2
}
```

### Wallet

#### Get Wallet

- POST `/rpc/energy.ext.v1.PrivateService/GetWallet`
- Gets the player wallet
- Sample request (2025-12-20): \
  POST /rpc/energy.ext.v1.PrivateService/GetWallet \
  Authorization: `Bearer <identityToken>` \

The Get Wallet request outputs the time the wallet was last updated, and when it exists, show the items dict when having bought Skip Ad Tickets.

<h5>Default Response</h5>

```json
walletdata {
  updated_at {
    sec: 1748426414
    nsec: 222099082
  }
}
```

<h5>efault Response (Bought Tickets)</h5>

```json
walletdata {
  items {
    key: "skip_ad_ticket"
    value: "10"
  }
  updated_at {
    sec: 1748426414
    nsec: 222099082
  }
}
```

#### Get Wallet Json

- POST `/rpc/energy.ext.v1.PrivateService/GetWallet`
- Gets the player wallet
- Sample request (2025-12-20):
  POST /rpc/energy.ext.v1.PrivateService/GetWallet
  Content-Type: application/json
  Authorization: `Bearer <identityToken>`

This is the same as the above `GetWallet`, except that it returns as json and outputs updated at time in iso format.

You have to post with a empty dict `{}` as the payload, else it will error.

It will, when having bought skip ad tickets, contain them in the `items` dict as `skip_ad_ticket` with the amount.

<h5>Default Response</h5>

```json
{ "wallet": { "items": {}, "updatedAt": "2025-09-29T11:42:16.550165Z" } }
```

<h5>efault Response (Bought Tickets)</h5>

```json
{
  "wallet": {
    "items": { "skip_ad_ticket": 10 },
    "updatedAt": "2025-09-29T11:42:16.550165Z"
  }
}
```

#### Consume

- POST `/rpc/wallet.ext.v1.PrivateService/Consume`
- Consumes from an offer
- Sample request (2025-12-21): \
  POST /rpc/wallet.ext.v1.PrivateService/Consume \
  Authorization: `Bearer <identityToken>` \
  msg: Empty \
  resp: SendInviteResponse

You can manipulate the tickets by using these instructions [hacks.md](./hacks.md#skip-ad-tickets)

This will consume a skip ad ticket for a provided offerid.

Or the this offerid is the skip ad ticket that is consumed(no idea). \
`44c48dba-68a0-4ef6-9df4-e8aa3b1bd913` is always provided regardless of the choosen purchase.

**Send body**

```json
{
  "offerId": "44c48dba-68a0-4ef6-9df4-e8aa3b1bd913"
}
```

**Default Response**

```json
{
  "wallet": {
    "items": { "skip_ad_ticket": 10 },
    "updatedAt": "2025-09-29T11:42:16.550165Z"
  }
}
```

**On empty string**

```json
{
  "code": "invalid_argument",
  "message": "bad request",
  "details": [
    {
      "type": "google.rpc.BadRequest",
      "value": "Ch0KCG9mZmVyX2lkEhF2YWx1ZSBpcyByZXF1aXJlZA",
      "debug": {
        "fieldViolations": [
          { "field": "offer_id", "description": "value is required" }
        ]
      }
    }
  ]
}
```

**On invalid uuid**

```json
{ "code": "unknown", "message": "request failed" }
```

### Energy

These endpoints where used for the Crossover of the Subway Surfers and Brawl Stars Showdown gamemode. \
They will likely also be used for other Crossover events.

#### Init Energy

- POST `/rpc/energy.ext.v1.PrivateService/InitializeEnergy`
- Initilizing and adding the energy of the uuid to the player
- Sample request (2025-12-20): \
  POST /rpc/energy.ext.v1.PrivateService/InitializeEnergy \
  Content-Type: application/json \
  Authorization: `Bearer <identityToken>`

Request

- Body fields:
  - kindId (string, required): UUID that identifies the energy kind (event).

Example request

```json
{
  "kindId": "0197780a-77bc-7bb8-bf9b-687fa58a53c0"
}
```

<h5>Default Response</h5>

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

<h5>When not using a valid uuid</h5>

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

<h5>When a uuid was not found</h5>

```json
{ "code": "not_found", "message": "request failed" }
```

<h5>When applying the same uuid again</h5>

```json
{ "code": "already_exists", "message": "request failed" }
```

When a **Energie** was initialized (added), it will return the **Energie** with the used uuid, a `value` and `regenCap` and the time it was updated.

It is unknown where this uuid is from, but it seems like its event (e.g event/crossover/collaboration) dependent.

#### Get Energies

- POST `/rpc/energy.ext.v1.PrivateService/GetEnergies`
- Gets the energies of the user
- Sample request (2025-12-20): \
  POST /rpc/energy.ext.v1.PrivateService/GetEnergies \
  Content-Type: application/json \
  Authorization: `Bearer <identityToken>`

<h5>Default Response</h5>

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

<h5>When no energie is set</h5>

```json
{ "energies": {} }
```

#### Use Energies

- POST `/rpc/energy.ext.v1.PrivateService/UseEnergy`
- Uses the energy of the uuid
- Sample request (2025-12-20): \
  POST /rpc/energy.ext.v1.PrivateService/UseEnergy \
  Content-Type: application/json \
  Authorization: `Bearer <identityToken>`

Request

- Body fields:
  - kindId (string, required): UUID that identifies the energy kind.
  - value (int, required): The amount of energy is used.

Example request

```json
{
  "energyDiff": { "kindId": "0197780a-77bc-7bb8-bf9b-687fa58a53c0", "value": 1 }
}
```

<h5>Default Response</h5>

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

<h5>When no energie is set</h5>

```json
{ "energies": {} }
```

#### Add Energy

- POST `/rpc/energy.ext.v1.PrivateService/AddEnergy`
- Add an amount of energy of the uuid
- Sample request (2025-12-20): \
  POST /rpc/energy.ext.v1.PrivateService/AddEnergy \
  Content-Type: application/json \
  Authorization: `Bearer <identityToken>`

Request

- Body fields:
  - kindId (string, required): UUID that identifies the energy kind.
  - value (int, required): The amount of energy that gets added.

Example request

```json
{
  "energyDiff": { "kindId": "0197780a-77bc-7bb8-bf9b-687fa58a53c0", "value": 1 }
}
```

This is used for adding energy via watching Ads.
It has a limit of 10 times per 24 hours.

<h5>Default Response</h5>

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

<h5>When add energie limit is reached</h5>

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

- POST `/rpc/player.ext.v1.PrivateService/Match`
- Gets 5 random players
- Sample request (2025-12-20): \
  POST /rpc/player.ext.v1.PrivateService/Match \
  Authorization: `Bearer <identityToken>` \
  msg: Empty \
  resp: PlayerResponse

This is used for generating a Match or a Player game group.
It will output 5 random players as [`PlayerResponse`](#player_response) bodies.
