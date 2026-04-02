# imports
from vector import R2Vector

class Body:
    def __init__(self, name:str, mass:int, position:R2Vector, velocity:R2Vector, radius=5, colour=(255,255,255)):
        """constructor for the body class"""
        self.name = name # default "Body"
        self.mass = mass 
        self.position = position
        self.velocity = velocity 
        self.radius = radius # default "5"
        self.colour = colour # default white

    def __str__(self):
        """returns the bodies name and position if the user prints the object"""
        return "\n".join(f"{k}: {v}" for k, v in self.__dict__.items())
    
    def __repr__(self):
        """returns the bodies name and position if the user prints the object"""
        return "\n".join(f"{k}: {v}" for k, v in self.__dict__.items())