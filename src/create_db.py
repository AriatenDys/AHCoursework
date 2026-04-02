# imports
from sql_commands import * 
from body import *

# connect to the db
print('connecting to db...')
print('connecting to db..')
print('connecting to db.')
print('connecting to db..')
print('connecting to db...')

# instantiate the db object and create the table
db = PlanetDB()
print('connected to db!')
db.create_table()

print('created db table!')

# close the db connection
db.close_db()
