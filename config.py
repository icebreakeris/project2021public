import os

class DevelopmentConfig(object):
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = b'\x88\x15\x8fR\x87f;\x8aG\xf4\xd7\xe1\xdf\x87\x92T\x02!x^\xd7\xe1b\xbd'
    DB_NAME = "dev_database.db"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(object):
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = b'v&\x83\xc0\xe90a\x01\xb8\x8c\x07\x89\\\xb6\xb8\x8d\x8e\xdeH\xabe\xd70\xcd'
    DB_NAME = "prod_database.db"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_NAME}"
    SQL_ALCHEMY_TRACK_MODIFICATIONS = False
