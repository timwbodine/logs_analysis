# Logs Analysis 
This is the Logs Analysis project for the Udacity Full Stack Nanodegree program.
## QuickStart
This project assumes you are running the Vagrant VM specified for this project.
1. Clone or download this repo into a directory accessible by your vagrant machine
2. Install the tabulate python library with ```pip install tabulate``` 
3. Install psycopg2 with ```pip install psycopg2```
4. Download and unzip the [newsdata.sql file](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) in the project directory.
5. Initialize the database with ```psql -d news -f newsdata.sql```
6. open the psql console with ```psql -d news```, and add the following views:
```
create view views_by_author_id as select articles.author, count(*) as num from articles, log where substring(log.path from '/article/(.*)')=articles.slug group by articles.author order by num desc;
create view errors_per_day as select date_trunc('day', time) as day, count(*) as errors from log where status != '200 OK' group by day order by day asc;
create view views_per_day as select date_trunc('day', time) as day, count(*) as views from log where status = '200 OK' group by day order by day asc;
```
alternatively, you can run ```python views.py``` to create these views.

7. Run ```python news_reporter.py``` to generate the output.txt file with the logs analysis
