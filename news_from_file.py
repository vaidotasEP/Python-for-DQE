import os
import re
from news_posts import PostBase
from utility_funcs import opened_w_error
from datetime import datetime


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
        print(filename)
        with opened_w_error(filename, "r") as (f, err):
            if err:
                print(f'IOError: {err}\n')
                return err
            else:
                txt = f.read()
                pattern = re.compile(fr'post:\s?((?:\r\n.+)+)\r\n*', re.UNICODE)
                self.content = re.findall(pattern, txt)
                return "Ok"

    def write_erroneous_post_to_file(self, content):
        filename = "invalid_posts.txt"
        with opened_w_error(filename, "a") as (f, err):
            if err:
                print(f'IOError: {err}')
                return err
            else:
                f.write(f'-----[{datetime.now()}]-----\n')
                for line in content:
                    f.write('post:\n\t')
                    f.write(line.strip() + '\n\n')

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
            print(f"\nYou entered '{self.input_format}', therefore we will attempt to read and publish all records.")

        self.path_to_input_file = './News/news1.txt'
        print(f"\nCurrently default input file is : `{self.path_to_input_file}`")
        user_input = input(f"\nPress ENTER to accept, or provide direct path to the news source file (ex: {self.path_to_input_file}: ")
        if user_input != '':
            self.path_to_input_file = user_input.strip()

    def publish(self, *args):
        newsPost, privateAd, wordOTD = args
        i = 0
        txt = ''
        _news = fr'type:\s?(.*)\n\s+body:\s?(.*(?:\r?\n(?!\r?\n).*)*)\s+city:\s?(.*)'
        _ad = fr'type:\s?(.*)\n\s+body:\s?(.*(?:\r?\n(?!\r?\n).*)*)\s+expiration:\s?(.*)'
        _word = fr'type:\s?(.*)\n\s+word:\s?(.*(?:\r?\n(?!\r?\n).*)*)\s+meaning:\s?(.*(?:\r?\n(?!\r?\n).*)*)'
        news_pattern = re.compile(_news)
        ad_pattern = re.compile(_ad)
        word_pattern = re.compile(_word)
        try:
            while i < len(self.content):
                post = self.content[i].strip().lower()
                news = re.findall(news_pattern, post)
                ads = re.findall(ad_pattern, post)
                words = re.findall(word_pattern, post)
                if news:
                    newsPost.text = news[0][1].strip()
                    newsPost.city = news[0][2].strip()
                    txt = newsPost.publish()
                    self.content.pop(i)
                elif ads:
                    privateAd.text = ads[0][1].strip()
                    date_entry = ads[0][2].strip()
                    try:
                        privateAd.validate_expiration_date(date_entry)  # validate expiration date
                    except ValueError as err:
                        print(f'\nWarning: {err}\n')
                        i += 1
                        continue
                    else:
                        txt = privateAd.publish()
                        self.content.pop(i)
                elif words:
                    wordOTD.word = words[0][1].strip()
                    wordOTD.meaning = words[0][2].strip()
                    txt = wordOTD.publish()
                    self.content.pop(i)
                else:
                    i += 1
                    continue
                if self.input_format == "1":
                    break
        except (ValueError, IndexError) as err:
            print(f'Error: {err}\n')
        else:
            if (len(self.content) > 0) and (self.input_format != "1"):
                print(
                    f'Warning: some records were not posted to the newsfeed. They were coppied to `invalid_posts.txt` file) \n')
                self.write_erroneous_post_to_file(self.content)
            if i >= len(self.content):
                print(f'All valid posts were published. Deleting the file `{self.path_to_input_file}`\n\n')
                self.delete_obsolete_input_file(self.path_to_input_file)
        return txt
