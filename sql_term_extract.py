from __future__ import with_statement
from termextractor.extract import TermExtractor
import MySQLdb

class SQLTermExtractor(object):
	def __init__(self, url, username, password, dbname, keywordlog, batchsize):
		self.url = url
		self.username = username
		self.password = password
		self.dbname = dbname
		self.batchsize = batchsize
		self.keywordlog = keywordlog
		
	def getArticleWithoutKeywords(self):
		self.conn = MySQLdb.connect(self.url, self.username, self.password, self.dbname)
		self.cur = self.conn.cursor()
		query = ''' select Id, Abstract from pubmed_article where articlekeywords is null and deleted = 0 limit 0, %d''' % self.batchsize
		self.cur.execute(query)
		articles = []
		for row in self.cur.fetchall():
			article = dict()
			article['Id'] = int(row[0])
			article['Abstract'] = row[1]
			articles.append(article)	
		self.conn.close()
		return articles
	
	def getArticleKeywords(self):
		articles = self.getArticleWithoutKeywords()
		te = TermExtractor()
		for article in articles:
			article['Keywords'] = ','.join(map(lambda x: x[0].replace("'", "''"), te(article['Abstract'])))
		self.articles = articles
	
	def getInsertArticleKeywordsQueries(self):
		self.getArticleKeywords()
		query = '''update pubmed_article set ArticleKeywords = '%s' where Id = %d'''
		self.queries = []
		for article in self.articles:
			self.queries.append(query % (article['Keywords'], article['Id']))
	
	def insertArticleKeywords(self):		
		self.getInsertArticleKeywordsQueries()	
		self.conn = MySQLdb.connect(self.url, self.username, self.password, self.dbname)
		self.cur = self.conn.cursor()
		for query in self.queries:
			self.cur.execute(query)		
		self.conn.commit()		
		self.conn.close()
		self.logKeywords()
		return len(self.queries)
			
	def logKeywords(self):
		with open(self.keywordlog, 'a') as f:
			for article in self.articles:
				f.write(str(article) + '\n')
		

if __name__ == '__main__':
	sqte = SQLTermExtractor('mysql1.cs.stonybrook.edu', 'yvijayakumar', '108112539', 'yvijayakumar', 'keywordlog', 10)
	num_batches = 10
	for i in range(num_batches):
		print 'Running batch %d of %d' % (i+1, num_batches)
		print 'No. of article keywords inserted: %d' % (sqte.insertArticleKeywords())
	