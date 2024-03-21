import datetime                        # import datetime, we will use it to perform operations with dates
from abc import ABC                    # use abc module to create abstract base classes in Python
from abc import abstractmethod         # lets us define abstract methods that need to be implemented by
                                       # the subclass which inherits that class and this way lets us
                                       # force behavior by forcing the subclass to implement those methods

from contextlib import contextmanager  # we define a custom contextmanager to take care of writing info to newsfeed file
import re                              # import regular expression module. Used to check if the expiry date matches
                                       # the specified format

from utility_funcs import normalize_case, opened_w_error

class PostBase(ABC):
    """
    A base class of a newsfeed Post. We use AMC to make it an abstract class.
    """

    @contextmanager
    def __init__(self):
        """
        Constructor of the base class PostBase. It creates date attribute with
        the current date. It runs a method to get required data, and then another
        method to publish the data into the newsfeed.
        """
        pass

    @property
    def date(self):
        return datetime.datetime.now()

    @abstractmethod
    def ask_required_data(self) -> None:
        """
        Abstract method to get required user input.
        Returns:
             None
        """
        pass

    @abstractmethod
    def publish(self) -> None:
        """
        Abstract method to publish post to the newsfeed.
        Returns:
             None
        """
        pass

    def post_to_newsfeed(self, header: str = '.....header.....', body: str = '??? body ???'):
        """
        Method for publishing post to the newsfeed file. We take
        Returns:
             None
        """
        filename = "newsfeed.txt"
        with opened_w_error(filename, "a") as (f, err):
            if err:
                print(f'IOError: {err}')
            else:
                f.write(f'{header}\n')
                f.write(f'{body}\n')
                f.write(f'\n')


class News(PostBase):
    """
    News class, inherits from PostBase. It is a news article.
    Attributes:
        text(str): the body of the news article
        city(str): the city featured in the news article

    Methods:
        ask_required_data(): get required user input
        publish(): publish post to the newsfeed
    """

    def __init__(self):
        self.post_type = 'News'

    def ask_required_data(self):
        self.text = input("Please enter news text: ")
        self.city = input("Please enter the name of the city: ")

    def publish(self):
        self.post_to_newsfeed(
            header=f'.....[{self.post_type}].....',
            body=f'{normalize_case(self.text)}\n{normalize_case(self.city)}, {self.date:%Y-%m-%d}'
        )


class PrivateAd(PostBase):
    """
    PrivateAd class, inherits from PostBase. It is a private ad post.
    Attributes:
        text(str): the body of the ad
        expiration_date(datetime.date): the expiration date

    Methods:
        ask_required_data(): get required user input
        validate_expiration_date(): checks if the expiration date is valid date and is a future date (not yet expired)
        publish(): publish post to the newsfeed
    """

    def __init__(self):
        self.post_type = 'Private Ad'
        self.text = ''
        self.expiration_date = datetime.date.today()

    def validate_expiration_date(self, date_entry: str):
        # Compile regex pattern. The pattern looks for the date matching specified format.
        pattern = re.compile(r'^(20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$')
        matches = pattern.findall(date_entry)  # we store all the matches in the list "matches"
        if len(matches) == 0:  # if the list is empty, this means no correctly formatted date was found
            raise ValueError("It is not a date or the date format is wrong.\n")
        year, month, day = map(int, date_entry.split('-'))
        self.expiration_date = datetime.date(year, month, day)
        if self.expiration_date <= datetime.date.today():
            raise ValueError("This Private Ad has already expired. The expiration date should be some future date.")

    def ask_required_data(self):
        self.text = input("Please enter the ad text: ")
        while True:  # we start an "infinite loop",
            # which is terminated with correctly formatted and valid expiration date

            # try...except block to handle exceptions when parsing date
            # we can correctly handle:
            #   - badly formatted dates
            #   - invalid dates, for example 2025-02-29 as February in 2025 will have only 28 days
            #   - expiration dates that >= today's date
            date_entry = input("Please enter the expiration date in YYYY-MM-DD format: ")
            try:
                self.validate_expiration_date(date_entry)
            except ValueError as err:
                print(f'Warning: {err}\n')
            else:
                break

    def publish(self):
        delta = self.expiration_date - datetime.date.today()
        self.post_to_newsfeed(
            header=f'.....[{self.post_type}].....',
            body=f'{normalize_case(self.text)}\nActual until: {self.expiration_date:%Y-%m-%d}, {delta.days} days left'
        )


class WordOfTheDay(PostBase):
    """
    WordOdTheDay class, inherits from PostBase. It is a post featuring "Word of the Day".
    It contains some interesting word and definition of it's meaning. Every day a new word
    is posted, each word is assigned a number, which is "day of year".
    Attributes:
        word(str): some interesting word
        meaning(str): definition of it's meaning

    Methods:
        ask_required_data(): get required user input
        publish(): publish post to the newsfeed
    """

    def __init__(self):
        self.post_type = 'Word of The Day'
        self.word = ''
        self.meaning = ''

    def ask_required_data(self):
        self.word = input("Enter word of the day: ")
        self.meaning = input(f'Enter the definition for "{self.word}": ')

    def publish(self, **kwargs):
        day_of_year = self.date.timetuple().tm_yday  # we calculate day of year
        self.post_to_newsfeed(
            header=f'.....[{self.post_type}].....',
            body=f'Word #{day_of_year}\nWord: {normalize_case(self.word)}\nMeaning: {normalize_case(self.meaning)}'
        )
