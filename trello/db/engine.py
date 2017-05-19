import os

from sqlalchemy import create_engine

# Ensure the database path is correct regardless of the working directory:
abs_path = os.path.dirname(os.path.abspath(__file__))
db_path = abs_path + '../../data/routes.db'

engine = create_engine('sqlite:///' + db_path, echo=False)
