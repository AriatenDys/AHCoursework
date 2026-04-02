import math
import random
from pathlib import Path
import re

# -------------------------
# paths
# -------------------------
BASE_DIR = Path(__file__).resolve().parent
SQL_FILE = BASE_DIR / "text.sql"

# -------------------------
# constants
# -------------------------
G = 1.0  # gravitational constant for simulation
NUM_SATELLITES = 10

# -------------------------
# helper: parse planets from SQL file
# -------------------------
def parse_planets(sql_file):
    planets = []
    pattern = re.compile(
        r"\(\s*'(?P<name>[^']+)'\s*,\s*(?P<mass>[\d\.]+)\s*,\s*(?P<px>[-\d\.]+)\s*,\s*(?P<py>[-\d\.]+)\s*,\s*(?P<vx>[-\d\.]+)\s*,\s*(?P<vy>[-\d\.]+)\s*,\s*(?P<radius>[\d\.]+)\s*,\s*(?P<r>\d+)\s*,\s*(?P<g>\d+)\s*,\s*(?P<b>\d+)\s*\)"
    )
    with open(sql_file, "r") as f:
        content = f.read()
    for match in pattern.finditer(content):
        pdata = match.groupdict()
        pdata = {k: float(v) if k not in ("name",) else v for k, v in pdata.items()}
        pdata["colour"] = (int(pdata.pop("r")), int(pdata.pop("g")), int(pdata.pop("b")))
        pdata["position"] = (pdata.pop("px"), pdata.pop("py"))
        pdata["velocity"] = (pdata.pop("vx"), pdata.pop("vy"))
        planets.append(pdata)
    return planets

# -------------------------
# generate satellites
# -------------------------
planets = parse_planets(SQL_FILE)
all_entries = []

for pdata in planets:
    pname = pdata["name"]
    pmass = pdata["mass"]
    px, py = pdata["position"]
    pr, pg, pb = pdata["colour"]
    
    for i in range(1, NUM_SATELLITES + 1):
        # random offset
        r = random.uniform(5.0, 15.0)
        angle = random.uniform(0, 2*math.pi)
        sat_px = px + r * math.cos(angle)
        sat_py = py + r * math.sin(angle)
        
        # circular orbit velocity
        v = math.sqrt(G * pmass / r)
        vx = -v * math.sin(angle)
        vy = v * math.cos(angle)
        
        # satellite mass and radius
        smass = pmass * random.uniform(0.01, 0.05)
        sradius = max(1.0, smass)
        
        # dimmed colour
        cr, cg, cb = [max(0, min(255, int(c*0.8))) for c in (pr, pg, pb)]
        
        # satellite name
        sname = f"{pname}-{i}"
        
        # create entry
        entry = f"('{sname}', {smass:.3f}, {sat_px:.3f}, {sat_py:.3f}, {vx:.3f}, {vy:.3f}, {sradius:.3f}, {cr}, {cg}, {cb})"
        all_entries.append(entry)

# -------------------------
# append to SQL file
# -------------------------
with open(SQL_FILE, "a") as f:
    f.write("\n-- satellites for all planets\nINSERT OR IGNORE INTO planets (name, mass, px, py, vx, vy, radius, colour_r, colour_g, colour_b) VALUES\n")
    f.write(",\n".join(all_entries) + ";\n")

print(f"Successfully generated {NUM_SATELLITES * len(planets)} satellites and appended to {SQL_FILE}")