import trello.db.models.entity
import trello.db.models.route
import trello.db.models.param
import trello.db.models.value

from trello.db.models.base import Base
from trello.db.engine import engine


def initialize_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
