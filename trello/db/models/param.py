from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from trello.db.models.base import Base


class Param(Base):
    __tablename__ = 'params'

    id = Column(Integer, primary_key=True, autoincrement=True)
    route_id = Column(Integer, ForeignKey('routes.id'))
    entity_id = Column(Integer)
    name = Column(String)
    is_required = Column(Boolean, default=False)
    default_value = Column(String)
    start_line = Column(Integer)
    end_line = Column(Integer)

    values = relationship('Value', backref='params')
