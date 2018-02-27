import psycopg2


def addNecessaryViews():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("create view views_by_author_id as select articles.author, count(*) as num from articles, log where substring(log.path from '/article/(.*)')=articles.slug group by articles.author order by num desc;")
    c.execute("create view errors_per_day as select date_part('day', time) as day, count(*) as errors from log where status != '200 OK' group by day order by day asc;")
    c.execute("create view views_per_day as select date_part('day', time) as day, count(*) as views from log where status = '200 OK' group by day order by day asc;")
    db.commit()


addNecessaryViews()
