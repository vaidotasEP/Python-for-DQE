import os

from news_posts import PostBase
from utility_funcs import opened_w_error

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
        with opened_w_error(filename, "r") as (f, err):
            if err:
                print(f'IOError: {err}')
                return err
            else:
                txt = f.read()
                self.content = txt.strip().split('\n')
                return "Ok"

    def delete_obsolete_input_file(self, filename: str):
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
        pass
