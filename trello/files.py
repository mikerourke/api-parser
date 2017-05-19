import os

source = './data/clean/'


def get_paths():
    """Loops through the 'clean' directory and returns an array of file paths"""
    file_paths = []
    for root, dirs, filenames in os.walk(source):
        for fn in filenames:
            full_path = os.path.join(source, fn)
            file_paths.append(full_path)
    return file_paths


def get_file_contents(file_name):
    """Gets the contents of the specified file from the 'clean' directory"""
    full_path = source + file_name
    file_contents = ''
    if os.path.isfile(full_path):
        text_file = open(full_path, 'r')
        file_contents = text_file.read()
        text_file.close()
    return file_contents
