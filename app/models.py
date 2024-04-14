from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Table, JSON, DateTime
from sqlalchemy.orm import relationship

from .database import Base

banner_tags = Table('banner_tags', Base.metadata,
    Column('banner_id', Integer, ForeignKey('banners.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Banner(Base):
    __tablename__ = "banners"

    id = Column(Integer, primary_key=True)
    feature_id = Column(Integer)
    tags = relationship('Tag', secondary=banner_tags, back_populates='banners')
    content = Column(JSON)
    is_active = Column(Boolean)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    banners = relationship('Banner', secondary=banner_tags, back_populates='tags')

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    is_admin = Column(Boolean)