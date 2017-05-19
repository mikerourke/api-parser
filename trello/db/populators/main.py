from trello.files import get_file_contents
from trello.db.models.entity import Entity
from trello.db.session import session

from trello.db.populators.entities import populate_entities_table
from trello.db.populators.params import populate_params_table
from trello.db.populators.routes import populate_routes_table
from trello.db.populators.values import populate_values_table


def populate_db():
    populate_entities_table()
    entities = session.query(Entity).all()
    for entity in entities:
        file_contents = get_file_contents(entity.name + '.txt')
        file_lines = file_contents.split('\n')
        populate_routes_table(entity, file_lines)
        populate_params_table(entity, file_lines)
        populate_values_table(entity, file_lines)
        print('Completed ' + entity.name)
    return
