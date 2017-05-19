from sqlalchemy import Column, Boolean, Integer, String, ForeignKey

from trello.db.models.base import Base


class Value(Base):
    __tablename__ = 'values'

    id = Column(Integer, primary_key=True, autoincrement=True)
    param_id = Column(Integer, ForeignKey('params.id'))
    entity_id = Column(Integer)
    value = Column(String)
    line_number = Column(Integer)
