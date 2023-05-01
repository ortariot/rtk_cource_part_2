from config import SQLALCHEMY_DATABASE_URI
from servicedataloader import ServiceDataLoader


if __name__ == '__main__':
    data_laoder = ServiceDataLoader('input', SQLALCHEMY_DATABASE_URI)
