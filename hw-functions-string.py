import re                          # import regex to perform regular expression operations

# copy of the given text stored as a multi-line string
input_str = """homEwork:
  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""


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


def replace(txt: str, from_substr: str, to_substr: str):
    """
        Within the given text string, replace one substring with another one. Substring has to be bounded by whitespaces.
        It can also be at the end of the sentence ending with . ? !

        Args:
            txt (str): text string where replacement needs to be performed;
            from_substr (str): a substring that we want to be changed
            to_substr (str): a substring that we want to see in place of an old substring
        Returns:
            text string with substring replacements
    """
    # Compile regex pattern. The pattern looks for "iz" preceded with 1 or more whitespace
    # symbols, and followed by a whitespace or end of sentence symbols '.' or '?' or '!'.
    pattern = re.compile(fr'(\s+)({from_substr})([\s?!.]+)')
    tmp_string = pattern.sub(fr'\1{to_substr}\3', txt)  # substitute matches with the 1st group,
    return tmp_string                                     # "is" and 3rd group from the found match


def list_last_words(txt: str):
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
    pattern = re.compile(r'\s+([a-zA-Z0-9-_]+)[.?!]+')
    return pattern.findall(txt)                     # find all words matching the pattern
                                                    # store results in the list

def insert_str_after(txt: str, string_to_insert: str, target: str):
    """
        In a given text string, locate a target substring and following that target insert a given string.

        Args:
            txt (str): text string with the target where we want an insertion to take place
            string_to_insert (str):  a string that we want to be inserted following the target substring
            target (str): a substring within the text string
        Returns:
            (str) text string with insertion if the target was found, or original text string otherwise
    """
    # Compile regex pattern. The pattern looks for the place where we need to insert
    # newly created sentence. The marker for that is the word "paragraph" followed by "."
    pattern = re.compile(fr'(\b{target})')
    return pattern.sub(r'\1 ' + string_to_insert, txt)  # insert the sentence.


def count_whitespaces(txt: str):
    """
        Return a number of whitespaces found in the given text string.

        Args:
            txt (str):  text string where we want to count whitespaces
        Returns:
            (int) a number of whitespaces found within the given text string
    """
    # Compile regex pattern. The pattern looks for whitespace symbols.
    pattern = re.compile(r'(\s)')
    matches = pattern.findall(txt)  # we store all the matches in the list "matches"
    return len(matches)


def lst_to_sentence(lst: list):
    """
        Make a properly capitalized sentence out of a list of words.

        Args:
            lst: list containing strings
        Returns:
            (str) text string containing a formed sentence
    """
    sentence = (' '.join(lst) + '.\n')  # construct a sentence
    return normalize_case(sentence)     # and capitalize it


my_string = normalize_case(input_str)
print(my_string)                        # print properly capitalized text
print()                                 # print an empty line for separation

my_string = replace(my_string, from_substr='iz', to_substr='is')
print(my_string)                                    # print properly capitalized text & "iz" corrected text
print()                                             # print an empty line for separation

sentence_to_insert = lst_to_sentence(list_last_words(my_string))
print(sentence_to_insert)                                           # print constructed sentence

my_string = insert_str_after(
    my_string,
    string_to_insert=sentence_to_insert,
    target='paragraph.'
)
print(my_string)     # print properly capitalized, "iz" corrected text with the added sentence

print()              # print an empty line for separation
# print the number of whitespaces found
print(f'Number of whitespaces found in the original string: {count_whitespaces(input_str)}')

