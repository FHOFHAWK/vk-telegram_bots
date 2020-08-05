from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


# Подключение к БД
def get_connection():
    engine = create_engine('postgresql+psycopg2://postgres:123456789@localhost/postgres')
    return engine


def get_sqlalchemy_session():
    sqlalchemy_session = sessionmaker(bind=get_connection())
    session = sqlalchemy_session()
    return session


if __name__ == '__main__':
    pass
