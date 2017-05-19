from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from trello.db.models.base import Base


class Route(Base):
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(Integer, ForeignKey('entities.id'))
    url = Column(String)
    method = Column(String)
    permissions = Column(String)
    description = Column(String)
    start_line = Column(Integer)
    end_line = Column(Integer)

    params = relationship('Param', backref='routes')
