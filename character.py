from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from persist import Base, Session

class C(Base):
    def __init__(self, world, name):
        self.previous_location = None
        self.location = world.get_metadata("entrypoint")
        self.world = world
        self.name = name
        self.action = None

    def move(self, new_location):
        self.previous_location = self.location
        self.location = new_location


class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    user = relationship("User")

    def verify_password(self, password):
        pwhash = bcrypt.hashpw(password, self.password)
        return self.password == pwhash

    def __repr__(self):
       return "<User(name='{}', fullname='{}', nickname='{}')>".format(self.name, self.email, self.nickname)


class CharacterRepository:
    def __init__(self):
        self.session = Session()
        self.salt = bcrypt.gensalt(rounds=16)

    def fetch_user(self, user):
        return self.session.query(Player).filter(Player.user == user).all()

    def generate_password(self, p):
        return bcrypt.hashpw(p.encode("utf-8"), self.salt)

    def create_user(self, name, email, password, nick):
        user = User(name=name, email=email, password=self.generate_password(password), nickname=nick)
        self.session.add(user)
        self.session.commit()
        return user


user_repository = UserRepository()
