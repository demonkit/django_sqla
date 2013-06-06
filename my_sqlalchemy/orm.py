# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

import settings


engine = create_engine(settings.DB_ENGINE, echo=True)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(100))
    password = Column(String(100))

    # not actually needed
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return u"<User ('%s', '%', '%s')>" % (self.name, self.fullname, self.password)


Base.metadata.create_all(engine)

ed_user = User('ed', 'Ed Jones', 'edpassword')
print ed_user.name, ed_user.password, ed_user.id

# session
Session = sessionmaker(bind=engine)
# or
Sesstion = sessionmaker()
Session.configure(bind=engine)

# add new object
# ed_user = User('ed', 'Ed Jones', 'edpassword')
session.add(ed_user)

our_user = session.query(User).filter_by(name='ed').first()
print our_user

print our_user is ed_user

session.add_all([
    User('wendy', 'Wendy Williams', 'foobar'),
    User('mary', 'Mary Contrary', 'xxg527'),
    User('fred', 'Fred Flinstone', 'blah')])

# change
ed_user.password = 'f8kskxos'
print session.dirty
# 3 new pending
print session.new

session.commit()


# roll backs
ed_user.name = 'Edwardo'
fake_user = User('fakeuser', 'Invalid', '12345')
session.add(fake_user)

print session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all()
session.rollback()
print session.query(User).filter(User.name.in_(['ed', 'fakeuser'])).all()

# query
for instance in session.query(User).order_by(User.id):
    print instance.name, instance.fullname

# count
print session.query(User).filter(User.name.like("%ed")).count()

# TODO
