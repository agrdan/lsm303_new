from main import db, NAME
from model.entity.Calibration import Calibration
from model.entity.WindowsStatus import WindowsStatus
from model.entity.UUID import UUID
from utilities.DBUtil import DBUtil

class InitializeService:


    def __init__(self):
        pass

    @staticmethod
    def initialize():
        db.create_all()

        uuid = DBUtil.findByName(UUID, NAME)
        if uuid is None:
            uuid = UUID.create(NAME)
            DBUtil.insert(uuid)

