CHAT_URL = "ws://{chdomain}:{chpt}/Websocket/{bj_id}"


class ServiceCode:
    SVC_KEEPALIVE = 0
    SVC_LOGIN = 1
    SVC_JOINCH = 2
    SVC_QUITCH = 3
    SVC_CHUSER = 4
    SVC_CHATMESG = 5
    SVC_SETCHNAME = 6
    SVC_SETBJSTAT = 7
    SVC_SETDUMB = 8
    SVC_DIRECTCHAT = 9
    SVC_NOTICE = 10
    SVC_KICK = 11
    SVC_SETUSERFLAG = 12
    SVC_SETSUBBJ = 13
    SVC_SETNICKNAME = 14
    SVC_SVRSTAT = 15
    SVC_RELOADHOST = 16
    SVC_CLUBCOLOR = 17
    SVC_SENDBALLOON = 18
    SVC_ICEMODE = 19
    SVC_SENDFANLETRTRER = 20
    SVC_ICEMODE_EX = 21
    SVC_GET_ICEMODE_RELAY = 22
    SVC_SLOWMODE = 23
    SVC_RELOADBURNLEVEL = 24
    SVC_BLINDKICK = 25
    SVC_MANAGERCHAT = 26
    SVC_APPENDDATA = 27
    SVC_BASEBALLEVENT = 28
    SVC_PAIDITEM = 29
    SVC_TOPFAN = 30
    SVC_SNSMESSAGE = 31
    SVC_SNSMODE = 32
    SVC_SENDBALLOONSUB = 33
    SVC_SENDFANLETRTRERSUB = 34
    SVC_TOPFANSUB = 35
    SVC_BJSTICKERITEM = 36
    SVC_CHOCOLATE = 37
    SVC_CHOCOLATESUB = 38
    SVC_TOPCLAN = 39
    SVC_TOPCLANSUB = 40
    SVC_SUPERCHAT = 41
    SVC_UPDATETICKET = 42
    SVC_NOTIGAMERANKER = 43
    SVC_STARCOIN = 44
    SVC_SENDQUICKVIEW = 45
    SVC_ITEMSTATUS = 46
    SVC_ITEMUSING = 47
    SVC_USEQUICKVIEW = 48
    SVC_NOTIFY_POLL = 50
    SVC_CHATBLOCKMODE = 51
    SVC_BDM_ADDBLACKINFO = 52
    SVC_SETBROADINFO = 53
    SVC_BAN_WORD = 54
    SVC_SENDADMINNOTICE = 58
    SVC_FREECAT_OWNER_JOIN = 65
    SVC_BUYGOODS = 70
    SVC_BUYGOODSSUB = 71
    SVC_SENDPROMOTION = 72
    SVC_NOTIFY_VR = 74
    SVC_NOTIFY_MOBBROAD_PAUSE = 75
    SVC_KICK_AND_CANCEL = 76
    SVC_KICK_USERLIST = 77
    SVC_ADMIN_CHUSER = 78
    SVC_CLIDOBAEINFO = 79
    SVC_VOD_BALLOON = 86
    SVC_ADCON_EFFECT = 87
    SVC_SVC_KICK_MSG_STATE = 90
    SVC_FOLLOW_ITEM = 91
    SVC_ITEM_SELL_EFFECT = 92
    SVC_FOLLOW_ITEM_EFFECT = 93
    SVC_TRANSLATION_STATE = 94
    SVC_TRANSLATION = 95
    SVC_GIFT_TICKET = 102
    SVC_VODADCON = 103
    SVC_BJ_NOTICE = 104
    SVC_VIDEOBALLOON = 105
    SVC_STATION_ADCON = 107
    SVC_SENDSUBSCRIPTION = 108
    SVC_OGQ_EMOTICON = 109
    SVC_ITEM_DROPS = 111
    SVC_VIDEOBALLOON_LINK = 117
    SVC_OGQ_EMOTICON_GIFT = 118
    SVC_AD_IN_BROAD_JSON = 119
    SVC_GEM_ITEMSEND = 120
    SVC_MISSION = 121
    SVC_LIVE_CAPTION = 122
    SVC_MISSION_SETTLE = 125
    SVC_SET_ADMIN_FLAG = 126


RETURN_CODE = {
    "SUCCESS": 0,
    "ERR_1_SYSTEM": 1,
    "ERR_2_NOTLOGIN": 2,
    "ERR_3_PROTOCOL": 3,
    "ERR_4_NOSERVICE": 4,
    "ERR_5_NOTIMPL": 5,
    "ERR_6_SESSKEY": 6,
    "ERR_7_DUPSESS": 7,
    "ERR_8_MINUSERIDLEN": 8,
    "ERR_9_MAXUSERIDLEN": 9,
    "ERR_10_ALREADYJOIN": 10,
    "ERR_11_MAXOPENCHANNEL": 11,
    "ERR_12_INVALIDCHNO": 12,
    "ERR_13_BUFOVERFLOW": 13,
    "ERR_14_PACKETHDADER": 14,
    "ERR_15_PACKETBODY": 15,
    "ERR_16_NOTJOINCH": 16,
    "ERR_17_NOTCHCREATOR": 17,
    "ERR_18_SHORTCHNAME": 18,
    "ERR_19_DUMBUSER": 19,
    "ERR_20_USERNOTFOUND": 20,
    "ERR_21_SELFCOMMAND": 21,
    "ERR_22_NOTADMIN": 22,
    "ERR_23_SETBJOFFLIN": 23,
    "ERR_24_NOTALLOWADMIN": 24,
    "ERR_25_NOTALLOWSUBBJ": 25,
    "ERR_26_DUPSUBBJ": 26,
    "ERR_27_OVERSUBBJ": 27,
    "ERR_28_NONESUBBJ": 28,
    "ERR_29_REALNAME": 29,
    "ERR_30_ALIASSUBBJ": 30,
    "ERR_31_MAXNICKNAMELEN": 31,
    "ERR_32_NODIRECT": 32,
    "ERR_33_HOSTDENIED": 33,
    "ERR_34_CHATPENALTY": 34,
    "ERR_35_GUEST": 35,
    "ERR_36_HACKVERSION": 36,
    "ERR_37_NICKTIME": 37,
    "ERR_39_ICEMODE": 39,
    "ERR_40_SPACEONLY": 40,
    "ERR_41_KICKEDUSER": 41,
    "ERR_42_NOTAVAILCHAT": 42,
    "ERR_43_DANGEROUSTAG": 43,
    "ERR_43_INVALIDNICK": 44,
    "ERR_45_BALLOONHACK": 45,
    "ERR_46_DUPNICK": 46,
    "ERR_47_SLOWMODE": 47,
    "ERR_48_DUPITEM": 48,
    "ERR_49_ICEMODE_FAN": 49,
    "ERR_50_ICEMODE_SUP": 50,
    "ERR_51_ICEMODE_FAN_SUP": 51,
    "ERR_52_KICK_ACCUMULATION": 52,
    "ERR_53_BANWORD": 53,
    "ERR_54_KICKLIST_EMPTY": 54,
    "ERR_55_DENY_CHAT_USER": 55,
    "ERR_56_LIVECHAT_ERR_ABUSE_JOIN": 56,
    "ERR_58_LIVECHAT_ERR_TRANS": 58,
    "ERR_59_LIVECHAT_ERR_TRANS_NOT_ALLOW": 59,
    "ERR_60_LIVECHAT_ERR_TRANS_DELAY": 60,
    "ERR_61_LIVECHAT_ERR_TRANS_DISABLE": 61,
    "ERR_62_LIVECHAT_ERR_TRANS_ABUSE": 62,
    "ERR_64_LIVECHAT_ERR_TRANS_AUTH_SHARE": 64,
    "ERR_67_LIVECHAT_ERR_OGQPENALTY": 67,
    "PASSWORD_ERROR": 57,  # 왜 아프리카 클라 const에 없는거지?
}


FLAG = {
    "MOBILE_WEB": {
        "where": 1,
        "value": 1 << 23,
    },
    "ADMIN": {
        "where": 1,
        "value": 1,
    },
    "HIDDEN": {
        "where": 1,
        "value": 2,
    },
    "BJ": {
        "where": 1,
        "value": 4,
    },
    "DUMB": {
        "where": 1,
        "value": 8,
    },
    "GUEST": {
        "where": 1,
        "value": 16,
    },
    "FANCLUB": {
        "where": 1,
        "value": 32,
    },
    "AUTOMANAGER": {
        "where": 1,
        "value": 64,
    },
    "MANAGERLIST": {
        "where": 1,
        "value": 128,
    },
    "MANAGER": {
        "where": 1,
        "value": 256,
    },
    "FEMALE": {
        "where": 1,
        "value": 512,
    },
    "AUTODUMB": {
        "where": 1,
        "value": 1024,
    },
    "DUMB_BLIND": {
        "where": 1,
        "value": 2048,
    },
    "DOBAE_BLIND": {
        "where": 1,
        "value": 4096,
    },
    "DOBAE_BLIND2": {
        "where": 1,
        "value": 1 << 24,
    },
    "EXITUSER": {
        "where": 1,
        "value": 8192,
    },
    "MOBILE": {
        "where": 1,
        "value": 16384,
    },
    "TOPFAN": {
        "where": 1,
        "value": 32768,
    },
    "REALNAME": {
        "where": 1,
        "value": 65536,
    },
    "NODIRECT": {
        "where": 1,
        "value": 1 << 17,
    },
    "GLOBAL_APP": {
        "where": 1,
        "value": 1 << 18,
    },
    "QUICKVIEW": {
        "where": 1,
        "value": 1 << 19,
    },
    "SPTR_STICKER": {
        "where": 1,
        "value": 1 << 20,
    },
    "CHROMECAST": {
        "where": 1,
        "value": 1 << 21,
    },
    "FOLLOWER": {
        "where": 1,
        "value": 1 << 28,
    },
    "NOTIVODBALLOON": {
        "where": 1,
        "value": 1 << 30,
    },
    "NOTITOPFAN": {
        "where": 1,
        "value": 1 << 31,
    },
    "GLOBAL_PC": {
        "where": 2,
        "value": 1,
    },
    "CLAN": {
        "where": 2,
        "value": 2,
    },
    "TOPCLAN": {
        "where": 2,
        "value": 4,
    },
    "TOP20": {
        "where": 2,
        "value": 8,
    },
    "GAMEGOD": {
        "where": 2,
        "value": 16,
    },
    "ATAG_ALLOW": {
        "where": 2,
        "value": 32,
    },
    "NOSUPERCHAT": {
        "where": 2,
        "value": 64,
    },
    "NORECVCHAT": {
        "where": 2,
        "value": 128,
    },
    "FLASH": {
        "where": 2,
        "value": 256,
    },
    "LGGAME": {
        "where": 2,
        "value": 512,
    },
    "EMPLOYEE": {
        "where": 2,
        "value": 1024,
    },
    "CLEANATI": {
        "where": 2,
        "value": 2048,
    },
    "POLICE": {
        "where": 2,
        "value": 4096,
    },
    "ADMINCHAT": {
        "where": 2,
        "value": 8192,
    },
    "PC": {
        "where": 2,
        "value": 16384,
    },
    "SPECIFY": {
        "where": 2,
        "value": 32768,
    },
}
