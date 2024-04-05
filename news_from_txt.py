import os
import re
from news_posts import PostBase
from news_from_file import NewsFromFile
from utility_funcs import opened_w_error
from datetime import datetime


class NewsFromTXT(NewsFromFile):
    """
    NewsFromTXT class, inherits from NewsFromFile. It is a post or number of posts read from a text file.

    Attributes:
        input_format(str): "1" means only one post will be read from the provided txt file,
                           any other value will cause an attempt to read all available posts
        path_to_input_file(str): path to a txt file containing news posts
        content(List[str]): full content of the txt file, split into list elements based on '\n'

    Methods:
        read_posts_from_file():
        write_erroneous_post_to_file():
        ask_required_data(): get required user input

        publish(): publish post to the newsfeed
    """
    def __init__(self):
        self.input_format = ''
        self.path_to_input_file = './News/news1.txt'
        self.content = []

    def read_posts_from_file(self):
        filename = self.path_to_input_file
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

    def ask_required_data(self, filename: str = ''):
        self.input_format, self.path_to_input_file = super().ask_required_data(self.path_to_input_file)

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
