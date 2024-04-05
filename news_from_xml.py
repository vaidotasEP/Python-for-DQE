import xml.etree.ElementTree as ET
from news_posts import PostBase, News, PrivateAd, WordOfTheDay
from news_from_file import NewsFromFile
from utility_funcs import opened_w_error
from datetime import datetime


class NewsFromXML(NewsFromFile):
    """
    NewsFromXML class, inherits from NewsFromFile. It is a post or number of posts read from an XML file.

    Attributes:
        input_format(str): "1" means only one post will be read from the provided xml file,
                           any other value will cause an attempt to read all available posts
        path_to_input_file(str): path to a xml file containing news posts
        content(List[str]): full content of the xml file, split into list elements based on '\n'

    Methods:
        read_posts_from_file():
        write_erroneous_post_to_file():
        ask_required_data(): get required user input
    """
    def __init__(self):
        self.input_format = ''
        self.path_to_input_file = './News/news1.xml'
        self.content = []

    def read_posts_from_file(self):
        filename = self.path_to_input_file
        with opened_w_error(filename, "r") as (f, err):
            if err:
                print(f'IOError: {err}\n')
                return err
            else:
                data = ET.parse(f)
                root = data.getroot()
                for post in root.findall('post'):
                    if 'type' in post.attrib:
                        tmp_post = {
                            'type': post.attrib['type'],
                            post[0].tag: post[0].text,
                            post[1].tag: post[1].text
                        }
                        self.content.append(tmp_post)
                return "Ok"

    def write_erroneous_post_to_file(self, content):
        filename = "invalid_posts.xml"
        with opened_w_error(filename, "a") as (f, err):
            if err:
                print(f'IOError: {err}')
                return err
            else:
                element_posts = ET.Element("posts")
                element_posts.set('timestamp', str(datetime.now()))

                for post in content:
                    element_post = ET.SubElement(element_posts, "post")
                    for key, val in post.items():
                        if key == 'type':
                            element_post.set(key, val)
                        else:
                            sub_element = ET.SubElement(element_post, key)
                            sub_element.text = val

                tree = ET.ElementTree(element_posts)
                tree.write(filename, encoding='utf-8', xml_declaration=True)

    def ask_required_data(self, filename: str = ''):
        self.input_format, self.path_to_input_file = super().ask_required_data(self.path_to_input_file)
