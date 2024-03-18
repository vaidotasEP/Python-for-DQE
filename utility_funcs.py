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
    return pattern.sub(make_upper, tmp_string)   # substitute matches with the result of the function


@contextmanager
def opened_w_error(filename: str, mode: str = "a"):
    """
    Context manager to implement try...except block to handle exceptions when writing to file
    Args:
        filename: the filename where data will be written
        mode: file access mode. The default setting is a - append
    Returns:
        a tuple consisting of file object and error
    """
    try:
        f = open(filename, mode, encoding='utf-8')
    except IOError as err:
        yield None, err
    else:
        try:
            yield f, None
        finally:
            f.close()
