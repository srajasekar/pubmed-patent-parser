# author : ajbharani
# author : saran

import MySQLdb
from patentparser.parser import Parser

class DocumentLoader:
	def __init__(self, doc_list, sql_host, sql_user, sql_password, sql_db):
		# author : ajbharani
		# constructor
		self.doc_list = doc_list
		self.sql_host = sql_host
		self.sql_user = sql_user
		self.sql_password = sql_password
		self.sql_db = sql_db
	
	def loadDocuments(self):
		# author : ajbharani
		contents = []
		for doc in self.doc_list:
			content = []
			content[0] = self._getArticleIds(doc)
			content[1] = self._getArticleKeywords(doc)
			content[2] = self._getAbstract(doc)
			content[3] = self._getBody(doc)
			content[4] = self._getPubDate(doc)
			contents.append(content)
		self._push_contents(contents)
	
	def _validateAndQuote(self, string_to_validate):
		# author : ajbharani
		if string_to_validate == '':
			string_to_validate = 'NULL'
		else:
			string_to_validate = "'" + string_to_validate + "'"
		return string_to_validate
	
	def _getInsertArticleQuery(self, articleIds, articleKeywords, abstract, body, pubDate):
		
		articleIds = self._validateAndQuote(articleIds)
		
		keywords = ''
		for articleKeyword in articleKeywords:
			ak = articleKeyword.get('ArticleKeywords', None)
			if(ak != None):
				keywords += ak + ','
		keywords = keywords[:len(keywords) - 1] # to remove the trailing comma
		keywords = self._validateAndQuote(keywords)
		
		_abstract = ''
		abs = abstract.get('Abstract', None)
		if abs != None:
			_abstract = abs
		_abstract = self._validateAndQuote(_abstract)
		
		_body = ''
		bdy = body.get('Body', None)
		if bdy != None:
			_body = bdy
		_body = self._validateAndQuote(_body)
		
		_pubDate = ''
		pd = pubDate.get('PubDate', None)
		if pd != None:
			_pubDate = pd
		_pubDate = self._validateAndQuote(_pubDate)
		
		query = '''insert into pubmed_Article(ArticleIds, ArticleKeywords, Abstract, Body, PubDate) values 
			(%s, %s, %s, %s, %s)''' % (articleIds, keywords, _abstract, _body, _pubDate)
		
		return query
	
	def _push_contents(self, contents):
		# author : ajbharani
		# method to push contents into the DB
		# "contents": [{[ArticleIds], [ArticleKeywords], Abstract, Body, PubDate, [Titles], 
		#	[Contributors], [{References, Ref_Contributors}]}, ...]
		# "ArticleKeywords" : [KW1, KW2, ...]
		# "ArticleIds": [{IdType, Id}, ...]
		# "Titles": [Title1, Title2, ...]
		# "Contributors": [{ContribType, Surname, GivenNames}, ...]
		# "References": [{RefId, RefType, Source, Title, PubYear, PubIdType, PubId}, ...]
		# "RefContributor": [{ContribType, Surname, GivenNames}, ...]
		for content in contents:
			articleQuery = self._getInsertArticleQuery(content[0], content[1], content[2], conten[3], content[4])
			conn = MySQLdb.connect(self.sql_host, self.sql_user, self.sql_password, self.sql_db)
			cur = conn.cursor()
			cur.execute(articleQuery)
			articleId = cur.insert_id()
			print articleId
	
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
	ld = DocumentLoader(['AAPS_J_2008_Feb_8_10(1)_120-132.xml'], 'localhost', 'bharani', '', 'test')
	print ld.loadDocuments()	