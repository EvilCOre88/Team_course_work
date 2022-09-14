# -*- coding: utf-8 -*-

import psycopg2
import sqlalchemy
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from db.db_modules import User, SearchUser, City, Gender, Age, Favorites, Photo, create_tables

"""
Create constant variable with connection data for database server
"""
# CONNECTION = {'drivername': 'postgresql',
#               'username': 'ckkuonzb',
#               'password': 'e_J-pEQOH4hRfJMeqo5ryKOymH4TFK4Q',
#               'host': 'chunee.db.elephantsql.com',
#               'port': 5432,
#               'database': 'ckkuonzb'
#               }

CONNECTION = {'drivername': 'postgresql+psycopg2',
              'username': 'postgres',
              'password': 'Qwerty2022',
              'host': 'localhost',
              'port': 5432,
              'database': 'sql_hw'
              }

class DataBase:
    """
    Create a new class: DataBase, that creates a tables in
    the database, querying the database and creating records.
    _________________________Methods_________________________
    __init__
    engine_start
    create_table()
    add_user()
    add_photos()
    read_user()
    read_search_user()
    read_favorites
    read_photos
    add_to_favourite()
    delete_from_favorite
    main_db_dater()
    """

    def __init__(self, **connection: dict):
        """
        Initializing connection to database and start
        sqlalchemy engine
        """
        self.connection = connection
        data_sourse = sqlalchemy.engine.url.URL.create(**CONNECTION)
        self.engine = sqlalchemy.create_engine(data_sourse)

    def engine_start(self) -> sqlalchemy.engine.base.Engine:
        """
        Return engine after it's start in init
        """
        return self.engine


    def create_table(self, engine: sqlalchemy.engine.base.Engine) -> bool:
        """
        Creates tables in database, by using method
        from db_modules.py file
        """
        if create_tables(engine):
            return True
        else:
            return False

    def add_user(self, user: dict, search=None):
        """
        Add user into database
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()
        if not session.query(Age).filter(Age.id == user['age']).all():
            session.add(Age(id=user['age'], birth_year=user['birth_year']))
            session.commit()
        if not session.query(City).filter(City.id == user['city']).all():
            session.add(City(id=user['city'], town=user['city_title']))
            session.commit()
        if not session.query(Gender).filter(Gender.id == user['gender']).all():
            session.add(Gender(id=user['gender'], sex=user['gender_title']))
            session.commit()
        if search is not None:
            query = SearchUser(id=user['id'],
                               first_name=user['first_name'],
                               last_name=user['last_name'],
                               patronymic=user['patronymic'],
                               gender_id=user['gender'],
                               city_id=user['city'],
                               age_id=user['age'])
            session.add(query)
            session.commit()
            session.close()
        else:
            query = User(id=user['id'],
                         first_name=user['first_name'],
                         last_name=user['last_name'],
                         patronymic=user['patronymic'],
                         gender_id=user['gender'],
                         city_id=user['city'],
                         age_id=user['age'])
            session.add(query)
            session.commit()
            session.close()
        return

    def add_photos(self, user_id: int, photos: list):
        """
        Add searched users photos to database
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()
        for photo in photos:
            session.add(Photo(id=photo, search_user_id=user_id))
            session.commit()
            session.close

    def read_user(self, user_id: int):
        """
        Read user from database
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()
        conn = self.engine.connect()
        result = []
        if query:
            for q in query:
                result.append({'first_name': q.first_name,
                               'last_name': q.last_name,
                               'id_user': q.id})
        return result

    def read_search_user(self) -> list:
        """
        Read searched users from database
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()
        conn = self.engine.connect()
        t = text("SELECT * FROM search_user")
        result = conn.execute(t)
        result_list = []
        for res in result:
            result_list.append(res)
        session.close()
        return result_list

    def read_favorites(self) -> list:
        """
        Read searched favorites users from database
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()
        conn = self.engine.connect()
        t = text("SELECT * FROM favorites")
        result = conn.execute(t)
        result_list = []
        for res in result:
            result_list.append(res)
        session.close()
        return result_list

    def read_photos(self, user_id: int):
        """
        Read searched users photos from database
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()
        conn = self.engine.connect()
        t = text(f"SELECT id FROM photo WHERE search_user_id = {user_id}")
        result = conn.execute(t)
        result_list = []
        for res in result:
            result_list.append(res[0])
        session.close()
        return result_list

    def add_to_favorite(self, user_id: int, search_user_id: int) -> bool:
        """
        Add searched user to the favorites list
        """
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            favorite_id = f'{user_id}_{search_user_id}'
            favorite = Favorites(id=favorite_id, user_id=user_id, search_user_id=search_user_id)
            session.add(favorite)
            session.commit()
            session.close()
            return True
        except:
            return False

    def delete_from_favorite(self, user_id: int, search_user_id: int) -> bool:
        """
        Add searched user to the favorites list
        """
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            favorite_id = f'{user_id}_{search_user_id}'
            conn = self.engine.connect()
            t = text(f"DELETE FROM favorites WHERE id = '{favorite_id}'")
            result = conn.execute(t)
            session.commit()
            session.close()
            return True
        except:
            return False

def main_db_dater(**connection):
    work = DataBase(**connection)
    engine = work.engine_start()
    create = work.create_table(engine)
    if create:
        return print(f'База данных успешно создана!')
    else:
        return print(f'База не создана, что-то пошло не так')