import psycopg2


def connect(database):
    try:
        db = psycopg2.connect("dbname={}".format(database))
        cursor = db.cursor()
        return db, cursor
    except:
        print("There was an error connecting to the database.")

def addNecessaryViews():
    db, cursor = connect("news");
    cursor.execute("create view views_by_author_id as select articles.au"
                   "thor, count(*) as num from articles, log where substri"
                   "ng(log.path from '/article/(.*)')=articles.slug group "
                   "by articles.author order by num desc;")
    cursor.execute("create view errors_per_day as select date_part("
                   "'day', time) as day, count(*) as errors from log"
                   " where status != '200 OK' group by day order by day asc;")
    cursor.execute("create view views_per_day as select date_part('day', "
                   "time) as day, count(*) as views from log where status "
                   "= '200 OK' group by day order by day asc;")
    db.commit()


addNecessaryViews()
