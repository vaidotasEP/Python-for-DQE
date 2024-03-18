from news_posts import News, PrivateAd, WordOfTheDay
from news_from_file import NewsFromFile


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
    try:
        while i < len(content):
            text_str = content[i].strip().lower()

            if text_str != '':
                if text_str == 'news':
                    newsPost.text = content[i+1].strip()
                    newsPost.city = content[i+2].strip()
                    newsPost.publish()
                elif text_str == 'private ad':
                    privateAd.text = content[i+1].strip()
                    date_entry = content[i + 2].strip()
                    try:
                        privateAd.validate_expiration_date(date_entry)   # validate expiration date
                    except ValueError as err:
                        print(f'(Warning:) {err}')
                        print(f'Aborting news import from text file')
                    privateAd.publish()
                elif text_str == 'word of the day':
                    wordOTD.word = content[i+1].strip()
                    wordOTD.meaning = content[i+2].strip()
                    wordOTD.publish()
            else:
                i += 1
                continue

            if (i == 0) and (newsFromFile.input_format == "1"):
                break
            else:
                i += 3
    except ValueError as err:
        print(f'(Warning:) {err}')
    else:
        if i >= len(content):
            print(f'All news published. Deleting the file `{newsFromFile.path_to_input_file}`\n')
            newsFromFile.delete_obsolete_input_file(newsFromFile.path_to_input_file)
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
            publish(newsFromFile.content)
    elif user_input.upper() == "Q":
        break
    else:
        print("That's not a valid choice!")
