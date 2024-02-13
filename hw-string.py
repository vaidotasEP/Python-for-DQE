# copy of the given text stored as a multi-line string
input_str = """homEwork:
  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

sep1 = '. '                                            # sentence separator
sep2 = u'\xa0 '                                        # alternative sentence separator
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'         # we list all possible upper characters

upper_chars = set()    # we define empty set, here we will store indexes of characters that need to be made uppercase

# split text based on sentence separator, capitalize obtained sentences and join them back into the text
text1 = sep1.join([s.capitalize() for s in input_str.split(sep1)])
# split text based on alternative sentence separator, capitalize obtained sentences and join them back into the text
text2 = sep2.join([s.capitalize() for s in input_str.split(sep2)])

for i, char in enumerate(input_str):                                     # iterate through the original text
    if (text1[i] in ascii_uppercase) or (text2[i] in ascii_uppercase):   # check if character is in upper case in text1 or text2
        upper_chars.add(i)                                               # add index of the character to the set

lst = list(input_str.lower())              # split text into separate characters, make them lower case and store as list
for i in upper_chars:                      # iterate through a set of indices of characters that need to be upper case
    lst[i] = lst[i].upper()                # we update the character in a list with its upper case version
output_str = ''.join(lst)                  # we reconstruct the text string by joining elements of the list

print(output_str)                          # print properly capitalized text

selected_words = []                                    # define empty list to store last word of each sentence
# iterate through sentences of a text, first we split on corrected sentence separators
for sentence in output_str.replace('.', '. ').split(sep1):
    selected_words.append((sentence.split(' ')[-1]))   # we split a sentence into separate words
                                                       # add the last word of a sentence to a list of selected words

# Construct a sentence by doing the following:
# join the words into a string, remove unnecessary whitespace, add . and new line symbol, capitalize sentence
tmp_sentence = (' '.join(selected_words).strip() + '.\n').capitalize()
print(tmp_sentence)                                    # print the constructed sentence

# add sentence to the end of the paragraph that ends with "paragraph."
output_str = output_str.replace('paragraph.', f'paragraph. {tmp_sentence}')
print(output_str)                                      # print properly capitalized text with added sentence

# fix "iz" with correct "is" using replace() method
output_str = output_str.replace(' iz ', ' is ')
print(output_str)                                      # print final edited text (capitalized, added sentence, fixed)

# calculate whitespaces
white_space = 0                                        # define integer counter for whitespace characters
for character in input_str:                            # we iterate through characters of the original input text
    if character in [' ', '\t', u'\xa0', '\n', '\r']:  # we check if a character is a whitespace character
        white_space += 1                               # we increment the counter

print(f'Number of whitespaces found in the original string: {white_space}')   # print the number of whitespaces found
