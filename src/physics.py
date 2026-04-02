# imports
from vector import R2Vector
from utils import *
from body import Body
from self_defined_decorators import physics_log_call

class PhysicsSystem:
    def __init__(self, bodies: list, G: float = 0.1, dt: float = 0.5):
        """class to handle the physics of the simulation"""
        self.bodies = bodies
        self.G = G
        self.dt = dt
        self.epsilon = 0.1

    def compute_force(self, body, other):
        """method to use newtons inverse square law to calculate the force between two objects"""
        r_vec = other.position - body.position
        distance = r_vec.norm() # might actually run better to replace this with returning distance**2, to remove floating point approximation

        denom = distance**2 + self.epsilon**2
        force_mag = self.G * body.mass * other.mass / denom

        if distance == 0: # prevent division by zero
            return R2Vector(0, 0)
        
        unit_r = r_vec / distance
        return unit_r * force_mag

    def compute_forces(self):
        """method to calculate the vector sum of the forces on an object"""
        forces = {body: R2Vector(x=0, y=0) for body in self.bodies} # dictionary for body: force, default 0N

        for i, b1 in enumerate(self.bodies): # force calculations using newtons third law
            for j in range(i + 1, len(self.bodies)):
                b2 = self.bodies[j]

                f = self.compute_force(b1, b2)

                forces[b1] += f
                forces[b2] -= f  # equal and opposite

        return forces

    def integrate(self):
        """method to use a velocity verlet integration technique on objects using other methods from class"""
        forces = self.compute_forces()
        accelerations = {b: forces[b] / b.mass for b in self.bodies} # dictionary storing accelerations body: acceleration

        # calculate first half of velocity and position
        for b in self.bodies:
            b.velocity += accelerations[b] * (0.5 * self.dt)

        for b in self.bodies:
            b.position += b.velocity * self.dt

        forces = self.compute_forces()
        accelerations = {b: forces[b] / b.mass for b in self.bodies}

        # calculate second half of velocity
        for b in self.bodies:
            b.velocity += accelerations[b] * (0.5 * self.dt)

@physics_log_call
def physics_setup(db):
    """set up the physics for the entire simulation"""
    bodies = []

    for pdata in db.get_all_planets(): # sets up the bodies array using database data
        body = Body(name=pdata["name"], mass=pdata["mass"], position=pdata["position"], 
                    velocity=pdata["velocity"], radius=pdata["radius"], colour=pdata["colour"])
        bodies.append(body)

    if not any(b.name == "sun" for b in bodies): # ensures at least one sun exists in the array
        sun = Body(name="sun", mass=5e4, position=R2Vector(x=0, y=0), 
                   velocity=R2Vector(x=0, y=0), radius=15, colour=(255, 255, 0))
        bodies.insert(0, sun)

    # sort the data and return to main
    bubble_sort(bodies)

    return PhysicsSystem(bodies)
