from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

MESSAGE_MAX_TEXT_LENGTH = 65535


MIN_DATA_LENGTH, MAX_DATA_LENGTH = 3, 255
HASH_LENGTH = 128



