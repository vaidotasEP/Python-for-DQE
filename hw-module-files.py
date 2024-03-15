import datetime                        # import datetime, we will use it to perform operations with dates
from abc import ABC                    # use abc module to create abstract base classes in Python
from abc import abstractmethod         # lets us define abstract methods that need to be implemented by
                                       # the subclass which inherits that class and this way lets us
                                       # force behavior by forcing the subclass to implement those methods
from contextlib import contextmanager  # we define a custom contextmanager to take care of writing info to newsfeed file
import re                              # import regular expression module. Used to check if the expiry date matches
                                       # the specified format
import os

# originally I had named my homework files using hyphens "-". I found this as a way to import a module
# which in the name contains hyphens "-". Alternatively, I would rename the file changing hyphens to
# underscore symbols and use:
#       from hw_functions_string import  normalize_case

import importlib
string_functions = importlib.import_module("hw-functions-string")

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
    print(f'4 - Create post(s) from a text file')
    print()
    print(f'Q - Quit')
    print('-------------------------------------------')
    print()


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

    @contextmanager
    def opened_w_error(self, filename: str, mode: str = "a"):
        """
        Context manager to implement try...except block to handle exceptions when writing to file
        Args:
            filename: the filename where data will be written
            mode: file access mode. The default setting is a - append
        Returns:
            a tuple consisting of file object and error
        """
        try:
            f = open(filename, mode)
        except IOError as err:
            yield None, err
        else:
            try:
                yield f, None
            finally:
                f.close()

    def post_to_newsfeed(self, header: str = '.....header.....', body: str = '??? body ???'):
        """
        Method for publishing post to the newsfeed file. We take
        Returns:
             None
        """
        filename = "newsfeed.txt"
        with self.opened_w_error(filename, "a") as (f, err):
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
            body=f'{string_functions.normalize_case(self.text)}\n{string_functions.normalize_case(self.city)}, {self.date:%Y-%m-%d}'
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
            raise ValueError("It is not a date or the date format is wrong.")
        year, month, day = map(int, date_entry.split('-'))
        self.expiration_date = datetime.date(year, month, day)
        if self.expiration_date <= datetime.date.today():
            raise ValueError("This Private Ad has already expired. The expiration date should be some future date.")

    def ask_required_data(self):
        self.text = input("Please enter the ad text: ")
        while True:     # we start an "infinite loop",
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
                print(f'(Warning:) {err}')
            else:
                break

    def publish(self):
        delta = self.expiration_date - datetime.date.today()
        self.post_to_newsfeed(
            header=f'.....[{self.post_type}].....',
            body=f'{string_functions.normalize_case(self.text)}\nActual until: {self.expiration_date:%Y-%m-%d}, {delta.days} days left'
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
        day_of_year = self.date.timetuple().tm_yday   # we calculate day of year
        self.post_to_newsfeed(
            header=f'.....[{self.post_type}].....',
            body=f'Word #{day_of_year}\nWord: {string_functions.normalize_case(self.word)}\nMeaning: {string_functions.normalize_case(self.meaning)}'
        )

class NewsFromFile(PostBase):
    """
    NewsFromFile class, inherits from PostBase. It is a post or number of posts read from a text file.

    Attributes:
        input_format(str): "1" means only one post will be read from the provided txt file,
                           any other value will cause an attempt to read all available posts
        path_to_input_file(str): path to a txt file containing news posts
        content(List[str]): full content of the txt file, split into list elements based on '\n'

    Methods:
        ask_required_data(): get required user input
        _delete_obsolete_input_file(filename: str): deletes obsolete input file
        read_posts_from_file():
        publish(): publish post to the newsfeed
    """
    def __init__(self):
        self.post_type = 'News from TXT File'
        self.input_format = ''
        self.path_to_input_file = 'news.txt'
        self.content = []


    def read_posts_from_file(self):
        filename = self.path_to_input_file  # "news.txt"
        with self.opened_w_error(filename, "r") as (f, err):
            if err:
                print(f'IOError: {err}')
                return err
            else:
                txt = f.read()
                self.content = txt.strip().split('\n')
                return "Ok"

    def _delete_obsolete_input_file(self, filename: str):
        # Try to delete the file.
        try:
            os.remove(filename)
        except OSError as e:
            # If it fails, inform the user.
            print("Error: %s - %s." % (e.filename, e.strerror))

    def ask_required_data(self):
        print(f"Load post(s) from 'news.txt' file.")
        self.input_format = input("Define input format. Press '1' for one record or any other key for many records: ")
        if self.input_format == "1":
            print(f"\nYou pressed '1', therefore we will attempt to read and publish a single record.")
        else:
            print(f"\nYou entered '{self.input_format}', therefore we will attempt to read and publish many records.")

        self.path_to_input_file = 'news.txt'
        print(f"\nCurrently default input file is : `{self.path_to_input_file}`")
        user_input = input(f"\nPress ENTER to accept, or provide direct path to the news source file (ex: ./News/news1.txt): ")
        if user_input != '':
            self.path_to_input_file = user_input.strip()


    def publish(self, **kwargs):
        i = 0
        try:
            while i < len(self.content):
                text_str = self.content[i].strip().lower()

                if text_str != '':
                    if text_str == 'news':
                        newsPost.text = self.content[i+1].strip()
                        newsPost.city = self.content[i+2].strip()
                        newsPost.publish()
                    elif text_str == 'private ad':
                        privateAd.text = self.content[i+1].strip()
                        date_entry = self.content[i + 2].strip()
                        try:
                            privateAd.validate_expiration_date(date_entry)   # validate expiration date
                        except ValueError as err:
                            print(f'(Warning:) {err}')
                            print(f'Aborting news import from text file')
                        privateAd.publish()
                    elif text_str == 'word of the day':
                        wordOTD.word = self.content[i+1].strip()
                        wordOTD.meaning = self.content[i+2].strip()
                        wordOTD.publish()
                else:
                    i += 1
                    continue

                if (i == 0) and (self.input_format == "1"):
                    break
                else:
                    i += 3
        except ValueError as err:
            print(f'(Warning:) {err}')
        else:
            if i >= len(self.content):
                print(f'All news published. Deleting the file `{self.path_to_input_file}`\n')
                self._delete_obsolete_input_file(self.path_to_input_file)
            else:
                print(f'File will not be deleted, as there is some more text that has not been imported.\n')


# initializing all classes before the loop to save computational resources by initializing them only once
newsPost = News()
privateAd = PrivateAd()
wordOTD = WordOfTheDay()
newsFromFile = NewsFromFile()

while True:      # we start an "infinite loop", which can be terminated by pressing "Q"
    show_menu()
    user_input = input("\nPlease enter your choice: ")
    if user_input == "1":
        newsPost.ask_required_data()
        newsPost.publish()
    elif user_input == "2":
        privateAd.ask_required_data()
        privateAd.publish()
    elif user_input == "3":
        wordOTD.ask_required_data()
        wordOTD.publish()
    elif user_input == "4":
        newsFromFile.ask_required_data()
        if newsFromFile.read_posts_from_file() == "Ok":
            newsFromFile.publish()
    elif user_input.upper() == "Q":
        break
    else:
        print("That's not a valid choice!")




    ### The best practice when using the __init__ method is to describe the initial state of the object.
    ### I strongly do not recommend calling other methods from this method,
    ### because they change the given initial state of the object and then the main meaning of the __init__ method is lost.
    #   Done


    ### use @property decorator for the date method.
    # self.date = datetime.datetime.now()    # get current data
    #   Done


    ### First, the @property decorator allows a method to be accessed as an attribute: self.date.
    ### Secondly, each time a new date is generated, this is relevant if the class is initialized only once.
    # @property
    # def date(self):
    #     return datetime.datetime.now()
    #   Done


    # self.ask_required_data()  # call method to get required user input
    # # recommended removing this attribute self.publish()
    # self.publish()  # publish post to the newsfeed
    #   Done


    ### I recomended adding additional methods here, for write changes to file
    ### Because all your entries essentially have the same structure and are repeated in other classes:
    ### Heading
    ### Main entry
    ### You can pass a header to this method, which, for example, is automatically generated in the form:
    ### .....[Heading].....
    ### And the main text for the entry.
    ###
    #   Done


    ### And strongly recommend using try...except block to handle exceptions when writing to file
    #   Done


    ### And strongly recommend using try...except block to handle exceptions when parsing date
    ### Now the program generates an error when entering an incorrect date.
    # year, month, day = map(int, date_entry.split('-'))
    #   Done


    ### Maybe it makes sense to check expiration_date if it is 0 or in the past relative to the current date?
    # self.expiration_date = datetime.date(year, month, day)
    #   Done


    ### I suggest moving show_menu() to inside the loop for create user friendly dialogue in terminal.
    #   Done


    ### I recommend initializing all classes before the loop
    ### because if you initialize a class every time, you will waste
    ### some time and computational resources on this process.
    ### In a real project, if you want to save the state of a class or the class is too large,
    ### you need to initialize the class once.
    # """
    # Example:
    #
    # news = News()
    # ...
    #
    # if user_input == "1":
    #     news.publish()
    #
    # """

    #   Done


    ### The average user is too lazy to enter an additional command every time)
    ### so I suggest showing the menu automatically before each new input.
    #   Done

