from main import db

class DBUtil:

    @staticmethod
    def insert(model):
        try:
            db.session.add(model)
            db.session.commit()
            print("Query executed successfuly!")
        except Exception as e:
            db.session.rollback()
            print("Query rollbacked!")
            print(e)


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
