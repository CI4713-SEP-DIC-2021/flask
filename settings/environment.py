import os
import sqlite3

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DB_URI = "sqlite:///" + BASE_DIR + "/database/backlog_usb.db"
APP_SETTINGS = "config.DevelopmentConfig"
