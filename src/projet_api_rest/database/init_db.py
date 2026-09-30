from projet_api_rest.database.base import Base
from projet_api_rest.database.connection import engine
from projet_api_rest import models

def init_db() -> None:
    Base.metadata.create_all(bind=engine)