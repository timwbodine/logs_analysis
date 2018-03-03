#!/usr/bin/python
"""news_reporter.py generates several tables from the newsdata.sql data,
organizing data by most popular authors, most popular articles, and high
error days."""
import psycopg2
from tabulate import tabulate


def connect(database):
    """connect to the database.  alternatively, print an error message."""
    try:
        db = psycopg2.connect("dbname={}".format(database))
        cursor = db.cursor()
        return db, cursor
    except Exception:
        print("There was an error connecting to the database.")


def get_most_popular_articles():
    """get a list of the top 3 most popular articles by all time views"""
    db, c = connect("news")
    c.execute("select articles.title, count(*) from articles, log where subst"
              "ring(log.path from '/article/(.*)')=articles.slug group by"
              " articles.title order by count desc limit 3;")
    return c.fetchall()


def get_most_popular_authors():
    """get a list of the most popular authors by all time views of articles
    written by them"""
    db, c = connect("news")
    c.execute("select authors.name, views_by_author_id.num from views_by_auth"
              "or_id, authors where views_by_author_id.author = authors.id;")
    return c.fetchall()


def get_high_error_days():
    """find and list any days on which the percentage of connections resulting
    in error exceeded 1%"""
    db, c = connect("news")
    c.execute("select views_per_day.day, float4((errors_per_day.errors * 100."
              "0)/(views_per_day.views + errors_per_day.errors)) as perc from"
              " errors_per_day, views_per_day where views_per_day.day"
              " = errors_per_day.day and float4((errors_per_day.errors * "
              "100.0)/(views_per_day.views + errors_per_day.errors)) >= 1.0;")
    return c.fetchall()


def run_program(output_file):
    with open(output_file, 'w') as output:
        def print_and_write(line):
            """use tabulate library to format tables written to output.txt. Also
            print them to terminal."""
            output.write(line)
            print line
        lines = get_most_popular_articles()
        print_and_write('Most Popular Articles\n\n')
        print_and_write(tabulate(lines, headers=['Articles', 'Views']))
        print_and_write('\n\nMost Popular Authors\n\n')
        lines = get_most_popular_authors()
        print_and_write(tabulate(lines, headers=['Authors', 'Views']))
        print_and_write('\n\nHigh Error Days\n\n')
        lines = get_high_error_days()
        print_and_write(tabulate(lines, headers=['Day', '% Errors']))
run_program('output.txt')
