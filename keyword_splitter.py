from __future__ import with_statement
import pickle
import os
import MySQLdb
import sys
import time

class KeywordSplitter(object):
	
	def __init__(self, url, username, password, db, pickle_filename, batch_size):
		self.url = url
		self.username = username
		self.password = password
		self.db = db
		self.pickle_filename = pickle_filename
		self.batch_size = batch_size
	
	def isDumpAvailable(self):
		return os.path.exists(self.pickle_filename)
	
	def loadDump(self):
		with open(self.pickle_filename, 'rb') as f:
			self.articles = pickle.load(f)
	
	def createDump(self):
		conn = MySQLdb.connect(self.url, self.username, self.password, self.db)
		query = 'select id, articlekeywords from pubmed_article where deleted = 0 order by id'
		cur = conn.cursor()
		cur.execute(query)
		self.articles = []
		for row in cur.fetchall():
			article = dict()
			article['Id'] = int(row[0])
			article['Keywords'] = row[1]
			self.articles.append(article)
		with open(self.pickle_filename, 'wb') as f:
			pickle.dump(self.articles, f)
		conn.close()
	
	def updateDump(self):
		print '(%s) Writing into Pickle file. DO NOT INTERRUPT' % (time.strftime('%H:%M:%S', time.localtime()))
		self.articles = self.articles[self.batch_size:]
		with open(self.pickle_filename, 'wb') as f:
			pickle.dump(self.articles, f)
		print '(%s) Pickle file write COMPLETE' % (time.strftime('%H:%M:%S', time.localtime()))
	
	def updateKeywords(self):
		self.current_batch = [] 	
		for article in self.articles[:self.batch_size]:
			_article = dict()
			article_keywords = map(lambda x: x.lower().strip(), article['Keywords'].split(','))
			keyword_set = set()
			for keyword in article_keywords:
				if (keyword[-2:] != 'es' and keyword[-1:] != 's'):
					if (((keyword + 's') not in keyword_set) and ((keyword + 'es') not in keyword_set)):
						keyword_set.add(keyword)
				elif (keyword[-2:] == 'es' and (keyword[:-2] not in keyword_set)):
					keyword_set.add(keyword)
				elif (keyword[-1:] == 's' and (keyword[:-1] not in keyword_set)):
					keyword_set.add(keyword)
			_article['Keywords'] = map(lambda x: x.replace("'","''"), list(keyword_set))
			_article['Id'] = article['Id']
			self.current_batch.append(_article)
		
	def genKeywordQueries(self):
		self.keywordQueries = []
		query = '''insert into pubmed_Keyword(ArticleId, Keyword) values (%d, '%s')'''
		for article in self.current_batch:
			for keyword in article['Keywords']:
				self.keywordQueries.append(query % (article['Id'], keyword))
	
	def uploadKeywords(self):
		conn = MySQLdb.connect(self.url, self.username, self.password, self.db)
		cur = conn.cursor()
		for query in self.keywordQueries:
			cur.execute(query)
		conn.commit()
		conn.close()
	
if __name__ == '__main__':
	ks = KeywordSplitter('mysql1.cs.stonybrook.edu', 'yvijayakumar', '108112539', 'yvijayakumar', 'pKeywords.pickle', int(sys.argv[1]))
	if ks.isDumpAvailable():
		ks.loadDump()
	else:
		ks.createDump()
	while True:
		remaining_articles = len(ks.articles)
		if remaining_articles == 0:
			break
		print '(%s) Remaining articles to process: %d' % (time.strftime('%H:%M:%S', time.localtime()), remaining_articles)
		print '(%s) Updating keywords' % (time.strftime('%H:%M:%S', time.localtime()))
		ks.updateKeywords()
		print '(%s) Generating queries' % (time.strftime('%H:%M:%S', time.localtime()))
		ks.genKeywordQueries()
		print '(%s) Uploading keywords' % (time.strftime('%H:%M:%S', time.localtime()))
		ks.uploadKeywords()
		print '(%s) Updating dump' % (time.strftime('%H:%M:%S', time.localtime()))
		ks.updateDump()
	
		