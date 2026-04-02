class R2Vector:
    def __init__(self, *, x, y):
        """2D Vector class"""
        self.x = x
        self.y = y

    def norm(self):
        """find the values of the vector which has a magnitude of 1"""
        return sum(val**2 for val in vars(self).values())**0.5

    def __str__(self):
        """return the vector in (x,y) form"""
        return str(tuple(getattr(self, i) for i in vars(self)))

    def __repr__(self):
        """return the vector in R2Vector(x,y) form"""
        arg_list = [f'{key}={val}' for key, val in vars(self).items()]
        args = ', '.join(arg_list)
        return f'{self.__class__.__name__}({args})'

    def __add__(self, other):
        """add two vectors assuming theyre both vectors"""
        if type(self) != type(other):
            return NotImplemented
        kwargs = {i: getattr(self, i) + getattr(other, i) for i in vars(self)}
        return self.__class__(**kwargs)

    def __sub__(self, other):
        """subtract two vectors assuming theyre both vectors"""
        if type(self) != type(other):
            return NotImplemented
        kwargs = {i: getattr(self, i) - getattr(other, i) for i in vars(self)}
        return self.__class__(**kwargs)

    def __mul__(self, other):
        """multiply two vectors or multiply a scalar and a vector"""
        if type(other) in (int, float): # scalar
            kwargs = {i: getattr(self, i) * other for i in vars(self)}
            return self.__class__(**kwargs)        
        elif type(self) == type(other): # vector
            args = [getattr(self, i) * getattr(other, i) for i in vars(self)]
            return sum(args)            
        return NotImplemented
    
    def __truediv__(self, other):
        """divide a vector by a scalar"""
        if type(other) in (int, float):
            kwargs = {i: getattr(self, i) / other for i in vars(self)}
            return self.__class__(**kwargs)
        return NotImplemented

    def __eq__(self, other):
        """equate two vectors"""
        if type(self) != type(other):
            return NotImplemented
        return all(getattr(self, i) == getattr(other, i) for i in vars(self))
        
    def __ne__(self, other):
        """inequate two vectors"""
        return not self == other

    def __lt__(self, other):
        """check one vector is less than the other"""
        if type(self) != type(other):
            return NotImplemented
        return self.norm() < other.norm()

    def __gt__(self, other):
        """check one vector is greater than the other"""
        if type(self) != type(other):
            return NotImplemented
        return self.norm() > other.norm()

    def __le__(self, other):
        """check one vector is less than or equal to the other"""
        return not self > other

    def __ge__(self, other):
        """check one vector is greater than or equal to the other"""
        return not self < other