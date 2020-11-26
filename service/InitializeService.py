from main import db
from model.entity.Calibration import Calibration

class InitializeService:

    def __init__(self):
        pass

    @staticmethod
    def initialize():
        db.create_all()
