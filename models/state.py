#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
import models
from models import *
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship(
            'City',
            backref='state',
            cascade='all, delete-orphan')

    if getenv('HBNB_TYPE_STORAGE', '') != 'db':
        @property
        def cities(self):
            """ return a list of City instances with state_id
            equals to the current State.id """
            all_cities = models.storage.all('City').values()
            tmp = []
            for city in all_cities:
                if city.state_id == self.id:
                    tmp.append(city)
            return tmp
