class City:
    """
    A base class of a City. A city has a name and geographical coordinates.

    Attributes:
        name(str): the name of a city
        latitude(float): latitude part of the coordinates expressed as float
        longitude(float): longitude part of the coordinates expressed as float

    Methods:
        ask_name(): ask the name of a city
        ask_coordinates(): asks coordinates (latitude and longitude) of a given city
        get_coordinates(): tries to look-up coordinates for a given city in the cities.db, if not found calls
            ask_coordinates() method, when coordinates are obtained - insert the record containing city information
            to the cities.db
    """

    def __init__(self):
        self.name = ''
        self.latitude = 0.0
        self.longitude = 0.0

    def ask_name(self) -> str:
        self.name = input("\nPlease, enter the name of the city: ")
        return self.name

    def _validate_coordinate_input(self, coordinate: str) -> float:
        """
        Ask for a coordinate. Check if it is a valid float number. Check if it has a valid coordinate (latitude or
        longitude) value.
        :param coordinate: text string with one of the two acceptable values 'latitude' or 'longitude'. It is used
        to guide the interaction with the user and validate entered value as a specified coordinate.
        :return: (float) returns a coordinate entered by the user
        """
        num = float('Nan')
        if coordinate.lower() == 'latitude':
            limit = 90
        elif coordinate.lower() == 'longitude':
            limit = 180
        else:
            return num

        while True:
            try:
                num = float(input(f"\tPlease enter the {coordinate} for {self.name}. Use the decimal format xx.xxxxx: "))
            except ValueError:
                print(f"{coordinate.capitalize()} needs to be a decimal number between {-limit} and {limit}")
                continue

            if -limit <= num <= limit:
                print(f"You have set the {coordinate} to {num}")
                return num
            else:
                print(f"Please enter a decimal number between {-limit} and {limit}")

    def ask_coordinates(self) -> (float, float):
        # self.latitude = float(input(f"\tPlease enter the latitude for {self.name}. Use the format xx.xxxxx: "))
        # self.longitude = float(input(f"\tPlease enter the longitude for {self.name}. Use the format xx.xxxxx: "))
        self.latitude = self._validate_coordinate_input('latitude')
        self.longitude = self._validate_coordinate_input('longitude')
        return self.latitude, self.longitude

    def get_coordinates(self, dbcon) -> (float, float):
        result = dbcon.find_city('cities', self.name)
        if result:
            print(f'"{self.name}" is already present in the database.\n')
            self.latitude, self.longitude = float(result[0][2]), float(result[0][3])
            print(f"{self.name}")
            print(f"\tLatitude: {self.latitude}")
            print(f"\tLongitude: {self.longitude}")
        else:
            print(f"{self.name} is not yet in the database. Let's add it...\n")
            self.latitude, self.longitude = self.ask_coordinates()
            data = {
                'city': self.name,
                'latitude': self.latitude,
                'longitude': self.longitude
            }
            dbcon.insert('cities', data)
        return self.latitude, self.longitude
