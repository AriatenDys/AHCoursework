# imports
from sql_commands import * 
from body import *

# connect to the db
print('connecting to db...')
print('connecting to db..')
print('connecting to db.')
print('connecting to db..')
print('connecting to db...')

# instantiate the db class and delete everything in the database
db = PlanetDB()
print('connected to db!')
db.delete_all_planets()

print('cleared db contents!')

# gather all planets in the database, just in case some never got deleted
db.get_all_planets()

# set up array for default settings
planets = []
for pdata in db.get_all_planets():
    # append planets to the array
    planets.append(Body(
        name=pdata["name"],
        mass=pdata["mass"],
        position=pdata["position"],
        velocity=pdata["velocity"],
        radius=pdata["radius"],
        colour=pdata["colour"]
    ))
    
# loop the array and display data
for planet in planets:
    print(f"{planet.name}: pos=({planet.position.x}, {planet.position.y}), vel=({planet.velocity.x}, {planet.velocity.y})")

# close db connection
db.close_db()
