import datetime                   # import datetime, we will use it to perform operations with dates
from abc import ABC               # use abc module to create abstract base classes in Python
from abc import abstractmethod    # lets us define abstract methods that need to be implemented by
                                  # the subclass which inherits that class and this way lets us
                                  # force behavior by forcing the subclass to implement those methods

def show_menu() -> None:
    """
    Displays a comprehensive user menu

    Returns:
        None
    """
    print('-------------------------------------------')
    print(f'1 - Create a News article')
    print(f'2 - Create a Private Ad')
    print(f'3 - Create "Word of the Day"')
    print()
    print(f'M - Show this menu')
    print(f'Q - Quit')
    print('-------------------------------------------')
    print()


class PostBase(ABC):
    """
    A base class of a newsfeed Post. We use AMC to make it an abstract class.
    """
    def __init__(self):
        """
        Constructor of the base class PostBase. It creates date attribute with
        the current date. It runs a method to get required data, and then another
        method to publish the data into the newsfeed.
        """
        self.date = datetime.datetime.now()    # get current data
        self.ask_required_data()               # call method to get required user input
        self.publish()                         # publish post to the newsfeed

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
        PostBase.__init__(self)        # we call constructor of a base class

    def ask_required_data(self):
        self.text = input("Please enter news text: ")
        self.city = input("Please enter the name of the city: ")

    def publish(self):
        with open('newsfeed.txt', 'a') as f:   # use context manager to append post to newsfeed.txt
            f.write(f'.....[{self.post_type}].....\n')
            f.write(f'{self.text}\n')
            f.write(f'{self.city}, {self.date:%Y-%m-%d}\n')
            f.write(f'\n')


class PrivateAd(PostBase):
    """
    PrivateAd class, inherits from PostBase. It is a private ad post.
    Attributes:
        text(str): the body of the ad
        expiration_date(datetime.date): the expiration date

    Methods:
        ask_required_data(): get required user input
        publish(): publish post to the newsfeed
    """
    def __init__(self):
        self.post_type = 'Private Ad'
        PostBase.__init__(self)        # we call constructor of a base class

    def ask_required_data(self):
        self.text = input("Please enter the ad text: ")
        date_entry = input("Please enter the expiration date in YYYY-MM-DD format: ")
        year, month, day = map(int, date_entry.split('-'))
        self.expiration_date = datetime.date(year, month, day)

    def publish(self):
        with open('newsfeed.txt', 'a') as f:   # use context manager to append post to newsfeed.txt
            f.write(f'.....[{self.post_type}]......\n')
            f.write(f'{self.text}\n')
            delta = self.expiration_date - datetime.date.today()
            f.write(f'Actual until: {self.expiration_date:%Y-%m-%d}, {delta.days} days left\n')
            f.write(f'\n')


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
        PostBase.__init__(self)        # we call constructor of a base class

    def ask_required_data(self):
        self.word = input("Enter word of the day: ")
        self.meaning = input(f'Enter the definition for "{self.word}": ')

    def publish(self, **kwargs):
        day_of_year = self.date.timetuple().tm_yday   # we calculate day of year
        with open('newsfeed.txt', 'a') as f:          # use context manager to append post to newsfeed.txt
            f.write(f'.....[{self.post_type}].....\n')
            f.write(f'Word #{day_of_year}\n')
            f.write(f'Word: {self.word}\n')
            f.write(f'Meaning: {self.meaning}\n')
            f.write(f'\n')


show_menu()      # call function to display user menu
while True:      # we start an "infinite loop", which can be terminated by pressing "Q"
    user_input = input("\nPlease enter your choice: ")
    if user_input == "1":
        obj = News()
    elif user_input == "2":
        obj = PrivateAd()
    elif user_input == "3":
        obj = WordOfTheDay()
    elif user_input.upper() == "M":
        show_menu()
    elif user_input.upper() == "Q":
        break
    else:
        print("That's not a valid choice!")