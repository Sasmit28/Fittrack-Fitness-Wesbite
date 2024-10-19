# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgre:root@localhost/fittrack'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
