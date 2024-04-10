from math import radians, sin, cos, acos
from city import City


class Route:
    """
    A base class of a Route. A Route connects two cities: city_a and city_b.

    Attributes:
        city_a(City): first city to start the route
        city_b(City): second city to end the route

    Methods:
        calculate_distance(): calculates and returns the distance in kilometers between two given cities
    """

    def __init__(self, city_a: City = None, city_b: City = None):
        self.city_a = city_a
        self.city_b = city_b

    def calculate_distance(self) -> float:
        """
         Convert the coordinates from degrees to radians and use the sine and cosine functions along with
         the Earth’s mean radius (6371.01 km) to calculate the distance. The acos() function is used to
         compute the arc-cosine of the central angle between the two locations.
         Source: https://www.askpython.com/python/examples/find-distance-between-two-geo-locations
        :return:
            distance between 2 cities in kilometers
        """
        mlat = radians(self.city_a.latitude)
        mlon = radians(self.city_a.longitude)
        plat = radians(self.city_b.latitude)
        plon = radians(self.city_b.longitude)
        return 6371.01 * acos(sin(mlat) * sin(plat) + cos(mlat) * cos(plat) * cos(mlon - plon))
