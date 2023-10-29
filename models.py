from database import Base, engine
from sqlalchemy import Integer, String, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker, registry
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Session = sessionmaker(bind=engine)
session = Session()

mapper_registry = registry()
mapper_registry.configure()

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)

    username = Column(String)
    password = Column(String)
    email = Column(String)
    # date_published = Column(DateTime, default=datetime.now())

    blogs = relationship("Blog", back_populates="owner")


class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    body = body = Column(String)
    date_published = Column(DateTime, default=datetime.now())
    url = Column(String)

    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="blogs")
