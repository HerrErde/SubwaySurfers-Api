import urllib.parse
from typing import Optional

import httpx

api_url = "https://subway.prod.sybo.net"


headers = {
    "User-Agent": "Subway Surf/3.46.9 (Android OS 13 / API-33 (TKQ1.230127.002/TP2R)) Android)",
    "TE": "trailers",
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip",
}


# TODO
def send_analytics(
    event_name=None,
    app_id="com.kiloo.subwaysurf",
    core_pkg="com.sybo.analytics@1.9.7",
    genuine_app=1,
    install_source="com.android.vending",
    ab_list={"default": "default"},
    event=None,
):
    url = api_url + "/v1.0/analytics/send"

    events = [
        "user_engagement",
        "friends_action",
        "session_start",
        "sdk_init",
        "ad_init",
        "ad_request",
        "ad_error",
        "ad_loaded",
        "ad_clicked",
        "asset_loaded",
        "xp_campaign",
        "collectible_action",
        "game_start",
        "run_finish",
        "app_step",
        "enc_item_buy",
        "enc_item_use",
        "feature_rw_unlock",
        "feature_rw_claim",
        "transaction_click",
        "player_profile",
        "ecn_item_use",
        "bootstrap_start",
        "bootstrap_end",
        "bootstrap_step",
        "ecn_inventory",
        "ecn_item_buy",
        "data_req",
        "data_resp",
        "ad_will_play",
        "ad_impression",
        "ad_served",
        "level_up",
        "game_finish",
        "revive_resp",
        "revive_req",
        "mail_read",
        "ecn_item_free",
        "permanently_unlocked",
        "ui_show",
    ]

    ab_list = [
        {"default": "default"},
        {"ex_maxmediation_v3": "default"},
        {"ex_maxmediation_v3": "default"},
    ]

    if event not in events:
        raise ValueError(f"Invalid event: {event}. Must be one of {events}.")

    if net_type not in ["ConnectedToWIFI", "ConnectedToData"]:
        raise ValueError(
            f"Invalid net_type: {net_type}. Must be 'ConnectedToWIFI' or 'ConnectedToData'."
        )

    if ab_list and not isinstance(ab_list, dict):
        raise ValueError("ab_list must be a dictionary.")
    if ab_list not in ab_list:
        raise ValueError(
            f"Invalid ab_list: {ab_list}. Must be one of {list(ab_list.keys())}."
        )

    # check if session_id is positive integer
    if session_id or session_time_ms <= 0:
        raise ValueError("session_id must be a positive integer.")

    common = {
        "game_data_version": app_version,
        "genuine_app": genuine_app,
        "net_ping": net_ping,
        "net_type": "ConnectedToWIFI",
        "ab_list": ab_list,
        "profile_id": profile_id,
    }

    if event_name is "bootstrap_start":
        common = {"game_data_version": "3.46.9"}
        custom = {"id": "sequence_main", "total_time_ms": 881, "memory_kb": 361636}
    elif event_name is "user_engagement":
        common = {"game_data_version": "3.46.9", "genuine_app": 0}
        custom = {}
    elif event_name is "friends_action":
        custom = {"friends": 6, "action": "info"}
        """{
            "friends": 5,
            "action": "remove",
            "uid": "0196fe23-380d-78e1-bb34-4e4d2e61a0c8",
            "action_det": "Navigation",
        }"""
    elif event_name is "ecn_inventory":
        custom = {
            "itm_balance": {
                "Hoverboards": 10,
                "Keys": 5,
                "HeadStarts": 5,
                "ScoreBoosters": 5,
                "Coins": 10104,
            },
            "dur_balance": [
                "character.jake",
                "outfit.jake.default",
                "board.default",
                "board_upgrade.default.default",
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
            ],
        }
    elif event_name is "bootstrap_end":
        custom = {
            "id": "sequence_main",
            "total_time_ms": 5743,
            "foreground_time_ms": 6287,
            "memory_kb": 662780,
        }

    elif event_name is "session_data":
        custom = {
            "age": 43,
            "consent": "Given",
            "lang": "en",
            "region_code": "de",
            "cmp": "error",
            "source": None,
            "cmp_error": "ANDROID_UMP_ERROR_INTERNET_ERROR",
        }

    elif event_name is "mail_read":
        custom = {
            "header": "ui.city_tour.title",
            "mail_id": "s101_copenhagen_200thWorldTour_2",
            "has_attachment": 0,
        }

    elif event_name is "permanently_unlocked":
        custom = {
            "item_id": "birthday2025",
            "item_type": "Board",
            "source": "Mailbox",
            "characters": 1,  #
            "outfits": 0,
            "boards": 2,
            "board_abilities": 0,
        }
        """{
          "item_id": "doubleScore",
          "item_type": "Upgrade",
          "source": "IngameCurrencyPurchase",
          "characters": 2,
          "outfits": 0,
          "boards": 2,
          "board_abilities": 0
        }"""

    elif event_name is "ecn_item_free":
        custom = (
            {
                "itm_balance": {
                    "Hoverboards": 15,
                    "Keys": 5,
                    "HeadStarts": 6,
                    "ScoreBoosters": 6,
                    "Coins": 10304,
                },
                "itm_acquired": {
                    "Coins": 200,
                    "HeadStarts": 1,
                    "ScoreBoosters": 1,
                    "Hoverboards": 5,
                },
                "source": "Mailbox",
                "level": 1,
                "location": "copenhagen",
                "game_no": 1,
            },
        )
        """{
            "itm_balance": {
                "Hoverboards": 20,
                "Keys": 11,
                "HeadStarts": 6,
                "ScoreBoosters": 10,
                "Coins": 7304,
                "EventCoins": 500,
            },
            "itm_acquired": {"EventCoins": 500},
            "source": "SeasonHunt,0/30",
            "level": 1,
            "location": "copenhagen",
            "game_no": 1,
        }"""
    elif event_name is "feature_rw_unlock":
        custom = {
            "feature_id": "Achievement",
            "feature_sub_id": "achievement_04",
            "location": "copenhagen",
            "season_id": "season_S101",
            "game_no": 1,
            "unlock_type": "Objective",
            "tiers": 4,
            "tier_no": 1,
            "req_reach_val": 2,
            "req_val": 12,
            "level": 1,
        }
    elif event_name is "player_profile":
        custom = {
            "portrait": 1,
            "background": 0,
            "frame": 0,
            "name": 0,
            "type": "local_profile",
        }
    elif event_name is "ecn_item_buy":
        custom = {
            "bundle_id": "dynamic_scorebooster_pack",
            "itm_balance": {
                "Hoverboards": 15,
                "Keys": 5,
                "HeadStarts": 6,
                "ScoreBoosters": 10,
                "Coins": 7804,
            },
            "itm_acquired": {"ScoreBoosters": 3},
            "itm_use": {"Coins": 7500},
            "level": 1,
            "location": "copenhagen",
            "source": "Shop",
            "game_no": 1,
        }
        """
        {
          "bundle_id": "",
          "itm_balance": {
            "Hoverboards": 20,
            "Keys": 1,
            "HeadStarts": 6,
            "ScoreBoosters": 10,
            "Coins": 7304,
            "EventCoins": 500
          },
          "itm_acquired": {
            "SeasonHuntSkip,season_S101,1": 1
          },
          "itm_use": {
            "Keys": 10
          },
          "level": 1,
          "location": "copenhagen",
          "source": "SeasonHunt",
          "game_no": 1
        }"""
    elif event_name is "feature_rw_claim":
        custom = {
            "feature_id": "calendar",
            "feature_sub_id": "s100_copenhagen_calendar",
            "location": "copenhagen",
            "season_id": "season_S101",
            "game_no": 1,
            "claim_type": 0,
            "tiers": 20,
            "tier_no": 5,
            "level": 1,
        }
        """{
          "feature_id": "mission",
          "feature_sub_id": "1",
          "location": "copenhagen",
          "season_id": "season_S101",
          "game_no": 1,
          "level": 1,
          "claim_type": 0,
          "tiers": 3,
          "tier_no": 0,
          "req_reach_val": 20,
          "req_val": 20
        }"""
    elif event_name is "app_step":
        custom = {
            "type": "Tutorial_Init",
            "sub_type": "GetHigherScores",
            "step_no": 12,
            "steps": 21,
        }
        """{
          "type": "Tutorial_Init",
          "sub_type": "TokenBoxPopup",
          "step_no": 16,
          "steps": 21
        }
        """
        """{
          "type": "Tutorial_Init",
          "sub_type": "GreatRun",
          "step_no": 17,
          "steps": 21
        }"""

    elif event_name is "transaction_click":
        custom = {
            "currency": "EUR",
            "value_local": 5.49,
            "product_id": "welcomepack_skipAds_tickets",
            "product_type": "Bundle",
            "sales_id": "",
            "sales_type": "NoDiscount",
        }

    elif event_name is "transaction":
        custom = {
            "iap_status": 3,
            "product_id": "welcomepack_skipAds_tickets",
            "currency": "EUR",
            "internal_error_code": 2006,
            "value_local": 5.49,
            "product_type": "Bundle",
            "sales_id": "",
            "sales_type": "NoDiscount",
            "transaction_id": None,
            "sku": "subwaysurfers.welcomepack_skipads",
        }

    elif event_name is "game_start":
        custom = {
            "location": "copenhagen",
            "active_features": [
                "dailyChallenge.v2_default_ranked",
                "coinChallenge.v2_new_coin",
            ],
            "level": 1,
            "game_no": 2,
            "run_no": 1,
            "season_id": "season_S101",
            "level_booster": 0,
            "character": "dino",
            "outfit": "default",
            "board": "default",
            "board_ability": "",
            "game_seed": 618682370,
            "mode": "default",
        }
        """{
          "location": "tokyo",
          "active_features": [
            "N/A"
          ],
          "level": 2,
          "game_no": 3,
          "run_no": 1,
          "season_id": "season_S101",
          "level_booster": 0,
          "character": "dino",
          "outfit": "default",
          "board": "default",
          "board_ability": "",
          "game_seed": 419144107,
          "mode": "cityTours"
        }"""
    elif event_name is "run_finish":
        custom = {
            "location": "copenhagen",
            "active_features": [
                "dailyChallenge.v2_default_ranked",
                "coinChallenge.v2_new_coin",
            ],
            "level": 1,
            "score": 5483,
            "game_no": 2,
            "run_no": 1,
            "run_time": 168,
            "run_speed": 213,
            "end_reason": "Hit",
            "stumbles": 0,
            "itm_used": {},
            "itm_collected": {"token": 1, "box": 2, "coin": 550, "letter": 10},
            "season_id": "season_S101",
            "end_obstacle": "Blocker_Roll",
            "difficulty": -1,
            "chunk_id": "Chunk_4_Units_3_Tracks_B-S-B",
            "shield_hits": 0,
            "shield_run_time": 0,
            "shield_score": 0,
            "bonus_offered": {},
            "bonus_viewed": {},
            "mode": "default",
        }
        """{
          "location": "tokyo",
          "active_features": [
            "N/A"
          ],
          "level": 2,
          "score": 24430,
          "game_no": 3,
          "run_no": 1,
          "run_time": 17,
          "run_speed": 220,
          "end_reason": "Hit",
          "stumbles": 0,
          "itm_used": {
            "headstart": 3,
            "score_booster": 3
          },
          "itm_collected": {
            "coin": 21
          },
          "season_id": "season_S101",
          "end_obstacle": "Train_Static_1",
          "difficulty": -1,
          "chunk_id": "Chunk_4_Units_3_Tracks_S-S-S-S",
          "shield_hits": 0,
          "shield_run_time": 0,
          "shield_score": 0,
          "bonus_offered": {},
          "bonus_viewed": {},
          "mode": "cityTours"
        }"""
        """{
          "location": "copenhagen",
          "active_features": [
            "dailyChallenge.v2_default_ranked",
            "coinChallenge.v2_new_coin"
          ],
          "level": 3,
          "score": 1090,
          "game_no": 5,
          "run_no": 1,
          "run_time": 18,
          "run_speed": 121,
          "end_reason": "Hit",
          "stumbles": 0,
          "itm_used": {},
          "itm_collected": {
            "coin": 45
          },
          "season_id": "season_S101",
          "end_obstacle": "Train_Static_3",
          "difficulty": -1,
          "chunk_id": "Chunk_S-B-S-B",
          "shield_hits": 0,
          "shield_run_time": 0,
          "shield_score": 0,
          "bonus_offered": {},
          "bonus_viewed": {},
          "mode": "default"
        }"""

    elif event_name is "revive_req":
        custom = {
            "location": "copenhagen",
            "level": 1,
            "status": "Skipped",
            "key_status": "MinRequirements",
            "ad_status": "NotAvailable",
            "price": 0,
            "itm_offered": {"jetpack": 1, "magnet": 1, "hoverboard": 1},
            "itm_balance": {
                "Hoverboards": 20,
                "Keys": 3,
                "HeadStarts": 6,
                "ScoreBoosters": 10,
                "Coins": 7604,
                "EventCoins": 500,
                "SprayCan": 15,
            },
            "run_no": 1,
            "type": "main",
            "game_no": 2,
            "mode": "default",
        }
        """{
          "location": "copenhagen",
          "level": 3,
          "status": "Shown",
          "key_status": "MinRequirements",
          "ad_status": "Shown",
          "price": 1,
          "itm_offered": {
            "jetpack": 1
          },
          "rev_timeout": 8,
          "game_no": 5,
          "run_no": 1,
          "mode": "default"
        }"""
        """{
          "location": "copenhagen",
          "level": 3,
          "status": "Shown",
          "key_status": "MinRequirements",
          "ad_status": "Shown",
          "price": 1,
          "itm_offered": {
            "magnet": 1
          },
          "rev_timeout": 8,
          "game_no": 4,
          "run_no": 2,
          "mode": "default"
        }"""
    elif event_name is "revive_resp":
        custom = {
            "location": "copenhagen",
            "level": 3,
            "ad_available": True,
            "price": 1,
            "itm_offered": {"jetpack": 1},
            "rev_choice": "DismissedByTime",
            "revived": False,
            "game_no": 5,
            "run_no": 1,
            "mode": "default",
        }
        """{
          "location": "copenhagen",
          "level": 3,
          "ad_available": true,
          "price": 1,
          "itm_offered": {
            "magnet": 1
          },
          "rev_choice": "DismissedByClickOutside",
          "revived": false,
          "game_no": 4,
          "run_no": 2,
          "mode": "default"
        }"""

    elif event_name is "game_finish":
        custom = {
            "location": "copenhagen",
            "active_features": [
                "dailyChallenge.v2_default_ranked",
                "coinChallenge.v2_new_coin",
            ],
            "level": 1,
            "score": 5483,
            "avg_fps": 59,
            "avg_mem": 510,
            "max_mem": 625,
            "fps_01perc_low": 54.69,
            "fps_001perc_low": 25,
            "target_fps": 60,
            "game_no": 2,
            "game_time": 168,
            "revives": 0,
            "mode": "default",
        }

    elif event_name is "level_up":
        custom = {"location": "copenhagen", "level": 2}
    elif event_name is "ecn_item_use":
        custom = {
            "itm_balance": {
                "Hoverboards": 20,
                "Keys": 3,
                "HeadStarts": 3,
                "ScoreBoosters": 7,
                "Coins": 9154,
                "EventCoins": 500,
                "SprayCan": 15,
            },
            "itm_use": {"HeadStarts": 3, "ScoreBoosters": 3},
            "level": 2,
            "location": "tokyo",
            "run_no": 1,
            "game_no": 3,
        }

    elif event_name is "ad_request":
        custom = {"sdk": "IronSource", "ad_unit": "interstitial"}
        """
        {
          "sdk": "IronSource",
          "ad_unit": "banner"
        }"""
    elif event_name is "ad_error":
        custom = {
            "sdk": "IronSource",
            "ad_unit": "banner",
            "error_type": "load_fail",
            "error_code": 606,
            "error_int_desc": "Mediation No fill",
            "revenue": 0,
        }
    elif event_name is "ad_served":
        custom = {
            "sdk": "IronSource",
            "ad_unit": "interstitial",
            "placement": "BeforeEndRun",
            "completed": False,
            "ad_network": "mintegral",
            "auction_id": "5661a590-398c-11f0-b2db-6112f2498d84_255040762",
            "instance_id": "3733491",
            "instance_name": "Bidding",
            "precision": "BID",
            "revenue": 0.0037263,
            "segment_name": "NON COPPA - Targeted Ads",
        }
    elif event_name is "ad_impression":
        custom = {
            "sdk": "IronSource",
            "ab": "N/A",
            "ad_unit": "interstitial",
            "auction_id": "5661a590-398c-11f0-b2db-6112f2498d84_255040762",
            "conversion_value": 0,
            "country": "DE",
            "placement": "BeforeEndRun",
            "segment_name": "NON COPPA - Targeted Ads",
            "ad_network": "mintegral",
            "instance_id": "3733491",
            "instance_name": "Bidding",
            "precision": "BID",
            "revenue": 0.0037263,
        }

    elif event_name is "ad_will_play":
        custom = {
            "sdk": "IronSource",
            "ad_unit": "interstitial",
            "placement": "BeforeEndRun",
            "auction_id": "5661a590-398c-11f0-b2db-6112f2498d84_255040762",
            "ad_network": "mintegral",
            "segment_name": "NON COPPA - Targeted Ads",
            "instance_id": "3733491",
            "instance_name": "Bidding",
            "precision": "BID",
            "revenue": 0.0037263,
        }
    elif event_name is "ad_loaded":
        custom = {"sdk": "IronSource", "ad_unit": "", "time_ms": 3980, "revenue": 0}
    elif event_name is "session_start":
        common = None  # None means that there is no change from the normal common dict
        custom = {}
    elif event_name is "sdk_init":
        common = None
        custom = {}
    elif event_name is "data_req":
        common = None
        custom = {"type": "data_consent"}
    elif event_name is "data_resp":
        common = None
        custom = {"type": "data_consent", "resp": "False", "time_ms": 6887}

    data = {
        "events": [
            {
                "event_id": "16e8bba6-3864-4ee5-a827-1d4ee1ed937e",  # no idea how its generated
                "event_timestamp": event_timestamp,  # event time in ms
                "event_name": event_name,
                "device": {
                    "category": device_category,
                    "model": device_model,
                    "os": device_os,
                    "locale": device_locale,
                    "tz_offset_sec": device_tz_offset_sec,
                    "os_brand": device_os_brand,
                    "os_device": device_os_device,
                    "os_model": device_os_model,
                },
                "core": {
                    "platform": "Android",
                    "app_id": app_id,
                    "app_version": app_version,
                    "user_id": "64126ceb-de69-41ae-9fc1-931c4bd6f397",  # no idea
                    "vendor_id": vendor_id,
                    "sample_val": 42,
                    "install_source": install_source,
                    "session_id": session_id,  # session start time in ms
                    "session_no": session_no,  # the session number, incremented each time a new session starts
                    "session_time_ms": session_time_ms,  # time in ms since session start
                    "pkg": core_pkg,
                },
                "common": common,
                "custom": custom,
            }
        ]
    }

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            json=data,
        )

        print("Response Status Code:", r.status_code)


# TODO
def send_analytics_blob():

    url = api_url + "/v1/analytics/blob"

    data = {
        "event_id": "",
        "event_timestamp": 1759499363230,
        "event_name": "user_engagement",
        "device": {
            "category": "Handheld",
            "model": "",
            "os": "",
            "locale": "en-US",
            "os_brand": "",
            "os_device": "",
            "os_model": "",
            "tz_offset_sec": 7200,
        },
        "core": {
            "platform": "Android",
            "app_id": "com.kiloo.subwaysurf",
            "app_version": "3.52.4",
            "user_id": "",
            "vendor_id": "",
            "sample_val": 70,
            "session_id": 1759499096799,
            "session_no": 111,
            "session_time_ms": 70793,
            "install_source": "",
            "backend_id": "01999632-e38e-7cf6-9aff-892dd477a3e4",
            "pkg": "com.sybo.analytics@1.10.2",
        },
        "common": {
            "game_data_version": "3.52.4",
            "net_ping": 14,
            "net_type": "ConnectedToData",
            "genuine_app": 3,
            "ab_list": {"default": "default"},
            "profile_id": "",
        },
        "custom": {},
    }

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            json=data,
        )
        r.raise_for_status()
        print("Response Status Code:", r.status_code)


analytics()
