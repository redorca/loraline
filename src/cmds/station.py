'''
    Define a station (or node) and it's properites.
'''

class Station():
    def __init__(self, ssid=None, type="Undef"):
        self.type = type
        self.StationID = id;
        self.ssid = ssid
        self.model = model
        self.build = build_version
        self.upTime = None
        self.power = None
        self.network


