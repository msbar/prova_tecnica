from sqlmodel import SQLModel, create_engine

import models


class ConnectionHandler:

    engine = None

    def __init__(self):
        self.sqlite_file_name = "combustivel.db"
        self.sqlite_url = f"sqlite:///{self.sqlite_file_name}"
        self.engine = create_engine(self.sqlite_url)

    def create_database(self):
        SQLModel.metadata.create_all(self.engine)
