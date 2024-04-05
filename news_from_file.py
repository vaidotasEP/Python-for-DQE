import os
from news_posts import PostBase
from abc import abstractmethod

class NewsFromFile(PostBase):
    """
    NewsFromFile class, inherits from PostBase. It is a post or number of posts read from a file.
    It serves as a parent class for NewsFromTXT, NewsFromJSON, NewsFromXML.

    Attributes:
        input_format(str): "1" means only one post will be read from the provided file,
                           any other value will cause an attempt to read all available posts
        path_to_input_file(str): path to a txt, json or xml file containing news posts
        content(List[str]): full content of the txt file, split into list elements based on '\n'

    Methods:
        ask_required_data(): get required user input
        _delete_obsolete_input_file(filename: str): deletes obsolete input file
        read_posts_from_file():
        publish(): publish post to the newsfeed
    """
    def __init__(self):
        self.post_type = 'News from File'
        self.input_format = ''
        self.path_to_input_file = 'news.*'
        self.content = []

    @abstractmethod
    def read_posts_from_file(self):
        pass

    @abstractmethod
    def write_erroneous_post_to_file(self, content):
        pass

    def delete_obsolete_input_file(self, filename: str):
        # Try to delete the file.
        try:
            os.remove(filename)
        except OSError as e:
            # If it fails, inform the user.
            print("Error: %s - %s." % (e.filename, e.strerror))

    def ask_required_data(self, filename: str = '') -> (str, str):
        self.path_to_input_file = filename

        print(f"Import post(s) from file.")
        self.input_format = input("Define input format. Press '1' for one record or any other key for many records: ")
        if self.input_format == "1":
            print(f"\nYou pressed '1', therefore we will attempt to read and publish a single record.")
        else:
            print(f"\nYou entered '{self.input_format}', therefore we will attempt to read and publish all records.")
        print(f"\nCurrently default input file is : `{self.path_to_input_file}`")
        user_input = input(f"\nPress ENTER to accept, or provide direct path to the news source file (ex: {self.path_to_input_file}: ")
        if user_input != '':
            self.path_to_input_file = user_input.strip()

        return self.input_format, self.path_to_input_file


    def publish(self, *args):
        newsPost, privateAd, wordOTD = args
        i = 0
        txt = ''
        try:
            while i < len(self.content):
                element = self.content[i]
                if element['type'].strip().lower() == 'news':
                    newsPost.text = element['body'].strip()
                    newsPost.city = element['city'].strip()
                    txt = newsPost.publish()
                    self.content.pop(i)
                elif element['type'].strip().lower() == 'private ad':
                    privateAd.text = element['body'].strip()
                    date_entry = element['expiration'].strip()
                    try:
                        privateAd.validate_expiration_date(date_entry)  # validate expiration date
                    except ValueError as err:
                        print(f'\nWarning: {err}\n')
                        i += 1
                        continue
                    else:
                        txt = privateAd.publish()
                        self.content.pop(i)
                elif element['type'].strip().lower() == 'word of the day':
                    wordOTD.word = element['word'].strip()
                    wordOTD.meaning = element['meaning'].strip()
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
                    f'Warning: some records were not posted to the newsfeed. They were coppied to `invalid_posts.json` file) \n')
                self.write_erroneous_post_to_file(self.content)
            if i >= len(self.content):
                print(f'All valid posts were published. Deleting the file `{self.path_to_input_file}`\n\n')
                self.delete_obsolete_input_file(self.path_to_input_file)
        return txt
