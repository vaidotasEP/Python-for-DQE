import csv
# import unicodecsv as csv
import string
from collections import defaultdict
from utility_funcs import list_words, read_posts_from_file, opened_w_error


class BaseCounter:
    """
    Class to implement word and letter counting. Counts are recorded in respective csv files:
    word counts are recorded in 'word-count.csv' file
    letter counts are recorded in 'letter-counts' file

    Attributes:
        word_list(lst): the list of published words
        word_counts(dict): dictionary containing words used in the newsfeed and their counts
        letter_counts(dict): dictionary containing letters used in newsfeed and their counts
        letter_results(defaultdict[int, int, float]): dictionary containing letters used in
            newsfeed and their counts (count_all, count_uppercase, percentage)
        tot_letter_count(int): total count of letters published in the newsfeed

    Methods:
        add_words(txt): takes text, splits it into separate words and updates word_list,
            word and letter counts
        count_words(word_list): counts words and updates word_counts dict
        count_letters(word_list): counts letters and updates letter_counts, letter_results dicts
        csv_write(rows_of_data: [dict], headers: [str], filename: str):
            writes rows_of_data dictionary and headers to .csv files
        csv_write_words(): writes word_counts dictionary to `word-count.csv` file
        csv_write_letters(): writes letter_results dictionary to `word-letters.csv` file
        csv_update_counts(): performs data write to .csv files by calling both: `self.csv_write_words()`
            and `self.csv_write_letters()` methods
    """

    def __init__(self):
        self.word_list = []
        self.word_counts = {}
        # self.letter_counts = {}
        self.letter_results = defaultdict(lambda: [0, 0, 0.0])
        self.tot_letter_count = 0


    def add_words(self, txt):
        lines = txt.split('\n')
        words = []
        for line in lines:
            for word in list_words(line):
                if word:
                    words.extend([word])
        self.word_list.extend(words)
        self.count_words(words)
        self.count_letters(words)


    def count_words(self, word_list):
        for word in word_list:
            word = word.lower()
            if word not in self.word_counts:
                self.word_counts[word] = 1
            else:
                self.word_counts[word] += 1


    def count_letters(self, word_list):
        letter_counts = {}
        for word in word_list:
            for letter in word:
                if letter not in letter_counts:
                    letter_counts[letter] = 1
                else:
                    letter_counts[letter] += 1

        for c in letter_counts.keys():
            if c == c.lower() and c not in self.letter_results:
                self.letter_results[c][0] = letter_counts[c]
            else:
                self.letter_results[c][0] += letter_counts[c]

        for c in letter_counts.keys():
            if c == c.upper() and c.lower() not in self.letter_results:
                self.letter_results[c.lower()][0] = letter_counts[c]
                self.letter_results[c.lower()][1] = letter_counts[c]
            else:
                self.letter_results[c.lower()][0] += letter_counts[c]  #self.letter_results[c.lower()][0] + letter_counts[c]
                self.letter_results[c.lower()][1] += letter_counts[c]

        for k, v in self.letter_results.items():
            self.tot_letter_count += v[0]

        for k, v in self.letter_results.items():
            self.letter_results[k][2] = round(v[0] * 100 / self.tot_letter_count, 2)


    def csv_write(self, rows_of_data: [dict], headers: [str], filename: str, need_header: bool):
        with opened_w_error(filename, 'w', newline='') as (f, err):
            if err:
                print(f'IOError: {err}')
            else:
                csv_writer = csv.DictWriter(
                    f,
                    fieldnames=headers
                )
                if need_header:
                    csv_writer.writeheader()
                for row in rows_of_data:
                    csv_writer.writerow(row)


    def csv_write_words(self):
        headers = ['word', 'count']
        rows_of_data = []
        for key, value in self.word_counts.items():
            rows_of_data.append({
                headers[0]: key,
                headers[1]: value
            })
        self.csv_write(
            rows_of_data=rows_of_data,
            headers=headers,
            filename='word-count.csv',
            need_header=False
        )


    def csv_write_letters(self):
        headers = ['letter', 'count_all', 'count_uppercase', 'percentage']
        rows_of_data = []
        for key, value_arr in self.letter_results.items():
            rows_of_data.append({
                headers[0]: key,
                headers[1]: value_arr[0],
                headers[2]: value_arr[1],
                headers[3]: value_arr[2],
            })
        self.csv_write(
            rows_of_data=rows_of_data,
            headers=headers,
            filename='letter-counts.csv',
            need_header=True
        )


    def csv_update_counts(self):
        self.csv_write_words()
        self.csv_write_letters()


if __name__ == "__main__":
    counter = BaseCounter()
    content = read_posts_from_file('newsfeed.txt')
    counter.add_words(content)
