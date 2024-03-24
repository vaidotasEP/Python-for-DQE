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


def list_words(txt: str):
    """
        Return a list words. Each word is the last words of each sentence in the given text.

        Args:
            txt (str): text string
        Returns:
            list of strings, each string is a word, last word of each sentence
    """
    # Compile regex pattern. The pattern looks for the last word in a sentence.
    # It is:
    # -  preceded by 1 or few whitespace symbols
    # -  may consist of one or more letters of any case, numbers from 0 to 9, "-" and "_" symbols
    # -  trailed by one or more sentence ending symbols "." "?" "!"
    pattern = re.compile(r'[\[\(\s]*([a-zA-Z0-9-_]+)[ \],.?!]*')
    return re.findall(pattern, txt)                 # find all words matching the pattern
                                                    # store results in the list


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
