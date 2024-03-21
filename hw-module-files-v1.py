from news_posts import News, PrivateAd, WordOfTheDay
from news_from_file import NewsFromFile
import re


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


def publish(content):
    i = 0
    _news = fr'type:\s?(.*)\n\s+body:\s?(.*(?:\r?\n(?!\r?\n).*)*)\s+city:\s?(.*)'
    _ad = fr'type:\s?(.*)\n\s+body:\s?(.*(?:\r?\n(?!\r?\n).*)*)\s+expiration:\s?(.*)'
    _word = fr'type:\s?(.*)\n\s+word:\s?(.*(?:\r?\n(?!\r?\n).*)*)\s+meaning:\s?(.*(?:\r?\n(?!\r?\n).*)*)'
    news_pattern = re.compile(_news)
    ad_pattern = re.compile(_ad)
    word_pattern = re.compile(_word)
    try:
        while i < len(content):
            post = content[i].strip().lower()
            news = re.findall(news_pattern, post)
            ads = re.findall(ad_pattern, post)
            words = re.findall(word_pattern, post)
            if news:
                newsPost.text = news[0][1].strip()
                newsPost.city = news[0][2].strip()
                newsPost.publish()
                content.pop(i)
            elif ads:
                privateAd.text = ads[0][1].strip()
                date_entry = ads[0][2].strip()
                try:
                    privateAd.validate_expiration_date(date_entry)   # validate expiration date
                except ValueError as err:
                    print(f'\nWarning: {err}\n')
                    i += 1
                    continue
                else:
                    privateAd.publish()
                    content.pop(i)
            elif words:
                wordOTD.word = words[0][1].strip()
                wordOTD.meaning = words[0][2].strip()
                wordOTD.publish()
                content.pop(i)
            else:
                i += 1
                continue
            if newsFromFile.input_format == "1":
                break
    except (ValueError, IndexError) as err:
        print(f'Error: {err}\n')
    else:
        if (len(content) > 0) and (newsFromFile.input_format != "1"):
            print(f'Warning: some records were not posted to the newsfeed. They were coppied to `invalid_posts.txt` file) \n')
            newsFromFile.write_erroneous_post_to_file(content)
        if i >= len(content):
            print(f'All valid posts were published. Deleting the file `{newsFromFile.path_to_input_file}`\n\n')


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
            publish(newsFromFile.content)
    elif user_input.upper() == "Q":
        break
    else:
        print("That's not a valid choice!")
