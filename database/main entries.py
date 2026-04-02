import math
import random
from pathlib import Path

# -------------------------
# paths
# -------------------------
BASE_DIR = Path(__file__).resolve().parent
SQL_FILE = BASE_DIR / "text.sql"

# -------------------------
# constants / config
# -------------------------
NUM_PLANETS = 10            # how many new main planets to generate
MASS_RANGE = (5.0, 100.0)   # min/max mass
POSITION_RANGE = (-4000, 4000)  # x and y coordinates
VELOCITY_RANGE = (-90.0, 90.0)    # vx, vy range
RADIUS_RANGE = (4.0, 20.0)      # radius range
G = 1.0                          # gravitational constant (optional if using circular velocity)
COLOUR_RANGE = (50, 255)         # RGB range

# -------------------------
# helper to generate a planet
# -------------------------
def generate_planet(index):
    name = str(index)
    mass = random.uniform(*MASS_RANGE)
    px = random.uniform(*POSITION_RANGE)
    py = random.uniform(*POSITION_RANGE)
    
    # velocity for circular-ish orbit around origin (rough approximation)
    dx = -px
    dy = -py
    distance = math.hypot(dx, dy) + 1e-6  # avoid zero
    v_mag = math.sqrt(G * mass / distance) if distance != 0 else 0.0
    vx = 20 * -v_mag * dy / distance 
    vy = 20 * v_mag * dx / distance
    
    radius = random.uniform(*RADIUS_RANGE)
    r = random.randint(*COLOUR_RANGE)
    g = random.randint(*COLOUR_RANGE)
    b = random.randint(*COLOUR_RANGE)
    
    return f"('{name}', {mass:.3f}, {px:.3f}, {py:.3f}, {vx:.3f}, {vy:.3f}, {radius:.3f}, {r}, {g}, {b})"

# -------------------------
# generate all planets
# -------------------------
all_entries = [generate_planet(i) for i in range(1, NUM_PLANETS)]  # starting at 101 to avoid name conflicts

# -------------------------
# append to SQL file
# -------------------------
with open(SQL_FILE, "a") as f:
    f.write("\n-- newly generated main planets\nINSERT OR IGNORE INTO planets (name, mass, px, py, vx, vy, radius, colour_r, colour_g, colour_b) VALUES\n")
    f.write(",\n".join(all_entries) + ";\n")

print(f"Successfully generated {NUM_PLANETS} main planets and appended to {SQL_FILE}")