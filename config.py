# config.py
import os

class Config:
    SECRET_KEY = 'supersecreto123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
