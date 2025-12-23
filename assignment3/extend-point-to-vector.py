import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
       
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def distance(self, other):
        
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx**2 + dy**2)

class Vector(Point):
    

    def __str__(self):
       
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        # Overloading the + operator for Vector addition
        # Returns a NEW Vector instance
        if isinstance(other, Vector) or isinstance(other, Point):
            new_x = self.x + other.x
            new_y = self.y + other.y
            return Vector(new_x, new_y)
        else:
            raise TypeError("Operand must be a Point or Vector")


if __name__ == "__main__":
    print("--- Testing Point Class ---")
    p1 = Point(1, 1)
    p2 = Point(4, 5)
    p3 = Point(1, 1)

    print(f"p1: {p1}")
    print(f"p2: {p2}")
    print(f"p1 == p3: {p1 == p3}")  # Should be True
    print(f"p1 == p2: {p1 == p2}")  # Should be False
    
    dist = p1.distance(p2)
    print(f"Distance between p1 and p2: {dist}") # Should be 5.0

    print("\n--- Testing Vector Class ---")
    v1 = Vector(2, 3)
    v2 = Vector(5, 7)

    print(f"v1: {v1}")
    print(f"v2: {v2}")

   
    v3 = v1 + v2
    print(f"v1 + v2 = {v3}") 
    print(f"Type of result: {type(v3).__name__}") # Should be 'Vector'