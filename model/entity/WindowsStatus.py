from main import db
from datetime import datetime as dt
from enum import Enum
import math

class Status(Enum):
    OTVOREN = 1
    ZATVOREN = 2
    KIPER = 3



class WindowsStatus(db.Model):
    __tablename__ = 'windows_status'

    id = db.Column(db.Integer(), primary_key=True)
    x = db.Column(db.Integer())
    y = db.Column(db.Integer())
    z = db.Column(db.Integer())
    vector = db.Column(db.Integer())
    status = db.Column(db.Integer(), unique=True)

    @staticmethod
    def create(x, y, z, s):
        status = WindowsStatus()
        status.x = x
        status.y = y
        status.z = z
        status.vector = math.sqrt(math.pow((x + y + z), 2))
        status.status = s
        return status