# author : ajbharani
# author : saran

import MySQLdb
from patentparser.parser import Parser
from datetime import datetime

class LoadDocuments:
	def __init__(self, doc_list, sql_host, sql_user, sql_password, sql_db, batch_size):
		# author : ajbharani
		# constructor
		self.doc_list = doc_list
		self.sql_host = sql_host
		self.sql_user = sql_user
		self.sql_password = sql_password
		self.sql_db = sql_db
		self.batch_size = batch_size
	
	def push_documents(self, contents):
		# author : ajbharani
		# method to push a document batch into the DB
		# "docs": [{[ArticleIds], [ArticleKeywords], Abstract, Body, PubDate, [Titles], 
		#	[Contributors], [{References, Ref_Contributors}]}, ...]
		# "ArticleKeywords" : [KW1, KW2, ...]
		# "ArticleIds": [{IdType, Id}, ...]
		# "Titles": [Title1, Title2, ...]
		# "Contributors": [{ContribType, Surname, GivenNames}, ...]
		# "References": [{RefId, RefType, Source, Title, PubYear, PubIdType, PubId}, ...]
		# "RefContributor": [{ContribType, Surname, GivenNames}, ...]
		pass
	
	def _getArticleIds(self, filename):
		# author : saran
		# "ArticleIds": [{IdType, Id},{IdType, Id}, ...]
		p = Parser(filename)
		articleIDs = p.ids()
		result = []
		for articleID in articleIDs:
			entry = dict()
			entry['IdType'] = articleID.get('id-type', None)
			entry['Id'] = articleID.get('id', None)
			result.append(entry)
		return result
	
	def _getArticleKeywords(self, filename):
		# author : saran
		# Returns : [{ArticleKeywords: 'KW1'},{ArticleKeywords: 'KW2'}, ...]
		p = Parser(filename)
		keywords = p.keywords()
		result = []
		for keyword in keywords:
			entry = dict()
			entry['ArticleKeywords'] = keyword
			result.append(entry)
		return result
	
	def _getAbstract(self, filename):
		# author : saran
		# Returns {Abstract:'abstract of the patent'}
		p = Parser(filename)
		abstract = p.abstract()
		result = dict()
		result['Abstract'] = abstract
		return result
	
	def _getBody(self, filename):
		# author : saran
		# Returns {Body:'body of the patent'}
		p = Parser(filename)
		body = p.body()
		result = dict()
		result['Body'] = body
		return result
	
	def _getPubDate(self, filename):
		# author : saran
		# Earliest publish date of the form YYYY-MM-DD
		# Returns: {PubDate:'Earliest publish date of the form YYYY-MM-DD'}
		p = Parser(filename)
		pubdates = p.pubdates()
		dates = []
		result = dict()
		for pubdate in pubdates:
			date =  pubdate.get('pub-date',None)
			date_object = datetime.strptime(date,'%Y-%m-%d')
			dates.append(date_object)
		max_date = max(dates)
		result['PubDate'] = max_date.strftime('%Y-%m-%d')
		return result
		
		
	
	def _getTitles(self, filename):
		# author : ajbharani
		# "Titles": [Title1, Title2, ...]
		p = Parser(filename)
		titles = p.titles()
		result = []
		for title in titles:
			entry = dict()
			entry['Title'] = title
			result.append(entry)
		return result
	
	def _getContributors(self, filename):
		# author : ajbharani
		# "Contributors": [{ContribType, Surname, GivenNames}, ...]
		p = Parser(filename)
		contributors = p.contributors()
		result = []
		for contributor in contributors:
			entry = dict()
			entry['ContribType'] = contributor.get('type', None)
			entry['Surname'] = contributor.get('surname', None)
			entry['GivenNames'] = contributor.get('GivenNames', None)
			result.append(entry)
		return result
	
	def _getReferences(self, filename):
		# author : ajbharani
		# "References": [{RefId, RefType, Source, Title, PubYear, PubIdType, PubId}, ...]
		# "RefContributor": [{ContribType, Surname, GivenNames}, ...]
		p = Parser(filename)
		references = p.references()
		result = []
		for reference in references:
			entry = dict()
			entry['RefId'] = reference.get('id', None)
			entry['RefType'] = reference.get('type', None)
			entry['Source'] = reference.get('source', None)
			entry['Title'] = reference.get('article-title', None)
			entry['PubYear'] = reference.get('year', None)
			entry['PubIdType'] = reference.get('pub-id-type', None)
			entry['PubId'] = reference.get('pub-id', None)
			contributors = reference.get('person-list', None)
			entry['RefContributor'] = []
			if contributors != None:
				for contributor in contributors:
					person = dict()
					person['ContribType'] = contributor.get('type', None)
					person['Surname'] = contributor.get('surname', None)
					person['GivenNames'] = contributor.get('given-names', None)
					entry['RefContributor'].append(person)
			result.append(entry)
		return result

if __name__ == '__main__':
	pass
