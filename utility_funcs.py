import re                              # import regex to perform regular expression operations
from contextlib import contextmanager  # we define a custom contextmanager to take care of writing info to newsfeed file


def make_upper(match):
    """
        Return match object with the first letter turned into upper case

        Args:
            match: regex match object

        Returns:
            regex match object with the first letter turned into upper case
    """
    return match.group(1).upper()


def normalize_case(txt: str):
    """
        Return given text with normalized case, i.e. the first letter of the first word in a sentence should be of
        upper-case. All other letters in the sentence should be lower-case.
        Be careful using this function on sentences with proper nouns!

        Args:
            txt (str):   a text string that needs to have the case of letters to be normalized
        Returns:
            (str) text string with normalized case
    """
    tmp_string = txt.lower()         # convert text of input_str to lower case
    # Compile regex pattern. The pattern looks for the first letter of each sentence.
    # It can be:
    #   - the first letter at the start of a text  '^' ;
    #   - a letter following '.' or '?' or '!' with some trailing whitespaces
    pattern = re.compile(u'((^|\.\s+|\?\s+|!\s+)(\w))')
    return pattern.sub(make_upper, tmp_string)   # substitute matches with the result of the


def split(delimiters: [str], string: str, maxsplit: int=0):
    regex_pattern = '|'.join(map(re.escape, delimiters))
    return re.split(regex_pattern, string, maxsplit)


def list_words(txt: str):
    """
        Return a list words. Each word is the last words of each sentence in the given text.

        Args:
            txt (str): text string
        Returns:
            list of strings, each string is a word, last word of each sentence
    """
    new_words = []
    resulting_wordlist = []
    pattern = re.compile(r"([\w'-_]+)")
    words = re.findall(pattern, txt)

    delimiters = [';', ',', '[', ']', '(', ')', '=', '_', '.']

    for word in words:
        split_words = split(delimiters, word)
        for str1 in split_words:
            if str1:
                new_words.append(str1)

    pattern = re.compile(r"[ ;:,.?!=\[\]\(\)]*")
    for word in new_words:
        if word[0].isalpha():
            new_word = re.sub(pattern, '', word)
            resulting_wordlist.append(new_word)

    return resulting_wordlist


@contextmanager
def opened_w_error(filename: str, mode: str = "a", newline: str = ''):
    """
        Context manager to implement try...except block to handle exceptions when writing to file
        Args:
            filename: the filename where data will be written
            mode: file access mode. The default setting is a - append
            newline: string specifying new line symbol
        Returns:
            a tuple consisting of file object and error
    """
    try:
        f = open(filename, mode, newline=newline, encoding='utf-8')
    except IOError as err:
        yield None, err
    else:
        try:
            yield f, None
        finally:
            f.close()


def read_posts_from_file(filename: str = 'newsfeed.txt'):
    """
        Reads text from a text file
        Args:
            filename: the filename from which text data will be read
        Returns:
            str: text string containing data extracted from the file
    """
    with opened_w_error(filename, "r") as (f, err):
        if err:
            print(f'IOError: {err}')
            return ''
        else:
            return f.read()
