from sqlalchemy.sql import text
from trello.db.session import session

from trello.db.models.entity import Entity
from trello.db.models.param import Param
from trello.db.models.route import Route
from trello.db.models.value import Value


def get_all(table_name):
    sql = text('SELECT * FROM ' + table_name)
    results = session.execute(sql)
    for row in results:
        print(row)
    return
