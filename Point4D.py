import numbers
from itertools import accumulate
from cmath import sqrt
import iround

class Point4D:
    def __init__(self, x: numbers.Number, 
                       y: numbers.Number, 
                       z: numbers.Number, 
                       w: numbers.Number, /) -> None:
        for dimension in (x, y, z, w):
            if not isinstance(dimension, numbers.Number):
                raise TypeError('Dimension arguments of a Point4D '
                                'instance must be a number.')
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    @property
    def distance_from_origin(self) -> float | complex:
        distance = tuple(accumulate((self.x, self.y, self.z, self.w), 
                               lambda x, y: sqrt(x**2 + y**2)))
        distance = distance[-1]
        if distance.imag == 0:
            return distance.real
        return distance

    def distance_to(self, other: 'Point4D') -> float | complex:
        if not isinstance(other, Point4D):
            raise TypeError('Argument of distance_to method '
                            'must be an instance of Point4D.')

        distance = tuple(accumulate((self.x - other.x,
                                     self.y - other.y,
                                     self.z - other.z,
                                     self.w - other.w), 
                                    lambda x, y: sqrt(x**2 + y**2)))
        distance = distance[-1]
        
        if distance.imag == 0:
            return distance.real
        return distance

    @staticmethod
    def distance_between(p1: 'Point4D', p2: 'Point4D') -> float | complex:
        for p in (p1, p2):
            if not isinstance(p, Point4D):
                raise TypeError('Arguments of distance_between method '
                                'must be instances of Point4D.')

        distance = tuple(accumulate((p1.x - p2.x,
                                     p1.y - p2.y,
                                     p1.z - p2.z,
                                     p1.w - p2.w), 
                                    lambda x, y: sqrt(x**2 + y**2)))
        distance = distance[-1]

        if distance.imag == 0:
            return distance.real
        return distance


def main():
    p1 = Point4D(2,2,2,2)
    print(p1.distance_from_origin)

    p2 = Point4D(2+1j, 4+2j, 0, 0)
    print(iround.iround(p2.distance_from_origin, 2))

    print(iround.iround(p1.distance_to(p2)))
    print(iround.iround(Point4D.distance_between(p1, p2)))


if __name__ == '__main__':
    main()