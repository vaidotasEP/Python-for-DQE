import json
from news_posts import PostBase, News, PrivateAd, WordOfTheDay
from news_from_file import NewsFromFile
from utility_funcs import opened_w_error
from datetime import datetime


class NewsFromJSON(NewsFromFile):
    """
    NewsFromJSON class, inherits from NewsFromFile. It is a post or number of posts read from a JSON file.

    Attributes:
        input_format(str): "1" means only one post will be read from the provided json file,
                           any other value will cause an attempt to read all available posts
        path_to_input_file(str): path to a json file containing news posts
        content(List[str]): full content of the json file, split into list elements based on '\n'

    Methods:
        ask_required_data(): get required user input
        delete_obsolete_input_file(filename: str): deletes obsolete input file
        read_posts_from_json():
        publish(): publish post to the newsfeed
    """
    def __init__(self):
        self.input_format = ''
        self.path_to_input_file = './News/news1.json'
        self.content = []

    def read_posts_from_file(self):
        filename = self.path_to_input_file
        with opened_w_error(filename, "r") as (f, err):
            if err:
                print(f'IOError: {err}\n')
                return err
            else:
                data = json.load(f)
                self.content = data['posts']
                return "Ok"

    def write_erroneous_post_to_file(self, content):
        filename = "invalid_posts.json"
        with opened_w_error(filename, "a") as (f, err):
            if err:
                print(f'IOError: {err}')
                return err
            else:
                elements = []
                posts = {}
                for item in content:
                    elements.append(item)
                posts['timestamp'] = str(datetime.now())
                posts['posts'] = elements
                json.dump(posts, f)

    def ask_required_data(self, filename: str = ''):
        self.input_format, self.path_to_input_file = super().ask_required_data(self.path_to_input_file)

    # def publish(self, dbcon: DBConnection, *args):
    #     newsPost, privateAd, wordOTD = args
    #     i = 0
    #     txt = ''
    #     try:
    #         while i < len(self.content):
    #             element = self.content[i]
    #             if element['type'].strip().lower() == 'news':
    #                 newsPost.text = element['body'].strip()
    #                 newsPost.city = element['city'].strip()
    #                 txt = newsPost.publish(dbcon)
    #                 self.content.pop(i)
    #             elif element['type'].strip().lower() == 'private ad':
    #                 privateAd.text = element['body'].strip()
    #                 date_entry = element['expiration'].strip()
    #                 try:
    #                     privateAd.validate_expiration_date(date_entry)  # validate expiration date
    #                 except ValueError as err:
    #                     print(f'\nWarning: {err}\n')
    #                     i += 1
    #                     continue
    #                 else:
    #                     txt = privateAd.publish(dbcon)
    #                     self.content.pop(i)
    #             elif element['type'].strip().lower() == 'word of the day':
    #                 wordOTD.word = element['word'].strip()
    #                 wordOTD.meaning = element['meaning'].strip()
    #                 txt = wordOTD.publish(dbcon)
    #                 self.content.pop(i)
    #             else:
    #                 i += 1
    #                 continue
    #             if self.input_format == "1":
    #                 break
    #     except (ValueError, IndexError) as err:
    #         print(f'Error: {err}\n')
    #     else:
    #         if (len(self.content) > 0) and (self.input_format != "1"):
    #             print(
    #                 f'Warning: some records were not posted to the newsfeed. They were coppied to `invalid_posts.json` file) \n')
    #             self.write_erroneous_post_to_file(self.content)
    #         if i >= len(self.content):
    #             print(f'All valid posts were published. Deleting the file `{self.path_to_input_file}`\n\n')
    #             self.delete_obsolete_input_file(self.path_to_input_file)
    #     return txt
