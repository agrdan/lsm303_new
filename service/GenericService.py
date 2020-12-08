from main import NAME
from model.entity.UUID import UUID
from utilities.DBUtil import DBUtil


class GenericService:

    @staticmethod
    def getUUID():
        uuid = DBUtil.findByName(UUID, NAME)
        return uuid.uuid