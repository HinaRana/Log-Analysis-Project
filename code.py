import psycopg2
conn = psycopg2.connect(database="news")
c = conn.cursor()
query = "SELECT path FROM log GROUP BY path HAVING count(*) > 100000 order by count(*) desc"



c.execute(query)

results = c.fetchall()
conn.close()
print "Data:"
for result in results:
	print result

