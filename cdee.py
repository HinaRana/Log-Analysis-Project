import psycopg2

ques1 = " 1. What are the most popular three articles of all time?"
query1 = """SELECT authors.name, articles.title,
        count(*) AS views FROM authors LEFT JOIN articles ON
        authors.id = articles.author LEFT JOIN log ON log.path
        LIKE concat('%',articles.slug) GROUP BY  articles.title,
        authors.name ORDER BY views DESC LIMIT 3"""

ques2 = " 2. Who are the most popular article authors of all time?"
query2 = """SELECT authors.name, count(*) AS views from authors
        left join
        articles ON authors.id = articles.author
        left join
        log ON concat('/article/', articles.slug)=log.path
        where log.status like '%200%' group by authors.name
        ORDER BY views desc"""

ques3 = " 3. On which days did more than 1% of requests lead to errors?"
query3 = """SELECT * from(
        select n.day, round(cast((b.hits*100) as numeric)/cast(n.hits as numeric), 2) as p from (select date(time) as day, count(*) as hits from log group by day) as n left join (select date(time) as day, count(*) as hits from log where status like '%404%' group by day) as b on n.day = b.day) as s where p > 1.0"""


def get_result(q):
    conn = psycopg2.connect(database="news")
    c = conn.cursor()
    c.execute(q)
    results = c.fetchall()
    conn.close()
    return results


def print_result1(q1, ques1):
    print(ques1)
    for q1 in q1[:3]:
        print("\t {:^10} -- {:^10} views".format(q1[1], q1[2]))


def print_result2(q2, ques2):
    print(ques2)
    for q2 in q2:
        print("\t {:^10} -- {:^10} views".format(q2[0], q2[1]))


def print_result3(q3, ques3):
    print(ques3)
    for i in range(len(q3)):
            print '\t', q3[i][0], '--', q3[i][1], "%errors"


query_result1 = get_result(query1)
query_result2 = get_result(query2)
query_result3 = get_result(query3)


print_result1(query_result1, ques1)
print_result2(query_result2, ques2)
print_result3(query_result3, ques3)
