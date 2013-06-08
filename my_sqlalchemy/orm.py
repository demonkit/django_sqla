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

# query filter operations
# equals: ==, not equals: !=, like,
# in: in_, not in: ~..in_, is null: ==None, is not null: != None,
# and: and_, or match

# count
print session.query(User).filter(User.name.like("%ed")).count()


# literal sql
for user in session.query(User).filter("id<1234").order_by("id").all():
    print user.name
print


# from statement
print session.query("id", "name", "thenumber12").\
        from_statement("select id, name, 12 as thenumber12 "
                "from users where name=:name").params(name="ed").all()
print


# relationship
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    # we can use User.addresses to get a user's address collection
    user = relationship("User", backref=backref('addresses', order_by=id))
    # or we can put this code below in the class User:
    # addresses = relationship("Address", order_by="Address.id", backref="user")

    def __init__(self, email_address):
        self.email_address = email_address

    def __repr__(self):
        return "<Address('%s')>" % self.email_address

# create the new table
Base.metadata.create_all(engine)


# insert some records
jack = User('jack', 'Jack Bean', 'gkshk')
print jack.addresses

jack.addresses = [
        Address(email_address="jack@google.com"),
        Address(email_address="jack@yahoo.com"),
    ]
# add
session.add(jack)
session.commit()
