from main import db

class DBUtil:

    @staticmethod
    def insert(model):
        try:
            db.session.add(model)
            db.session.commit()
            print("Query executed successfuly!")
            return True
        except Exception as e:
            db.session.rollback()
            print("Query rollbacked!")
            print(e)
        return False


    @staticmethod
    def findAll(clazz):
        eList = clazz.query.all()
        return eList


    @staticmethod
    def findById(clazz, id):
        entity = clazz.query.filter_by(id=id).one_or_none()
        return entity


    @staticmethod
    def delete(model):
        try:
            db.session.delete(model)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    @staticmethod
    def findByStatus(clazz, s):
        entity = clazz.query.filter_by(status=s).one_or_none()
        return entity

    @staticmethod
    def findByName(clazz, name):
        entity = clazz.query.filter_by(name=name).one_or_none()
        return entity

    @staticmethod
    def updateWindowsStatus(clazz, tempEntity):
        entity = DBUtil.findByStatus(clazz, tempEntity.status)
        if entity is not None:
            try:
                entity.x = tempEntity.x
                entity.y = tempEntity.y
                entity.z = tempEntity.z
                entity.vector = tempEntity.vector
                db.session.commit()
                print("Windows status updated!")
                return True
            except Exception as e:
                db.session.rollback()
                print("Query rollbacked!")
                print(e)
        return False


