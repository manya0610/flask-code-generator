class DatabaseScriptGenerator:
    project_name: str

    def __init__(self, project_name):
        self.project_name = project_name

    def database_script_generator(self):
        return """

import subprocess
import sys

from sqlalchemy_utils import create_database, database_exists, drop_database

from database import engine


def create_db():
    if not database_exists(engine.url):
        print("database doesn't exist, creating it")
        create_database(engine.url)
        print("database created")
    else:
        print("database already exists, dropping it")
        drop_database(engine.url)
        print("database dropped, now creating it")
        create_database(engine.url)
        print("database created")
    engine.dispose()


def drop_db():
    if not database_exists(engine.url):
        print("database doesn't exist")
        raise Exception("database doesn't exist")
    drop_database(engine.url)
    print("database dropped")


def create_tables():
    subprocess.run(["alembic", "upgrade", "head"])


print("argument list", sys.argv)

for arg in sys.argv[1:]:
    if arg == "create_db":
        create_db()
    elif arg == "drop_db":
        drop_db()
    elif arg == "create_tables":
        create_tables()
    # elif arg == "create_user":
    #     create_user()
    else:
        print("invalid arg", arg)

"""
