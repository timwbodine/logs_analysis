"""news_reporter.py generates several tables from the newsdata.sql data, organizing data by most popular authors, most popular articles, and high error days."""
#!/usr/bin/python
import psycopg2
from tabulate import tabulate


def connect(database):
    """connect to the database.  alternatively, print an error message."""
    try:
        db = psycopg2.connect("dbname={}".format(database))
        cursor = db.cursor()
        return db, cursor
    except:
        print("There was an error connecting to the database.")

def get_most_popular_articles():
    """get a list of the top 3 most popular articles by all time views"""
    db, c = connect("news")
    c.execute("select articles.title, count(*) from articles, log where subst"
              "ring(log.path from '/article/(.*)')=articles.slug group by"
              " articles.title order by count desc limit 3;")
    return c.fetchall()


def get_most_popular_authors():
    """get a list of the top 4 most popular authors by all time views of articles written by them"""
    db, c = connect("news")
    c.execute("select authors.name, views_by_author_id.num from views_by_auth"
              "or_id, authors where views_by_author_id.author = authors.id"
              " limit 4;")
    return c.fetchall()


def get_high_error_days():
    """find and list any days on which the percentage of connections resulting in error exceeded 1%"""
    db, c = connect("news")
    c.execute("select views_per_day.day, float4((errors_per_day.errors * 100."
              "0)/views_per_day.views) as perc from errors_per_day, views_per"
              "_day where views_per_day.day = errors_per_day.day and float4(("
              "errors_per_day.errors * 100.0)/views_per_day.views) >= 1.0;")
    return c.fetchall()

"""use tabulate library to format tables written to output.txt"""
with open('output.txt', 'w') as output:
    lines = get_most_popular_articles()
    output.write('Most Popular Articles\n\n')
    output.write(tabulate(lines, headers=['Articles', 'Views']))
    output.write('\n\nMost Popular Authors\n\n')
    lines = get_most_popular_authors()
    output.write(tabulate(lines, headers=['Authors', 'Views']))
    output.write('\n\nHigh Error Days\n\n')
    lines = get_high_error_days()
    output.write(tabulate(lines, headers=['Day', '% Errors']))
