from trello.db.session import session
from trello.db.models.entity import Entity
from trello.db.models.param import Param
from trello.db.models.route import Route

DEF_EXPR = 'Default: '
OPT_EXPR = ' (optional)'
REQ_EXPR = ' (required)'


class ParamLine:
    """Line in the file that corresponds to a param."""
    def __init__(self, param_name, is_required, default_value, line_number):
        self.param_name = param_name
        self.is_required = is_required
        self.default_value = default_value
        self.line_number = line_number


def get_default_value(file_lines, index):
    default_value = ''
    next_line = str(file_lines[index + 1])
    if DEF_EXPR in next_line:
        default_value = next_line.replace(DEF_EXPR, '')
    return default_value


def get_param_lines(file_lines):
    param_lines = []
    for index, file_line in enumerate(file_lines):
        file_line = str(file_line)
        is_optional = OPT_EXPR in file_line
        is_required = REQ_EXPR in file_line
        is_param = is_optional or is_required
        if is_param:
            param_name = file_line \
                .replace(OPT_EXPR, '') \
                .replace(REQ_EXPR, '')
            default_value = get_default_value(file_lines, index)
            param_line = ParamLine(param_name, is_required, default_value,
                                   index + 1)
            param_lines.append(param_line)
    return param_lines


def get_next_line_number(param_lines, index):
    next_line_number = 0
    try:
        next_line_number = param_lines[index + 1].line_number
    except IndexError:
        pass
    return next_line_number


def save_all_params(entity, file_lines):
    param_lines = get_param_lines(file_lines)
    param_records = []
    for index, param_line in enumerate(param_lines):
        end_line = get_next_line_number(param_lines, index)
        if end_line == 0:
            end_line = len(file_lines)
        param_to_add = Param(route_id=1,
                             entity_id=entity.id,
                             name=param_line.param_name,
                             is_required=param_line.is_required,
                             default_value=param_line.default_value,
                             start_line=param_line.line_number,
                             end_line=end_line - 1)
        session.add(param_to_add)
        param_records.append(param_to_add)
    session.commit()
    return


def assign_params_to_routes():
    entities = session.query(Entity).all()
    for entity in entities:
        routes = session.query(Route). \
            filter(Route.entity_id == entity.id)
        params = session.query(Param). \
            filter(Param.entity_id == entity.id)
        for route in routes:
            for param in params:
                is_lower_bound = param.start_line >= route.start_line
                is_upper_bound = param.start_line <= route.end_line
                if is_lower_bound and is_upper_bound:
                    param.route_id = route.id
    session.commit()
    return


def fix_params():
    params = session.query(Param).all()
    for index, param in enumerate(params):
        try:
            first_param = param
            next_param = params[index + 1]
            if first_param.route_id != next_param.route_id:
                current_end_line = first_param.end_line
                first_param.end_line = current_end_line - 2
        except IndexError:
            pass
        continue
    session.commit()
    return


def populate_params_table(entity, file_lines):
    save_all_params(entity, file_lines)
    assign_params_to_routes()
    fix_params()
    return
