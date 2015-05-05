#!/usr/bin/env python2
import collections
import multiprocessing
import functools
import string
from glob import glob
from pprint import pprint


def map_func(ignored, minlen, filename):
    """Read a file and return a sequence of (word, 1) values.
    ignored: words which should be ignored
    minlen: minimal length for word
    filename: file for reading
    """
    tr = string.maketrans(string.punctuation, ' ' * len(string.punctuation))
    output = []
    with open(filename, 'rt') as f:
        for line in f:
            line = line.translate(tr)
            for word in line.split():
                word = word.lower()
                if (word.isalpha() and
                            word not in ignored and
                            len(word) >= minlen):
                    output.append((word, 1))
    return output

def map_func_factory(ignored, minlen):
    """Provides map_func function with specified default arguments.
    ignored: default ignored argument for map_func function
    minlen: default minlen argument for map_func function
    """
    func = functools.partial(map_func, ignored, minlen)
    return func

def reduce_func(item):
    """Convert the partitioned data for a word to a
    tuple containing the word and the number of occurances.
    item: partitioned data for a word
    """
    word, occurances = item
    return (word, sum(occurances))

def partition(mapped_values):
    """Organize the mapped values by their key.
    Returns an unsorted sequence of tuples with a key and a sequence of values.
    mapped_values: sequence of mapped values (map_func output)
    """
    partitioned_data = collections.defaultdict(list)
    for key, value in mapped_values:
        partitioned_data[key].append(value)
    return partitioned_data.items()

def words_counter(path, ext=["*"], ignored=[], minlen=2,
                  num_workers=None, chunksize=1):
    """Counts the number of occurrences of each word in the specified files.
    path: directory with files for reading
    ext: extensions of files which should be read
    ignored: words which should be ignored
    minlen: minimal length for word
    num_workers: the number of workers to create in the pool
    chunksize: the portion of the input data to hand to each worker
    """
    listmerge = lambda ll: reduce(lambda a,b: a + b, ll, [])
    pool = multiprocessing.Pool(num_workers)
    input_files = listmerge(map(lambda e: glob('%s*.%s' % (path, e)), ext))
    new_map_func = map_func_factory(ignored, minlen)
    map_responses = pool.map(new_map_func, input_files, chunksize=chunksize)
    partitioned_data = partition(listmerge(map_responses))
    reduced_values = pool.map(reduce_func, partitioned_data)
    pool.close()
    return reduced_values

# USING
if __name__ == '__main__':
    exclude = ["if", "else", "on", "at"]
    words = words_counter('/home/dzmitry/pycourse-dmoroz/pyttleship/',
                          ext=["py"],
                          ignored=exclude,
                          minlen=2)
    pprint(words)
