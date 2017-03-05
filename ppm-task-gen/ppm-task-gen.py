"""
A script for generating the tasks for project-playbills-mark.
"""
import os
import csv
import json
import argparse
import itertools


def makedir(path):
    """Create a directory."""
    try:
        os.mkdir(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def write_csv(path, data):
    """Write the data to a csv file."""
    with open(path, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)


def read_csv(path, questions):
    """Return the question data generated for the csv and json files."""
    with open(path, 'rb') as f:
        reader = csv.reader(f)
        l = list(reader)
        headers = l[0] + [questions[0][k] for k in sorted(questions[0])]
        for r in l[1:]:
            row = [r + [q[k] for k in sorted(q)] for q in questions]
            data[r[4]] = data.get(r[4], []) + row
        return data, headers


if __name__ == '__main__':
    description = '''Generate tasks for project-playbills-mark.
    
    By default it loads ppm-ark-data.csv, adds a row for each question defined 
    in ppm-questions.json, then generates a new csv file containing all data 
    assoicated with each Aleph System number.
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--arks', default='ppm-ark-data.csv',
                        help="The CSV input file.")
    parser.add_argument('--questions', default='ppm-questions.json',
                        help="The CSV input file.")
    args = parser.parse_args()
    questions = json.load(open(args.questions, 'rb'))
    data, headers = read_csv(args.arks, questions)
    makedir(os.path.join(os.path.dirname(__file__), 'tasks'))
    for k in data.keys():
        write_csv('tasks/{0}.csv'.format(k), data[k], headers)
        