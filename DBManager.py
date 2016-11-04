from sqlalchemy import *


DB_DIALECT = ''
DB_DRIVER = 'mysql'
DB_USERNAME = 'root'
DB_PASSWORD = ''
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_DATABASE = 'assessment'


db = create_engine(DB_DIALECT+DB_DRIVER+ '://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST + ':' + DB_PORT +
                       '/' + DB_DATABASE)

db.echo = False
