from random import randint    # import randint function for random integer generation,

# Define parameters
min_val = 0            # define minimum possible value
max_val = 1000         # define maximum possible value
num_of_elements = 100  # define the length of the list

# create list of random numbers. Here we use list comprehension
lst = [randint(min_val, max_val) for i in range(num_of_elements)]

print('Output of the generated list:')  # print sub-header string
print(f'\t{lst}')                       # print the original list of random numbers

# below we sort the list using Bubble sort algorithm
sorted_flag = False                     # we initialize a boolean variable to indicate if list is sorted
end_reached_counter = 0                 # we initialize a variable to count the number of times we reached the end
while not sorted_flag:                  # outer while loop, we loop till the list gets sorted
    j = 0                               # we initialize integer variable, index for next element
    for i in range(len(lst)-1):         # we use inner for loop that loops through the list items
        j = i + 1                       # we update index for next element
        if lst[i] > lst[j]:             # we compare current and next elements
            lst[i], lst[j] = lst[j], lst[i]   # if current element is larger than the next element we swap the
            break                       # once the elements got swapped we break the loop
    if j == len(lst) - 1:               # if the index of the next element equals the index of the last element
        end_reached_counter += 1        # we increment the counter
    if end_reached_counter == 2:        # we nmake sure to reach the end twice thus we ensure all elements are sorted
        sorted_flag = True              # We set the boolean flag "sorted_flag" to True. That will terminate
                                        # the outer While loop.

print('Output of the sorted list:')     # print sub-header string
print(f'\t{lst}')                       # print the sorted list of random numbers, we use f string for indentation

odd_nums = [el for el in lst if el % 2 == 1]       # we use list comprehension to pick odd elements to a new list
even_nums = [el for el in lst if el % 2 == 0]      # we use list comprehension to pick even elements to a new list

sum_odd = 0                         # we define an interim variable to store the sum of odd numbers
for item in odd_nums:               # use for loop to iterate through a list and sum all elements of a list
    sum_odd += item                 # and sum all elements of a list

sum_even = 0                        # we define an interim variable to store the sum of even numbers
for item in even_nums:              # use for loop to iterate through a list and sum all elements of a list
    sum_even += item                # and sum all elements of a list

avg_odd_A = sum_odd / len(odd_nums)                    # we calculate average of odd elements of the list
avg_even_A = sum_even / len(even_nums)                 # we calculate average of even elements of the list

print('Output of calculation results:')                # print text header for the results output
print(f'\tAverage of odd numbers = {avg_odd_A}')       # print average of odd list elements
print(f'\tAverage of even numbers = {avg_even_A}')     # print average of even list elements