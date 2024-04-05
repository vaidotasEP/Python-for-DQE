from news_posts import News, PrivateAd, WordOfTheDay
from news_from_txt import NewsFromTXT
from news_from_json import NewsFromJSON
from news_from_xml import NewsFromXML
from utility_funcs import read_posts_from_file
from csv_counters import BaseCounter


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
    print(f'4 - Import post(s) from .txt file')
    print(f'5 - Import post(s) from .json file')
    print(f'6 - Import post(s) from .xml file')
    print()
    print(f'Q - Quit')
    print('-------------------------------------------')
    print()


# initializing all classes before the loop to save computational resources by initializing them only once
newsPost = News()
privateAd = PrivateAd()
wordOTD = WordOfTheDay()
newsFromTXT = NewsFromTXT()
newsFromJSON = NewsFromJSON()
newsFromXML = NewsFromXML()

counter = BaseCounter()
content = read_posts_from_file('newsfeed.txt')
counter.add_words(content)
counter.csv_update_counts()

while True:      # we start an "infinite loop", which can be terminated by pressing "Q"
    txt = ''
    show_menu()
    user_input = input("\nPlease enter your choice: ")
    if user_input == "1":
        newsPost.ask_required_data()
        txt = newsPost.publish()
    elif user_input == "2":
        privateAd.ask_required_data()
        txt = privateAd.publish()
    elif user_input == "3":
        wordOTD.ask_required_data()
        txt = wordOTD.publish()
    elif user_input == "4":
        newsFromTXT.ask_required_data()
        if newsFromTXT.read_posts_from_file() == "Ok":
            txt = newsFromTXT.publish(newsPost, privateAd, wordOTD)
    elif user_input == "5":
        newsFromJSON.ask_required_data()
        if newsFromJSON.read_posts_from_file() == "Ok":
            txt = newsFromJSON.publish(newsPost, privateAd, wordOTD)
    elif user_input == "6":
        newsFromXML.ask_required_data()
        if newsFromXML.read_posts_from_file() == "Ok":
            txt = newsFromXML.publish(newsPost, privateAd, wordOTD)
    elif user_input.upper() == "Q":
        break
    else:
        print("That's not a valid choice!")

    if txt:
        counter.add_words(txt)
        counter.csv_update_counts()
