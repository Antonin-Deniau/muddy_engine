import bcrypt
from sqlalchemy import Column, Integer, String
from persist import Base, Session
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    nickname = Column(String)
    password = Column(String)
    
    characters = relationship("Character", back_populates="user")

    def verify_password(self, password):
        pwhash = bcrypt.hashpw(password, self.password)
        return self.password == pwhash

    def __repr__(self):
       return "<User(name='{}', fullname='{}', nickname='{}')>".format(self.name, self.email, self.nickname)


class UserRepository:
    def __init__(self):
        self.session = Session()
        self.salt = bcrypt.gensalt(rounds=16)

    def fetch_user(self, name):
        return self.session.query(User).filter(User.name == name).one_or_none()

    def generate_password(self, p):
        return bcrypt.hashpw(p.encode("utf-8"), self.salt)

    def create_user(self, name, email, password, nick):
        user = User(name=name, email=email, password=self.generate_password(password), nickname=nick)
        self.session.add(user)
        self.session.commit()
        return user


user_repository = UserRepository()
