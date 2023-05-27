# IMPORT THE SQALCHEMY LIBRARY's CREATE_ENGINE METHOD
import sqlalchemy as db
import configparser

config = configparser.ConfigParser()
config.read('settings/utils.ini')

user = config['DBCredentials']['user']
password = config['DBCredentials']['password']
host = config['DBCredentials']['host']
port = config['DBCredentials']['port']
database = config['DBCredentials']['database']

engine = db.create_engine("mariadb+pymysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database))