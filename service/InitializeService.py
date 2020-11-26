from main import db
from model.entity.Calibration import Calibration
from model.entity.WindowsStatus import WindowsStatus

class InitializeService:

    def __init__(self):
        pass

    @staticmethod
    def initialize():
        db.create_all()
