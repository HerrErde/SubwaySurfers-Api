# Explainations

## General Notes

All knowledge is for versions 3.47.0 \
Changes can happen in future versions

grpc-status-details-bin content is base64

after registering a account, you'll have to create a player to use all the requests, else the account is 'empty' and cant make player actions

You can only add abtesting to the account after adding crosspromo. This must be done in that order, else it will result in an error.

All time values are in epoch time

### Expired identityToken

When refreshing a identity token but still making requests with the old token, it will seem to work just fine, but e.g. your game (with the now new refreshed token) will have no changes (send invite will only appear on the player with the token, not the new one). \
Make sure to keep your identityToken refreshed and the everywhere the same.

### Protobuf Body

<details>
  <summary>PlayerResponse</summary>

```json
userdata {
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

### identity file

The identity file contains a dictionary with the user dict which contains id, name, picture, links list
and a refresh and identityToken dict that both contain a `token` value. \
Also a `expiresAt` that will tell the app when to refresh the token.

all tokens are have 7 days ttl (time to live)

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

identity token

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

A user cant have more than 10 friend requests at the same time. \
After that is reached, new friend requests will not be successful

A user's friend invite rate limit, is 2 accepted invites per user per 24 hours. \
E.g. you can send a friend request to User A, they decline, then repeat a second time.
On the third request you'll likely need to wait around 24 hours before being able to send a third invite to the same player. \
But you can still send 2 friend requests to User B.

#### Get invites

When requesting the list of recieved invites, you get a list of `invite` bodys with each body having an `action_uuid` with which you control actions like accept, reject and so on.
The `user_uuid` that got the invite (your own), and a `PlayerResponse` body which contains the whole player metadata with uuid, and player details (game stats, collectables) and the quota with max_friends and max_invites, friend_count and invite_count

<details>

```json
received_invites {
  action_uuid: "01972f8a-5024-7218-bb95-73583e92edb8"
  user_uuid {
    uuid: "01972f81-3f5b-73ec-99ea-fa9c481ff4a6"
  }
  user_info {
    uuid: "01972f8a-4c30-723d-8d67-0ee30cf56335"
    userdata {
      name: "FunnyPins"
      tag: "7VY5K26493SHYG"
      level: 4
      highscore: 4622
      metadata {
        key: "stat_total_visited_destinations"
        value: "14"
      }
      trunicated metadata...
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
  invite_count: 1
  max_invites: 10
}
```

</details>

<details>

```json
sent_invites {
  action_uuid: "0197590f-df48-7105-b384-4a0c20be6a3e"
  user_info {
    uuid: "0197554e-7bd0-7061-818a-32f59e3254f5"
    userdata {
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

```json
quota  {
  max_friends: 100
  friend_count: 1
  invite_count: 1
  max_invites: 10
}
```

</details>


#### Get FriendsAndInvites

This will get you, you guessed right, your Friends AND Invites


#### Sending Friend Request

When sending a friends request to a user it will show the `action_uuid`, the trunicated inviter userinfo (without metadata details) and invited user info

<details>

```json
userinvite {
  action_uuid: "01972f9b-2f74-74fb-9625-6759350ee44c"
  invited {
    uuid: "01972f81-3f5b-73ec-99ea-fa9c481ff4a6"
    userdata {
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
    userdata {
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

When wanting to cancel send a friend Request, you have to take the `action_uuid` from the invite or the invites list response and then use it to cancel the invite

The `action_uuid` is different per player and current friend request and cant be replaced by the original player uuid \

#### Get Relationship

GetRelationship returns the relationship status between the user and another player:

Status Codes:
1 - The player is a friend
2 - The other player has sent a friend request to the user
3 - The user has sent a friend request to the other player
4 - No friend relationship exists

```json
status {
  status: 2
}
```

`action_uuid` wont work

### Get Player

This will get the own player

it will just retun the `PlayerResponse` body

The fields do not show up directly after generating the Player

all metadata fields will not exist until they are created with UpdatePlayer

also so do not `update_player_at`, `name_changed_at` or `name_change_expires_at` \
`name_changed_at` and `name_changed_expires_at` only show when the name is changed from the name the player was creatd with

### Get Player by Tag

This gets a player by their invite Tag

it returns the `PlayerResponse` body

### Get Player by Id

This gets a player by their uuid

it returns the `PlayerResponse` body

to get the data from a player via their uuid
you need first the uuid of the player which you can get via the tag or your own from the auth/subway-prod/identity file, the `id` field

it is not possible to get the data via a `action_uuid`, it will result in an error

### Get Wallet

The Get Wallet request outputs the time the wallet was last updated (probably)

```json
walletdata {
  wallet_last_save_at {
    sec: 1748426414
    nsec: 222099082
  }
}
```

### update player

Update fields

Get all valid values [HerrErde/subway-source](https://github.com/HerrErde/subway-source)

| Id                                 | Type   | Limit                                              | Special                                                                                                                                                       |
| ---------------------------------- | :----- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- |
| name                               | string | 2-15 characters, only alphabet letters, no numeric | 604800 seconds (7 days) regex: `^[a-zA-Z]+$`                                                                                                                  |     |
| level                              | int    | 100                                                |                                                                                                                                                               |
| highscore                          | int    | 214748364<u>6</u>                                  | 214748364<u>7</u> is the int32 limit, also just -1                                                                                                            |
| stat_total_visited_destinations    | int    | 49 characters                                      |                                                                                                                                                               |
| stat_total_games                   | int    | 49 characters                                      | Once set, [this value should only be increased](#stat_total_games_error) for details                                                                          |     |
| stat_owned_characters              | int    | 49 characters characters                           |                                                                                                                                                               |
| stat_owned_characters_outfits      | int    | 49 characters characters                           |                                                                                                                                                               |
| stat_owned_boards                  | int    | 49 characters characters                           |                                                                                                                                                               |
| stat_owned_boards_upgrades         | int    | 49 characters characters                           |                                                                                                                                                               |
| selected_portrait                  | string | 49 characters characters                           |                                                                                                                                                               |
| selected_frame                     | string | 49 characters characters                           |                                                                                                                                                               |
| selected_country                   | string | 49 characters                                      | Only ISO 3166-1 alpha-2 codes (e.g., de, en, nl). Using other values (e.g., `test`) will display `countries.test.name` ([country_iso.txt](./country_iso.txt)) |
| selected_character                 | string | 49 characters                                      | Must follow the format `character.Outfit` (e.g., `jake.darkOutfit`)                                                                                           |
| selected_board_upgrades            | string | 49 characters                                      | Comma-separated list of upgrades (e.g., "default,trail")                                                                                                      |
| selected_board                     | string | 49 characters                                      |                                                                                                                                                               |
| selected_background                | string | 49 characters                                      |                                                                                                                                                               |
| highscore_default                  | int    | 49 characters                                      |                                                                                                                                                               |
| stat_achievements                  | int    | 49 characters                                      |                                                                                                                                                               |
| stat_total_top_run_medals_bronze   | int    | 49 characters                                      |                                                                                                                                                               |
| stat_total_top_run_medals_silver   | int    | 49 characters                                      |                                                                                                                                                               |
| stat_total_top_run_medals_gold     | int    | 49 characters                                      |                                                                                                                                                               |
| stat_total_top_run_medals_diamond  | int    | 49 characters                                      |                                                                                                                                                               |
| stat_total_top_run_medals_champion | int    | 49 characters                                      |                                                                                                                                                               |

all values inside the `metadata` dict have to be set in quotes even when they are integers e.g. \
stat_total_visited_destinations: "1" \
all values will allow strings but the values will then not show up in the the app correctly

when setting the key to value of 50 the error will say that the metadata values have a limit of 50 characters, which seems wrong, only 49 works

you can still try to apply values out of the specified range but it will 1. return an error or 2. will just return the unmodified values \
when the `level` field value e.g. should be set to 101, when before it is set 100 it only show 100 \
highscore it will return an error

when the fields `level` or `highscore` are set to 0, it will hide them in the response

#### inputs

when updating a players values these will not me mirrored into the players save files but will only be shown on a player request e.g when wanting to send you an invite \
When requesting to see a profile via the Top Run list it will get the data from the `/profile` not the `GetPlayer`
When you look at your own Player Profile, there will the data also not appear (data is from your save file)

Only the name field it needed for any request \
level, highscore, metadata are all optional and do not have to be included to make a successfull request

Field ids are not required to have a valid value to make a successful request \
When an Invalid value is set, in the app users will be shown the default values e.g jake.default, jake_portrait ...

you can set any valid value you want, and they are not restricted by having to unlock the cosmetic e.g. having to unlock the dino_portrait

<h4 id="stat_total_games_error">stat_total_games error</h4>
When setting the field <code>stat_total_games</code> to a value and then decrease the value <br>
it will then show it as a minus value, by how ever much you have decreased it <br>
e.g. when setting the value to <code>10</code> and then changing it to <code>9</code>, it will show in the response as <code>-1/25</code> (25 runs until a new level)
<br><br>
when setting the e.g. the field <code>selected_portrait</code> to a invalid value it will show in the player preview the jake_portrait image and in the pop out profile as a white box
<br><br>
sometimes it can take 1-5 seconds until the change is visibile in the app

#### Name

You can rename yourself by only changing the name value \
This is the name value that shows everywhere up e.g. Player Profile, Top Run list
After the change, all your requests have to use that new name until the 604800 second (7 days) refresh period expires.

## Json

### Register

This will create a "empty" account that only creates a user with which you populate it with a player \
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

The Refresh request is used to refresh the Accounts identity token before the set ttl

it will return the same json as register response

### Manifest

From the Manifest you get the version specific version data \
You get the secret by extracting the game file (apk or ipa) and in the `assets/settings/sybo.tower.default.json` (ipa is `Payload/SubwaySurf.app/Data/Raw/settings/sybo.tower.default.json`) file contains a key `Secret` with the version specific secret.

for specific experiments you can set `ab_google_play`, `ab_revive_codechange`

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

```
https://manifest.tower.sybo.net/v1.0/subway/3.36.0/ios/4fPvIR1E1SnL1LRl9453/manifest.json
https://manifest.tower.sybo.net/v1.0/subway/3.44.1/android/99fGW8FHpmAbQR4BqBwr/manifest.json
https://manifest.tower.sybo.net/v1.0/subway/3.44.2/ios/s8B88pVbhzpKmvX6BV0u/manifest.json
https://manifest.tower.sybo.net/v1.0/subway/3.44.2/android/s8B88pVbhzpKmvX6BV0u/ab_revive_codechange/manifest.json
https://manifest.tower.sybo.net/v1.0/subway/3.44.2/android/s8B88pVbhzpKmvX6BV0u/manifest.json
```


```
https://manifest.tower.sybo.net/v1.0/{game}/{version}/{platform}/{secretToken}/manifest.json
```
### Gamedata

It is possible to get the gamedata/tower files of the old depreciated method of extracting the apk gamefile or ipa gamefile, using from the manifest request contained `gamedata` value
(state 3.47.0)

You can request the `manifest.json`, which is contains the manifest of all the exsisting files in gamedata, after you can get all other files

```json
{"experiment":"default","game":"subway","objects":{"achievements":{"filename":"achievements.json","key":"2bed33daedf13ae310d90edff852600598e665e3"},"adplacements":{"filename":"adplacements.json","key":"2010b70022bba2451310a6e60166a4b31f21fe0b"},"assemblyevents":{"filename":"assemblyevents.json","key":"4fa66108ddd7f8bead20b40f6a8b505a9cdf098f"}...},"spec":"v1.0","version":"3.46.0"}
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

it needs to have the User Agent \
`UnityPlayer/2022.3.24f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)`

inside the `assets/aa/catalog.json` file, inside the list `m_InternalIds`, you can see all the files which are the links that are beginning with "sybo://"

`9917a9a0-0de9-40fb-bb80-392ee596f705/bundle/1.0.0/characters-remote_assets_pixeljake_default_outfit_config_7a3d5cbdbef0e42b386ceea8f110c324.bundle`

### GDPR status

You can delete your account which is required by the gdpr and with this request you can look for the status of your deletion request

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
when you are friends with a player you are removed their friends list

it will only delete your `player` but not your `account`, that means you can just use `CreatePlayer` again without the need of registering again

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

### send tournament

<details>

````json
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


```json

<details>

### get tournament

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
````

</details>

### profile

This request returns the complete save data for a player.
you only need the player uuid

the response will then output the save data in escaped json that you can decode using [profile_decode.py](./profile_decode.py)

All players listed in the tournament (Top Run) will return successfully.
This profile data can be requested using the `uid`, which is simply the player's uuid.

It is unknown when and how the save data of a player is requestable

when the id dosnt exist then it will return with 404 error

trunicated version with only wallet, dataConsent, missedRewardsModels

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

### analytics

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

3 - Already redeemed
5 - Promocode dosnt exists
6 - Promocode Expired

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

One scenario I consider is that, since the app doesn’t send all your save data directly to the server and the save data is needed to make the `/profile` request, that they instead collect via the analytics, over time, about what you buy, collect, choose, and play, then generate your profile from that data.

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
