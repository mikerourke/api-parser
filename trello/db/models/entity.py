from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from trello.db.models.base import Base


class Entity(Base):
    __tablename__ = 'entities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)

    routes = relationship('Route', backref='entities')
