from random import randint      # import randint function for random integer generation

ascii_letters = 'abcdefghijklmnopqrstuvwxyz'    # string listing all possible letters for dictionary keys

# Define parameters
min_num_of_dicts = 2            # define minimum possible value for the number of generated dictionaries
max_num_of_dicts = 10           # define maximum possible value for the number of generated dictionaries
min_num_of_keys = 2             # define minimum possible value for the number of elements in generated dictionaries
max_num_of_keys = 10            # define maximum possible value for the number of elements in generated dictionaries
min_value = 0                   # define minimum possible value for entries within generated dictionaries
max_value = 100                 # define minimum possible value for entries within generated dictionaries

num_of_dicts = randint(min_num_of_dicts, max_num_of_dicts)   # we generate random number of dicts from the given range
lst = []                        # define an empty list to store our generated data

for i in range(num_of_dicts):   # we use for loop to generate a list containing num_of_dicts dictionaries
    dic = {}                    # define an empty dictionary, we will be adding random entries here
    num_of_keys = randint(min_num_of_keys, max_num_of_keys)     # generate random number to define the size of the dict
    while len(dic.keys()) < num_of_keys:                        # loop till we add sufficient number of random entries
        key = ascii_letters[randint(0, len(ascii_letters)-1)]  # use random numer generator to generate random letter
        value = randint(min_value, max_value)                   # generate random value for the entry
        dic.setdefault(key, value)                              # add key value pair to the dictionary
    lst.append(dic)             # add newly generated dictionary to the list

print('Output of the generated list:')  # print sub-header string
print(f'\t{lst}')                       # print the generated list containing randomly generated dictionaries

set_of_keys = set()                 # define an empty set, we will use it to generate a set of all unique keys
for dic in lst:                     # we iterate through the list of randomly generated dictionaries
    set_of_keys = set_of_keys.union(set(dic.keys()))  # add keys of each dictionary to the set

lst_of_keys = list(set_of_keys)     # convert the set to the list. It contains all unique keys present in the lst

new_dic = {}                        # define an empty dictionary, it will store our final result
count_dic = {}                      # define an empty dictionary of lists, to store array index+1 where key is present
index_max_val_dic = {}              # define an empty dictionary, to store index+1 of dict where the key with largest
                                    # value was spotted
for key in lst_of_keys:             # iterate through all unique keys
    for i, dic in enumerate(lst):   # iterate through dictionaries in the list, with the index value and the dictionary
        i += 1                      # increment index by 1, as we will use key suffixes numbering starting from 1
        if dic.get(key, -1) > -1:   # check if given key exists in the given dictionary
            if count_dic.get(key, -1) == -1:  # we check if we have this key in our counter dictionary
                count_dic[key] = 1  # if not we add the key with the value 1, i.e. we met this key one time
            else:
                count_dic[key] += 1  # if we already saw this key, we increment the corresponding counter
        if dic.get(key, -1) > new_dic.get(key, -1):  # if the value is larger for a given key, we
            new_dic[key] = dic.get(key, -1)          # add/update the key value pair
            index_max_val_dic[key] = i               # we add the index + 1 of the dict where larger value was spotted

# the loop below is for reassigning values to appropriately renamed keys, obsolete key value pairs get deleted
for key, val in count_dic.items():   # loop through the dict containing counts the key was observed in different dicts
    if val > 1:                      # if it is more than one time
        new_dic[str(f'{key}_{index_max_val_dic[key]}')] = new_dic.pop(key)  # create renamed key and reassign value
                                                                            # obsolated key value pair gets removed
print('Output of the derived one common dict:')  # print sub-header string
print(f'\t{new_dic}')                            # print the generated list containing randomly generated dictionaries
