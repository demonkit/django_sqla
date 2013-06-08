# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import select, text, and_, or_, not_, bindparam, func

import settings


engine = create_engine(settings.DB_ENGINE, echo=True)


metadata = MetaData()
users = Table('users', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(50)),
        Column('fullname', String(100)),)
addresses = Table('addresses', metadata,
        Column('id', Integer, primary_key=True),
        Column('user_id', None, ForeignKey('users.id')),
        Column('email_address', String(100), nullable=False),)

metadata.create_all(engine)


conn = engine.connect()

# unusually used way
ins1 = users.insert().values(name='jack', fullname='Jack Jones')
print str(ins1)
print ins1.compile().params

result1 = conn.execute(ins1)
print result


# a normal way
ins2 = users.insert()
print str(ins2)
result2 = conn.execute(ins2, id=2, name='wendy', fullname='Wendy Williams')
print result2


# addresses
conn.execute(addresses.insert(), [
    {'user_id': 1, 'email_address': 'jack@yahoo.com'},
    {'user_id': 1, 'email_address': 'jack@msn.com'},
    {'user_id': 2, 'email_address': 'www@www.org'},
    {'user_id': 2, 'email_address': 'wendy@msn.com'},
])


# select
s = select([users])
result = conn.execute(s)
for row in result:
    print row
    print row[0], row['name'], row.fullname
    print
result.close()

# some rows
s = select([users.c.name])
result = conn.execute(s)
print result.fetchone()
print '-----------------------------------'
result.close()


# where
s = select([users, addresses]).where(users.c.id == addresses.c.user_id)
for row in conn.execute(s):
    print row
print '-----------------------------------'

# where clause
print type(users.c.id == addresses.c.user_id)
print str(users.c.id == addresses.c.user_id)
print '-----------------------------------'


# text
s = text("""
        select users.fullname, addresses.email_address as title
        from users, addresses
        where users.id = addresses.user_id
        and users.name between :x and :y
        and (addresses.email_address like :e1 or addresses.email_address like :e2)
        """)
print conn.execute(s, x='m', y='z', e1='%@aol.com', e2='%@msn.com').fetchall()
print '-----------------------------------'

# same
s = select(['users.fullname, addresses.email_address as title']).where(
        and_(
            'users.id = addresses.user_id',
            'users.name between "m" and "z"',
            '(addresses.email_address like :x or addresses.email_address like :y)'
        )
        ).select_from('users, addresses')
print conn.execute(s, x='%@aol.com', y='%@msn.com').fetchall()
print '-----------------------------------'

# bind own parameter
s = users.select(users.c.name == bindparam('username'))
print conn.execute(s, username='wendy').fetchall()
print '-----------------------------------'

s = users.select(users.c.name.like(bindparam('username', type_=String) + text("'%'")))
print conn.execute(s, username='wendy').fetchall()
print '-----------------------------------'


# fuctions
print func.now()
print func.concat('x', 'y')
print '-----------------------------------'
