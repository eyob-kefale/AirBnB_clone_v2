#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship


place_amenity = Table(
        'place_amenity', Base.metadata,
        Column(
            'place_id',
            String(60),
            ForeignKey('places.id'),
            primary_key=True,
            nullable=False),
        Column(
            'aminity_id',
            String(60),
            ForeignKey('amenities.id'),
            primary_key=True,
            nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(
            String(60),
            ForeignKey('cities.id'),
            nullable=False)
    user_id = Column(
            String(60),
            ForeignKey('users.id'),
            nullable=False)
    name = Column(
            String(128),
            nullable=False)
    description = Column(
            String(1024),
            nullable=True)
    number_rooms = Column(
            Integer,
            nullable=False,
            default=0)
    number_bathrooms = Column(
            Integer,
            nullable=False,
            default=0)
    max_guest = Column(
            Integer,
            nullable=False,
            default=0)
    price_by_night = Column(
            Integer,
            nullable=False,
            default=0)
    latitude = Column(
            Float,
            nullable=True)
    longitude = Column(
            Float,
            nullable=True)
    amenity_ids = []

    if getenv('HBNB_TYPE_STORAGE', '') == 'db':
        reviews = relationship(
                'Review',
                backref='place',
                cascade='all, delete-orphan')
        amenities = relationship(
                'Amenity',
                secondary=place_amenity,
                backref='places',
                viewonly=False)
    else:
        @property
        def reviews(self):
            """ returns the list of Reviews instances with place_id
            equals to the current Place.id """
            rev = []
            for r in storage.all('Review').values():
                if self.id == r.place_id:
                    rev.append(r)
            return rev

        @property
        def amenities(self):
            """ returns the list of Amenity instances with place_id
            matching self.id """
            amn = []
            for a in storage.all('Amenity').values():
                if self.id == a.place_id:
                    amn.append(a)
            return amn

        @amenities.setter
        def amenities(self, obj):
            """ Adds id of object to list 'self.amenity_ids'
            if object is Amenity """
            if (type(obj) == 'Amenity'):
                self.amenity_ids.append(obj.id)
