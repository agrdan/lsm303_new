import json
from utilities.JSONSerializator import JSONSerializator
from datetime import datetime as dt


class LSM303Dto(JSONSerializator):

    def __init__(self):
        self.uuid = None
        self.x = None
        self.y = None
        self.z = None
        self.status = None
        self.created = None



    def getJson(self):
        lsm = {
            'UUID': self.uuid,
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'status': self.status,
            'created': str(int(dt.now().timestamp()))
        }
        return str(lsm)
