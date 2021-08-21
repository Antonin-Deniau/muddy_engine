import bcrypt
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.exceptions import ClientEx
from core.persist import Base, session


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    nickname = Column(String)
    password = Column(String)
    salt = Column(String)
    
    characters = relationship("Character", back_populates="user")

    def verify_password(self, password):
        pwhash = bcrypt.hashpw(password.encode("utf-8"), self.salt)
        return self.password == pwhash

    def __repr__(self):
       return "<User(name='{}', fullname='{}', nickname='{}')>".format(self.name, self.email, self.nickname)


class UserService:
    def __init__(self):
        self.session = session

    def fetch_user(self, name):
        return self.session.query(User).filter(User.name == name).one_or_none()

    def generate_password(self, p, salt):
        return bcrypt.hashpw(p.encode("utf-8"), salt)
    
    def name_exist(self, name):
        return self.session.query(User.id).filter_by(name=name).first() is not None

    def email_exist(self, email):
        return self.session.query(User.id).filter_by(email=email).first() is not None

    def create_user(self, name, email, password, nick):
        if self.email_exist(email):
            raise ClientEx("Email already exist")

        if self.name_exist(name):
            raise ClientEx("Name already exist")

        salt = bcrypt.gensalt(rounds=16)

        user = User(name=name, email=email, salt=salt, password=self.generate_password(password, salt), nickname=nick)
        self.session.add(user)
        self.session.commit()
        return user


user_service = UserService()
