from main import db
from datetime import datetime as dt
import uuid as uid

class UUID(db.Model):
    __tablename__ = 'UUID'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    uuid = db.Column(db.String())
    created = db.Column(db.String(20), nullable=False)

    @staticmethod
    def create(name):
        _uuid = UUID()
        _uuid.name = name
        _uuid.uuid = str(uid.uuid4())
        _uuid.created = str(int(dt.now().timestamp()))
        return _uuid