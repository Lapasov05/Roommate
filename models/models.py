
from sqlalchemy import (
    Column, ForeignKey, Integer, String,
    Text, TIMESTAMP,
    MetaData, Boolean, Float
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()
metadata = MetaData()


class University(Base):
    __tablename__ = 'university'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    acronym = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)

    faculty = relationship('Faculty', back_populates='university')
    user = relationship('User', back_populates='university')


class Faculty(Base):
    __tablename__ = 'faculty'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    university_id = Column(Integer, ForeignKey("university.id"))
    longitude = Column(Float)
    latitude = Column(Float)

    university = relationship('University', back_populates='faculty')
    user = relationship('User', back_populates='faculty')


class Region(Base):
    __tablename__ = 'region'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    district = relationship('District', back_populates='region')


class District(Base):
    __tablename__ = 'district'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    region_id = Column(Integer, ForeignKey('region.id'))

    region = relationship('Region', back_populates='district')


class Jins(Base):
    __tablename__ = 'jins'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    user = relationship('User', back_populates='jins')
    rent = relationship('Rent', back_populates='jins')


class User(Base):
    __tablename__ = 'user'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String)
    lastname = Column(String)
    phone = Column(String)
    jins_id = Column(Integer, ForeignKey('jins.id'))
    university_id = Column(Integer, ForeignKey("university.id"))
    faculty_id = Column(Integer, ForeignKey('faculty.id'))
    grade = Column(Integer)
    password = Column(String)
    image = Column(String)
    invisible = Column(Boolean, default=False)
    district_id = Column(Integer, ForeignKey("district.id"))
    register_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC))

    university = relationship('University', back_populates='user')
    faculty = relationship('Faculty', back_populates='user')
    district = relationship('District', back_populates='user')
    wishlist = relationship('Wishlist', back_populates='user')
    like = relationship('Like', back_populates='user')
    jins = relationship('Jins', back_populates='user')


class Renter(Base):
    __tablename__ = 'renter'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String)
    lastname = Column(String)
    phone = Column(String, unique=True)
    password = Column(String)
    image = Column(String)
    register_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC))

    rent = relationship('Renter', back_populates='renter')


class Category(Base):
    __tablename__ = 'category'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    rent = relationship('Rent', back_populates='category')


class Rent(Base):
    __tablename__ = 'rent'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(Text)
    room_count = Column(Integer)
    total_price = Column(Float)
    student_jins_id = Column(Integer, ForeignKey('jins.id'))
    student_count = Column(Integer)
    renter_id = Column(Integer, ForeignKey('renter.id'))
    location = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)
    wifi = Column(Boolean)
    conditioner = Column(Boolean)
    washing_machine = Column(Boolean)
    TV = Column(Boolean)
    refrigerator = Column(Boolean)
    furniture = Column(Boolean)
    other_convenience = Column(Text)

    like = relationship("Like", back_populates='rent')
    wishlist = relationship("Wishlist", back_populates='rent')
    category = relationship("Category", back_populates='rent')
    jins = relationship('Jins', back_populates='rent')


class Rate(Base):
    __tablename__ = 'rate'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    rent_id = Column(Integer, ForeignKey('rent.id'))
    rate = Column(Integer)

    rent = relationship('Rent', back_populates='like')
    user = relationship('User', back_populates='like')


class Wishlist(Base):
    __tablename__ = 'wishlist'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    rent_id = Column(Integer, ForeignKey('rent.id'))

    rent = relationship('Rent', back_populates='wishlist')
    user = relationship('User', back_populates='wishlist')
