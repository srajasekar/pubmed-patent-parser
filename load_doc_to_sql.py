# author : ajbharani
# author : saran

import MySQLdb

class LoadDocuments:
	def __init__(self, doc_path, sql_host, sql_user, sql_password, sql_db, batch_size):
		# author : ajbharani
		# constructor
		self.doc_path = doc_path
		self.sql_host = sql_host
		self.sql_user = sql_user
		self.sql_password = sql_password
		self.sql_db = sql_db
		self.batch_size = batch_size
	
	def push_documents(self, docs):
		# author : ajbharani
		# method to push a document batch into the DB
		# "docs": [{[ArticleIds], [ArticleKeywords], Abstract, Body, PubDate, [Titles], 
		#	[Contributors], [References], [Ref_Contributors]}, ...]
		# "ArticleKeywords" : [KW1, KW2, ...]
		# "ArticleIds": [{IdType, Id}, ...]
		# "Titles": [Title1, Title2, ...]
		# "Contributors": [{ContribType, Surname, GiveNames}, ...]
		# "References": [{RefId, RefType, Source, Title, PubYear, PubIdType, PubId}, ...]
		# "Ref_Contributors": [{ContribType, Surname, GivenNames}, ...]
		pass
	
	def _getArticleIds(self, filename):
		# author : saran
		# "ArticleIds": [{IdType, Id}, ...]
		pass
	
	def _getArticleKeywords(self, filename):
		# author : saran
		# "ArticleKeywords" : [KW1, KW2, ...]
		pass
	
	def _getAbstract(self, filename):
		# author : saran
		pass
	
	def _getBody(self, filename):
		# author : saran
		pass
	
	def _getPubDate(self, filename):
		# author : saran
		# Earliest publish date of the form YYYY-MM-DD
		pass
	
	def _getTitles(self, filename):
		# author : ajbharani
		# "Titles": [Title1, Title2, ...]
		pass
	
	def _getContributors(self, filename):
		# author : ajbharani
		# "Contributors": [{ContribType, Surname, GiveNames}, ...]
		pass
	
	def _getReferences(self, filename):
		# author : ajbharani
		# "References": [{RefId, RefType, Source, Title, PubYear, PubIdType, PubId}, ...]
		pass
	
	def _getRefContributors(self, filename):
		# author : ajbharani
		# "Ref_Contributors": [{ContribType, Surname, GivenNames}, ...]
		pass

if __name__ == '__main__':
	pass		