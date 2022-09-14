import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    """
    Create a new class: User
    That class create 'user' table in database.
    _______________________Rows_______________________
    id
    first_name
    last_name
    patronymic
    age_id
    gender_id
    city_id
    """
    __tablename__ = 'user'

    id = sq.Column(sq.Integer, primary_key=True, unique=True)
    first_name = sq.Column(sq.Text, nullable=False)
    last_name = sq.Column(sq.Text, nullable=False)
    patronymic = sq.Column(sq.Text, nullable=True) #user's screenname
    age_id = sq.Column(sq.Integer, sq.ForeignKey('age.id'), nullable=False)
    gender_id = sq.Column(sq.Integer, sq.ForeignKey('gender.id'), nullable=False)
    city_id = sq.Column(sq.Integer, sq.ForeignKey('city.id'), nullable=False)
    city = relationship('City', backref='user')
    gender = relationship('Gender', backref='user')
    favorites = relationship('Favorites', backref='user')


class SearchUser(Base):
    """
    Create a new class: SearchUser
    That class create 'search_user' table in database.
    _______________________Rows_______________________
    id
    first_name
    last_name
    patronymic
    age_id
    gender_id
    city_id
    """
    __tablename__ = 'search_user'

    id = sq.Column(sq.Integer, primary_key=True, unique=True)
    first_name = sq.Column(sq.Text, nullable=False)
    last_name = sq.Column(sq.Text, nullable=False)
    patronymic = sq.Column(sq.Text, nullable=True) #user's screenname
    age_id = sq.Column(sq.Integer, sq.ForeignKey('age.id'), nullable=False)
    gender_id = sq.Column(sq.Integer, sq.ForeignKey('gender.id'), nullable=False)
    city_id = sq.Column(sq.Integer, sq.ForeignKey('city.id'), nullable=False)
    city = relationship('City', backref='search_user')
    gender = relationship('Gender', backref='search_user')
    favorites = relationship('Favorites', backref='search_user')
    photo = relationship('Photo', backref='search_user')


class City(Base):
    """
    Create a new class: City
    That class create 'city' table in database.
    _______________________Rows_______________________
    id
    town
    """
    __tablename__ = 'city'

    id = sq.Column(sq.Integer, primary_key=True, unique=True)
    town = sq.Column(sq.Text, nullable=False)


class Gender(Base):
    """
    Create a new class: Gender
    That class create 'gender' table in database.
    _______________________Rows_______________________
    id
    sex
    """
    __tablename__ = 'gender'

    id = sq.Column(sq.Integer, primary_key=True, unique=True)
    sex = sq.Column(sq.Text, nullable=False)


class Age(Base):
    """
    Create a new class: Age
    That class create 'age' table in database.
    _______________________Rows_______________________
    id
    years_old
    """
    __tablename__ = 'age'

    id = sq.Column(sq.Integer, primary_key=True, unique=True)
    birth_year = sq.Column(sq.Integer, nullable=False)


class Favorites(Base):
    """
    Create a new class: Favorites
    That class create 'favorites' table in database.
    _______________________Rows_______________________
    id
    user_id
    search_user_id
    """
    __tablename__ = 'favorites'

    id = sq.Column(sq.Text, primary_key=True, unique=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('user.id'), nullable=True)
    search_user_id = sq.Column(sq.Integer, sq.ForeignKey('search_user.id'), nullable=True)


class Photo(Base):
    """
    Create a new class: Photo
    That class create 'photo' table in database.
    _______________________Rows_______________________
    id
    photo_id
    search_user_id
    """
    __tablename__ = 'photo'

    id = sq.Column(sq.Text, primary_key=True, unique=True)
    search_user_id = sq.Column(sq.Integer, sq.ForeignKey('search_user.id'), nullable=True)


def create_tables(engine: sq.engine.base.Engine) -> bool:
    """
    Create a new class: Photo
    That class create 'photo' table in database.
    _______________________Rows_______________________
    id
    photo_id
    search_user_id
    """
    try:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        return True
    except:
        return False