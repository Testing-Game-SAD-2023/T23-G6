import hashlib
from sqlalchemy import delete, insert, select, update, Table, Column, MetaData, Integer, String, TIMESTAMP, ForeignKeyConstraint, func, exc
from database import engine
import json

class Model:

    metadata = MetaData()

    Users_Table = Table('USERS', metadata,
                        Column('ID', Integer(), primary_key=True,autoincrement=True),
                        Column('REGISTRATION_STATE', String(64)),
                        Column('NAME', String(64), nullable=False, default="Mario"),
                        Column('SURNAME', String(64), nullable=False, default="Rui"),
                        Column('EMAIL', String(64), nullable=False, default="maestro@gmail.it", unique=True),
                        Column('PW', String(64), nullable=False, default="mariorui"),
                        Column('DEGREE', String(64))
                        )

    Users_Sessions_Table = Table('USERS_SESSIONS', metadata,
                        Column('USER_TOKEN', String(64), primary_key=True),
                        Column('ID_USER', Integer(), default="-1"),
                        Column('CREATED_AT', TIMESTAMP, server_default=func.now()),
                        ForeignKeyConstraint(["ID_USER"], ["USERS.ID"], name="FK_SESSIONS")
                        )
    
    class dbBaseClass:
        def __init__(self, json : dict = {}, **kwargs) -> None:
            self.table = None
            for key, value in json.items():
                setattr(self, str.lower(key), value)
            for key, value in kwargs.items():
                setattr(self, str.lower(key), value)

        def insert(self):
            try:
                with engine.connect() as Base:
                    Base.execute(insert(self.table), self.__initializedKeys__())
                    Base.commit()
            except:
                Base.rollback()
                raise exc.InvalidRequestError("Invalid request")
                
        def search(self) -> list:
            try:
                where_conditions = [getattr(self.table.c, key) == value for key, value in self.__initializedKeys__().items() if type(value) != Table]
                with engine.connect() as Base:
                    result = Base.execute(select(self.table)
                                        .where(*where_conditions))
                return [type(self)(json = i) for i in result.mappings().all()]
            except:
                raise exc.InvalidRequestError("Invalid request")

        def update(self, **kwargs):
            try:
                where_conditions = [getattr(self.table.c, key) == value for key, value in self.__initializedKeys__().items() if type(value) != Table]
                with engine.connect() as Base:
                    result = Base.execute(update(self.table)
                                        .where(*where_conditions)
                                        .values(**kwargs))
                    Base.commit()
                return True
            except:
                raise exc.InvalidRequestError("Invalid request")

        def delete(self):
            try:
                where_conditions = [getattr(self.table.c, key) == value for key, value in self.__initializedKeys__().items() if type(value) != Table]
                with engine.connect() as Base:
                    result = Base.execute(delete(self.table)
                                        .where(*where_conditions))
                    Base.commit()
                return result
            except:
                Base.rollback()
                raise exc.InvalidRequestError("Invalid request")

        def __initializedKeys__(self) -> dict:
            return {str.upper(k) : v for k,v in vars(self).items() if v is not None}

    class User(dbBaseClass):

        def __init__(self, json : dict = {}, cript = False, **kwargs):
            super().__init__(json, **kwargs)
            self.table = Model.Users_Table
            if(cript):
                self.pw = Model.User.__cryptCredentials__(self.pw, self.email) if hasattr(self, 'pw') and hasattr(self, 'email') else None


        def update(self, **kwargs):
            if('PW' in kwargs.keys()):
                kwargs['PW'] = Model.User.__cryptCredentials__(kwargs['PW'], self.email if 'EMAIL' not in kwargs.keys() else kwargs['EMAIL'])
            where_conditions = [getattr(self.table.c, key) == value for key, value in self.__initializedKeys__().items() if type(value) != Table]
            with engine.connect() as Base:
                result = Base.execute(update(self.table)
                                      .where(*where_conditions)
                                      .values(**kwargs))
                Base.commit()
            return True
    
        def __cryptCredentials__(*strings) -> str:
            credentials = ''.join(str(i) for i in strings)
            return hashlib.md5(credentials.encode()).hexdigest()
    
            

    class Session(dbBaseClass):

        def __init__(self, json : dict = {},**kwargs) -> None:
            super().__init__(json, **kwargs)
            self.table = Model.Users_Sessions_Table

        def generateToken(*strings: str) -> str:
            token = ''.join(str(i) for i in strings)
            return hashlib.md5(token.encode()).hexdigest()

    class Redirect:
        settings = {}
        filePath = "./settings/redirectSettings.json"

        def getSettings():
            if(len(Model.Redirect.settings) == 0):
                Model.Redirect.__initSettings__()
            return Model.Redirect.settings

        def __initSettings__():
            with open(Model.Redirect.filePath) as file:
                Model.Redirect.settings = json.load(file)
