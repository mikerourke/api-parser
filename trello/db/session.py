from sqlalchemy.orm import sessionmaker

from trello.db.engine import engine

Session = sessionmaker(bind=engine)
session = Session()

