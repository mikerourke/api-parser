from trello.files import get_paths
from trello.db.models.entity import Entity
from trello.db.session import session


def get_entity_names():
    file_paths = get_paths()
    entity_names = []
    for fn in file_paths:
        path_elements = fn.split('/')
        entity_name = str(path_elements[-1]).replace('.txt', '')
        entity_names.append(entity_name)
    return entity_names


def populate_entities_table():
    names = get_entity_names()
    for name in names:
        entity_to_add = Entity(name=name)
        session.add(entity_to_add)

    session.commit()
    return
