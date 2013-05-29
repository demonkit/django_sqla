# -*- coding: utf-8 -*-

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Language(Base):
    __tablename__ = 'languages'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    extension = Column(String(200))

    def __init__(self, name, extension):
        self.name = name
        self.extension = extension

    def __repr__(self):
        return u"Language(%s, %s)" % (self.name, self.extension)
