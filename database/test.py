try:
    import sqlite3
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "sqlite3"])
    import sqlite3
from vector import R2Vector 
from settings import *

class PlanetDB:
    def __init__(self, db_path="planets.db"):
        self.db_path = db_path
        self.cx = sqlite3.connect(self.db_path)
        self.cu = self.cx.cursor()
        self.create_table()

    def __del__(self):
        if hasattr(self, "cx"):
            self.close_db()

    def __str__(self):
        if self.cx is None:
            return "Database status: Closed"
        else:
            return "Database status: Open"

    def create_table(self):
        """create the planets table if it doesn't exist"""
        self.cu.execute("""
            CREATE TABLE IF NOT EXISTS planets(
                name TEXT PRIMARY KEY,
                mass REAL,
                px REAL,
                py REAL,
                vx REAL,
                vy REAL,
                radius REAL,
                colour_r INTEGER,
                colour_g INTEGER,
                colour_b INTEGER
            )
        """)
        self.cx.commit()

    def insert_planet(self, name, mass, pos, vel, radius=5, colour=(255, 255, 255)):
        """insert a new planet object"""
        self.cu.execute("""
            INSERT OR REPLACE INTO planets
            (name, mass, px, py, vx, vy, radius, colour_r, colour_g, colour_b)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, mass, pos.x, pos.y, vel.x, vel.y, radius, *colour))
        self.cx.commit()

    def get_all_planets(self):
        """fetch all planets as a list of dictionaries"""
        try:
            self.cu.execute("SELECT * FROM planets")
            planets = []
            for row in self.cu.fetchall():
                planets.append({
                    "name": row[0],
                    "mass": row[1],
                    "position": R2Vector(x=row[2], y=row[3]),
                    "velocity": R2Vector(x=row[4], y=row[5]),
                    "radius": row[6],
                    "colour": (row[7], row[8], row[9])
                })
            return planets
        except Exception as e:
            print("database error:", e)
            return []

    def delete_planet(self, name):
        """delete a planet by name"""
        self.cu.execute("DELETE FROM planets WHERE name = ?", (name,))
        self.cx.commit()

    def delete_all_planets(self, physics_system=None):
        """delete all planets from DB and remove them from the simulation"""
        self.cu.execute("DELETE FROM planets")
        self.cx.commit()

        # if a physics system is passed in, remove all planets except the sun
        if physics_system:
            physics_system.bodies = [b for b in physics_system.bodies if b.name == "sun"]

    def close_db(self):
        """close the database connection"""
        if self.cx:
            self.cx.close()
            self.cx = None
            self.cu = None
