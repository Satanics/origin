import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from Connection import engine, User, conn

class Repository:
    
    def create_user(self, fio):
        raise NotImplementedError()
    
    def delete_user(self, id):
        raise NotImplementedError()

    def select_user(self, id):
        raise NotImplementedError()
    
    def update_user(self, fio, id):
        raise NotImplementedError()
    
    def select_all_users(self):
        raise NotImplementedError()


class PostgresRepository(Repository):

    def create_user(self, fio) -> str:
        name = fio
        with Session(autoflush=False, bind=engine) as db:
            rig = User(fio = name)
            db.add(rig)
            db.commit()
        return(name)

    def delete_user(self, id) -> str:
        with Session(autoflush=False, bind=engine) as db:
            db.execute(text(f'DELETE FROM test_work WHERE id = {id}'))
            db.commit()
        return('deleted')

    def select_user(self, id) -> str:
        request = conn.execute(sqlalchemy.sql.select(User.fio).where(User.id == id)).one_or_none()
        return(request[0])
    
    def update_user(self, id, fio) -> str:
        with Session(autoflush=False, bind=engine) as db:
            db.execute(text(f"UPDATE test_work SET fio = '{fio}' WHERE id = {id}"))
            db.commit()
        return('updated')
    
    def select_all_users(self) -> list:
        request = conn.execute(statement=sqlalchemy.select(User)).all()
        spisok = [[i.id,i.fio] for i in request]
        return spisok

class MemoryRepository(Repository):

    def __init__ (self) -> None:
        self.slovar = {}

    def create_user(self,fio) -> None:
        self.slovar[max(self.slovar,default = 0) + 1]  = fio

    def delete_user(self,id) -> None:
        del self.slovar[id]

    def select_user(self,id) -> dict:
        return self.slovar.get(id)

    def update_user(self,id,fio) -> None:
        self.slovar[id] = fio

    def select_all_users(self) -> dict:
        values = list(self.slovar.values())
        return values