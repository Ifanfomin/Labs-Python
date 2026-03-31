import math

class Circle:
    def __init__(self, radius):
        self._radius = radius
        
    @property
    def area(self):
        """
        >>> round(Circle(5).area, 4)
        31.4159
        >>> Circle(1).area
        0.0
        """
        return 2 * self.radius * math.pi
        
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, radius):
        self._radius = radius

    @radius.deleter
    def radius(self):
        del self._radius
        
    @property
    def diameter(self):
        """
        >>> Circle(5).diameter
        10
        >>> Circle(0).diameter
        0
        """
        return self.radius * 2
    
    @diameter.setter
    def diameter(self, diameter):
        self._radius = diameter / 2 
        
import doctest
doctest.testmod()
