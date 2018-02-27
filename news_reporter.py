import psycopg2
from tabulate import tabulate


def get_most_popular_articles():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("select articles.title, count(*) from articles, log where subst"
              "ring(log.path from '/article/(.*)')=articles.slug group by"
              " articles.title order by count desc;")
    return c.fetchall()
    db.close()


def get_most_popular_authors():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("select authors.name, views_by_author_id.num from views_by_auth"
              "or_id, authors where views_by_author_id.author = authors.id;")
    return c.fetchall()
    db.close()


def get_high_error_days():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("select views_per_day.day, float4((errors_per_day.errors * 100."
              "0)/views_per_day.views) as perc from errors_per_day, views_per"
              "_day where views_per_day.day = errors_per_day.day and float4(("
              "errors_per_day.errors * 100.0)/views_per_day.views) >= 1.0;")
    return c.fetchall()
    db.close()


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
