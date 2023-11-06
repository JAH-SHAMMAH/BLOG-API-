from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, engine
from sqlalchemy import Integer, String, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker, registry
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)

    username = Column(String)
    password = Column(String)
    email = Column(String)

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
    comments = relationship("Comments", back_populates="commenter")
    # category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="blogger")


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    comment = Column(String)

    comment_id = Column(Integer, ForeignKey("blogs.id"))
    commenter = relationship("Blog", back_populates="comments")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    body = Column(String)
    # owner = Column(String)
    date_published = Column(DateTime, default=datetime.now())

    category_id = Column(Integer, ForeignKey("blogs.id"))
    blogger = relationship("Blog", back_populates="category")
