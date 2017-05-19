"""
This module extrapolates the routes from the entity files and writes them
to the "routes" table in the database.
"""
from trello.db.session import session
from trello.db.models.route import Route

current_entity = None

PERM_EXPR = 'Required permissions: '


class RouteLine:
    """Line in the file that corresponds to a route."""
    def __init__(self, file_line, line_number):
        self.file_line = file_line
        self.line_number = line_number


class RouteDescriptor:
    """Elements of a route pulled from the route line in the file."""
    def __init__(self, method, url):
        self.method = method
        self.url = url


def get_permissions(file_lines, route_line, method):
    """
    Extrapolates the permissions from the file based on the line number of the
    route line.  The permissions are normally the next line down from the
    line containing the route.
    :param file_lines: List of lines from the entity file.
    :param route_line: Line containing route definition.
    :param method: HTTP verb associated with route.
    :return: A string representing the permissions for the specified route.
    """
    perm_line_num = int(route_line.line_number) + 1
    expected_line = file_lines[perm_line_num]
    permissions = ''
    # The permissions in the file are in this format:
    # "Required permissions: write"
    if PERM_EXPR in expected_line:
        permissions = expected_line.replace(PERM_EXPR, '')

    # No permissions were associated with the route.  For the most part,
    # any method other than "GET" requires "write" permissions:
    if permissions == '':
        if method == 'GET':
            permissions = 'read'
        else:
            permissions = 'write'

    return permissions


def get_sanitized_route(route_line):
    """
    Cleans the route path, extrapolates the method, and returns an object
    containing the method and URL of the route line.
    :param route_line: File line containing route information.
    :return: Instance of RouteDescriptor class with method and URL.
    """
    file_line = str(route_line.file_line)
    clean_file_line = file_line \
        .replace('idMember or username', 'memberId') \
        .replace('card id or shortlink', 'cardId') \
        .replace('board_id', 'idBoard') \
        .replace('[', ':') \
        .replace(']', '') \
        .replace('board_id', 'idBoard') \
        .replace(':cardId', ':idCard') \
        .replace(':memberId', ':idMember')
    file_elements = clean_file_line.split(' ')
    route_descriptor = RouteDescriptor(file_elements[0], file_elements[1])
    return route_descriptor


def get_route_lines(file_lines):
    """
    Loops through files and builds a list of file lines containing route paths.
    :param file_lines: List of lines in the file.
    :return: List of lines containing routes.
    """
    http_verbs = ['DELETE', 'GET', 'POST', 'PUT']
    route_lines = []
    line_number = 1
    for file_line in file_lines:
        first_word = str(file_line.split(' ')[0])
        if first_word in http_verbs:
            route_line = RouteLine(file_line, line_number)
            route_lines.append(route_line)
        line_number += 1
    return route_lines


def get_next_line_number(route_lines, index):
    next_line_number = 0
    try:
        next_line_number = route_lines[index + 1].line_number
    except IndexError:
        pass
    return next_line_number


def save_routes_for_entity(file_lines):
    """
    Extrapolates the route lines from the entity file, creates a new row in the
    database for the route, and commits the changes.
    """
    route_lines = get_route_lines(file_lines)
    for index, route_line in enumerate(route_lines):
        sanitized_route = get_sanitized_route(route_line)
        method = sanitized_route.method
        url = sanitized_route.url
        permissions = get_permissions(file_lines, route_line, method)
        end_line = get_next_line_number(route_lines, index)
        if end_line == 0:
            end_line = len(file_lines)
        route_to_add = Route(entity_id=current_entity.id,
                             url=url,
                             method=method,
                             permissions=permissions,
                             start_line=route_line.line_number,
                             end_line=end_line - 1)
        session.add(route_to_add)
    session.commit()
    return


def populate_routes_table(entity, file_lines):
    global current_entity
    current_entity = entity
    save_routes_for_entity(file_lines)
    return
