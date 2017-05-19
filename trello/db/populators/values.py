"""
1. Loop through entities
2. Get file for each entity
3. Query all params associated with the entity
4. Loop through each Param and:
    for line_number in range(start_line, end_line)
        value_line = file_lines[line_number]
        if 'Default:' not in value_line and 'Values:' not in value_line:
            value_to_add = Value(param_id=param.id,
                                 value=value_line,
                                 line_number=line_number)
            session.add(value_to_add)
"""

from trello.db.session import session
from trello.db.models.param import Param
from trello.db.models.value import Value


def is_valid_value(line_value):
    is_valid = False
    if 'Default: ' not in line_value and \
            'Values:' not in line_value and \
            '(' not in line_value and \
            '/1' not in line_value and \
            'permissions:' not in line_value and \
            '.' not in line_value and \
            '[' not in line_value and \
            ']' not in line_value and \
            'Arguments' not in line_value:
        is_valid = True
    return is_valid

def save_all_values(entity, file_lines):
    params = session.query(Param). \
        filter(Param.entity_id == entity.id)
    value_records = []
    for param in params:
        line_start = param.start_line - 1
        line_end = param.end_line - 1
        for index in range(line_start, line_end):
            line_value = str(file_lines[index])
            if is_valid_value(line_value):
                value_to_add = Value(param_id=param.id,
                                     entity_id=entity.id,
                                     value=line_value,
                                     line_number=index + 1)
                session.add(value_to_add)
                value_records.append(value_to_add)
    session.commit()
    return


def populate_values_table(entity, file_lines):
    save_all_values(entity, file_lines)
    return
