from random import randint, seed    # import randint function for random integer generation,
                                    # and seed function to ensure reproducibility working with random numbers
from functools import reduce        # import reduce. We use it for reducing a list into a
                                    # single number - sum of all elements

# Define parameters
min_val = 0            # define minimum possible value
max_val = 1000         # define maximum possible value
num_of_elements = 100  # define the length of the list

seed(12345)            # we set the seed to make results reproducible

# create list of random numbers. Here we use list comprehension
lst = [randint(min_val, max_val) for i in range(num_of_elements)]

# print(lst)           # print the original list of random numbers
# print(len(lst))      # print the length of the list

# below we sort the list using Bubble sort algorithm
sorted = False                          # we initialize a boolean variable to indicate if list is sorted
while (not sorted):                     # outer while loop, we loop till the list gets sorted
    j = 0                               # we initialize integer variable, index for next element
    for i in range(len(lst) - 1):       # we use inner for loop that loops through the list items
        j = i + 1                       # we update index for next element
        if lst[i] > lst[j]:             # we compare current and next elements
            lst[i], lst[j] = lst[j], lst[i]   # if current element is larger than the next element we swap the
            break                       # once elements got swapped we break the loop
    if j == len(lst) - 1:               # if the index of the next element equals the index of the last element
        sorted = True                   # means we reached the end of the list and all the preceding
                                        # elements are sorted. That means the entire list is sorted.
                                        # We set the boolean flag "sorted" to True. That will terminate
                                        # the outer While loop.

# print(lst)                            # print the sorted list of random numbers

def sum(a, b):                          # we define a function that gets two elements
    return a + b                        # and returns the sum of those elements
                                        # we will use this function together with reduce

# Below I developed 2 solutions:
#   (A) using list comprehensions, and
#   (B) using filter function and lambda function
# Both solutions produce the same result

# Solution (A):
odd_A = [el for el in lst if el % 2 == 1]       # we use list comprehension to pick odd elements to a new list
even_A = [el for el in lst if el % 2 == 0]      # we use list comprehension to pick even elements to a new list

# use reduce to sum all elements of a list and divide by the number of elements in the list to calculate avg
avg_odd_A = reduce(sum, odd_A) / len(odd_A)     # we calculate average of odd elements of the list
avg_even_A = reduce(sum, even_A) / len(even_A)  # we calculate average of even elements of the list

print('Solution A:')                            # print text header for the results output
print(avg_odd_A)                                # print average of odd list elements
print(avg_even_A)                               # print average of odd list elements
print()                                         # print empty line to have visual separation in the output

# Solution (B):
odd_B = list(filter(lambda el: el % 2 == 1, lst))   # we use filter to pick odd elements to a new list
even_B = list(filter(lambda el: el % 2 == 0, lst))  # we use filter to pick even elements to a new list

# use reduce to sum all elements of a list and divide by the number of elements in the list to calculate avg
avg_odd_B = reduce(sum, odd_B) / len(odd_B)         # we calculate average of odd elements of the list
avg_even_B = reduce(sum, even_B) / len(even_B)      # we calculate average of even elements of the list

print('Solution B:')                            # print text header for the results output
print(avg_odd_B)                                # print average of odd list elements
print(avg_even_B)                               # print average of odd list elements




