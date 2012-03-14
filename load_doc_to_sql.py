# author : ajbharani
# author : saran

import MySQLdb
import unicodedata
from patentparser.parser import Parser
from datetime import datetime

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
			content.append(self._getArticleIds(doc))
			content.append(self._getArticleKeywords(doc))
			content.append(self._getAbstract(doc))
			content.append(self._getBody(doc))
			content.append(self._getPubDate(doc))
			content.append(self._getTitles(doc))
			contents.append(content)
		self._push_contents(contents)

	def _is_ascii(self, s):
		return all(ord(c) < 128 for c in s)
	
	def _validateAndQuote(self, string_to_validate):
		# author : ajbharani
		if self._is_ascii(string_to_validate) == False:
			string_to_validate = unicodedata.normalize('NFKD', string_to_validate).encode('ascii', 'ignore')
		string_to_validate = string_to_validate.replace("'", "''")
		if string_to_validate == '':
			string_to_validate = 'NULL'
		else:
			string_to_validate = "'" + str(string_to_validate) + "'"
		return string_to_validate
	
	def _getInsertArticleQuery(self, articleIds, articleKeywords, abstract, body, pubDate):		
		articleIds = self._validateAndQuote(str(articleIds))
		
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
	
	def _getInsertArticleTitleQueries(self, articleId, titles):
		result = []
		for title in titles:
			_title = ''
			tit = title.get('Title', None)
			if tit != None:
				_title = tit
			_title = self._validateAndQuote(_title)
			query = '''insert into pubmed_Title(ArticleId, Title) values
				(%d, %s)''' % (articleId, _title)
			result.append(query)
		return result
	
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
			articleQuery = self._getInsertArticleQuery(content[0], content[1], content[2], content[3], content[4])
			conn = MySQLdb.connect(self.sql_host, self.sql_user, self.sql_password, self.sql_db)
			cur = conn.cursor()
			cur.execute(articleQuery)
			articleId = conn.insert_id()
			articleTitleQueries = self._getInsertArticleTitleQueries(articleId, content[5])
			for articleTitleQuery in articleTitleQueries:
				cur.execute(articleTitleQuery)
			conn.commit()
			conn.close()
	
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
	ld = DocumentLoader(['AAPS_J_2008_Feb_8_10(1)_120-132.xml'], 'localhost', 'bharani', '', 'test')
	ld.loadDocuments()
