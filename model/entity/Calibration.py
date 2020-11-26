from main import db
from datetime import datetime as dt

class Calibration(db.Model):
    __tablename__ = 'calibration'

    id = db.Column(db.Integer(), primary_key=True)
    offset_x = db.Column(db.Integer())
    offset_y = db.Column(db.Integer())
    offset_z = db.Column(db.Integer())
    scale_x = db.Column(db.Float())
    scale_y = db.Column(db.Float())
    scale_z = db.Column(db.Float())
    created = db.Column(db.String(20), nullable=False)

    @staticmethod
    def create(offsetX, offsetY, offsetZ, scaleX, scaleY, scaleZ):
        calibration = Calibration()
        calibration.offset_x = offsetX
        calibration.offset_y = offsetY
        calibration.offset_z = offsetZ
        calibration.scale_x = scaleX
        calibration.scale_y = scaleY
        calibration.scale_z = scaleZ
        calibration.created = str(int(dt.now().timestamp()))
        return calibration