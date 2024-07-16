'''
    set of commands understood by the network nodes.
'''
'''
'''

lora_cmds  = {
        "get":["info", "map", "online", "nwinfo", "debug", "userinfo", "new map", "grpinfo", "LOG", "more log", "id", "wifi",],
        "write": ["log", ],
        "add": ["station", "grp", ],
        "remove": ["stn", "grp"],
        "clear": ["map", "groups", "log" ],
        "send": ["RU_ON", "TR", "ru_ok", "msg", "text", "name", "address", "tz", "params"],
        "change": ["id", ],
        "reboot": ["", "stn"],
        "update": ["all", "{n,m}", "stn", ],
        "clone": ["stn", ],
        "set": ["epoch"],
        "exit": [], }

