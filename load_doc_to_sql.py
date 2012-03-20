# author : ajbharani
# author : saran

import MySQLdb
import unicodedata
import os
import pickle
import time
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
	
	def loadDocuments(self, log_file):
		# author : ajbharani
		try:
			contents = []
			for doc in self.doc_list:
				content = []
				content.append(self._getArticleIds(doc))
				content.append(self._getArticleKeywords(doc))
				content.append(self._getAbstract(doc))
				content.append(self._getBody(doc))
				content.append(self._getPubDate(doc))
				content.append(self._getTitles(doc))
				content.append(self._getContributors(doc))
				content.append(self._getReferences(doc))
				contents.append(content)
			self._push_contents(contents)
		except Exception as inst:
			print 'Exception while parsing.'
			print inst
			f = open(log_file, 'a')
			f.write('Error while parsing. Batch below\n')
			for doc in self.doc_list:
				f.write(doc + '\n')
			f.close()

	def _is_ascii(self, s):
		# author : ajbharani
		return all(ord(c) < 128 for c in s)
	
	def _validateAndQuote(self, string_to_validate):
		# author : ajbharani
		if string_to_validate == None:
			string_to_validate = ''
		if self._is_ascii(string_to_validate) == False:
			string_to_validate = unicodedata.normalize('NFKD', string_to_validate).encode('ascii', 'ignore')
		string_to_validate = string_to_validate.replace("'", "''")
		if string_to_validate == '':
			string_to_validate = 'NULL'
		else:
			string_to_validate = "'" + str(string_to_validate) + "'"
		return string_to_validate
	
	def _getInsertArticleQuery(self, articleIds, articleKeywords, abstract, body, pubDate):
		# author : ajbharani
		articleIds = self._validateAndQuote(str(articleIds))
		
		keywords = ''
		for articleKeyword in articleKeywords:
			ak = articleKeyword.get('ArticleKeywords', None)
			if(ak != None):
				keywords += ak + ','
		keywords = keywords[:len(keywords) - 1] # to remove the trailing comma
		keywords = self._validateAndQuote(keywords)
		
		_abstract = abstract.get('Abstract', '')
		_abstract = self._validateAndQuote(_abstract)
		
		_body = body.get('Body', '')
		_body = self._validateAndQuote(_body)
		
		_pubDate = pubDate.get('PubDate', '')
		_pubDate = self._validateAndQuote(_pubDate)
		
		query = '''insert into pubmed_Article(ArticleIds, ArticleKeywords, Abstract, Body, PubDate) values 
			(%s, %s, %s, %s, %s)''' % (articleIds, keywords, _abstract, _body, _pubDate)
		
		return query
	
	def _getInsertArticleTitleQueries(self, articleId, titles):
		# author : ajbharani
		result = []
		for title in titles:
			_title = title.get('Title', '')
			_title = self._validateAndQuote(_title)
			query = '''insert into pubmed_Title(ArticleId, Title) values
				(%d, %s)''' % (articleId, _title)
			result.append(query)
		return result

	def _getInsertContributorQueries(self, articleId, contributors):
		# author : ajbharani
		result = []
		for contributor in contributors:
			_type = self._validateAndQuote(contributor.get('ContribType', ''))
			_surname = self._validateAndQuote(contributor.get('Surname', ''))
			_given_names = self._validateAndQuote(contributor.get('GivenNames', ''))
			query = '''insert into pubmed_Contributor(ArticleId, ContribType, Surname, GivenNames) values
				(%d, %s, %s, %s)''' % (articleId, _type, _surname, _given_names)
			result.append(query)
		return result
	
	def _getInsertReferenceQueries(self, articleId, references):
		# author : ajbharani
		result = []
		for reference in references:
			_refid = self._validateAndQuote(reference.get('RefId', ''))
			_reftype = self._validateAndQuote(reference.get('RefType', ''))
			_source = self._validateAndQuote(reference.get('Source', ''))
			_title = self._validateAndQuote(reference.get('Title', ''))
			_pubyear = self._validateAndQuote(reference.get('PubYear', ''))
			_pubidtype = self._validateAndQuote(reference.get('PubIdType', ''))
			_pubid = self._validateAndQuote(reference.get('PubId', ''))
			query = '''insert into pubmed_Reference(ArticleId, RefId, RefType, Source, Title, PubYear, PubIdType, PubId)
				values(%d, %s, %s, %s, %s, %s, %s, %s)''' % (articleId, _refid, _reftype, _source, _title, _pubyear, 
					_pubidtype, _pubid)
			contributors = reference.get('RefContributor', [])
			result.append((query, contributors))
		return result
	
	def _getInsertRefContributorQueries(self, referenceId, contributors):
		# author : ajbharani
		result = []
		for contributor in contributors:
			_type = self._validateAndQuote(contributor.get('ContribType', ''))
			_surname = self._validateAndQuote(contributor.get('Surname', ''))
			_given_names = self._validateAndQuote(contributor.get('GivenNames', ''))
			query = '''insert into pubmed_RefContributor(RefId, ContribType, Surname, GivenNames) values
				(%d, %s, %s, %s)''' % (referenceId, _type, _surname, _given_names)
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
			contributorQueries = self._getInsertContributorQueries(articleId, content[6])
			for contributorQuery in contributorQueries:
				cur.execute(contributorQuery)
			referenceQueries = self._getInsertReferenceQueries(articleId, content[7])
			for referenceQuery, contributors in referenceQueries:
				cur.execute(referenceQuery)
				referenceId = conn.insert_id()
				refContributorQueries = self._getInsertRefContributorQueries(referenceId, contributors)
				for refContributorQuery in refContributorQueries:
					cur.execute(refContributorQuery)
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
			date =  pubdate.get('pub-date', None)
			date_object = datetime.strptime(date, '%Y-%m-%d')
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
			entry['GivenNames'] = contributor.get('given-names', None)
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
	# Initialize file names
	log_file = 'load_log.txt'
	corpus_file_names = 'pubmed_file_list.txt'
	remaining_files_pickle = 'remaining_files.pickle'
	batch_size = 1000
	# Log file to log if there is any exception
	# Clear the log file first
	open(log_file, 'w').close()
	# Check if a pickle file already exist for
	# loading the remaining file to be processed
	if os.path.exists(remaining_files_pickle):
		f = open(remaining_files_pickle, 'rb')
		input_file_list = pickle.load(f)
		f.close()
	# If pickle not available, load the file 
	# list into a python list for processing
	else:
		f = open(corpus_file_names)
		input_file_list = f.readlines()
		# Eliminate the trailing '\n'
		input_file_list = map(lambda x: x.replace('\n',''), input_file_list)
		f.close()
	# Process the input_file_list until it is empty
	while len(input_file_list) > 0:
		print 'Remaining files to process: ' + str(len(input_file_list))
		# Pick first 1000 files from the input file list
		# for the current batch
		current_batch = input_file_list[:batch_size]
		# Load the documents into the database
		print 'Started to load ' + str(batch_size) + ' documents'
		print 'Start time: ' + time.strftime('%H:%M:%S', time.localtime())
		ld = DocumentLoader(current_batch, 'localhost', 'bharani', '', 'test')
		ld.loadDocuments(log_file)
		print 'End time: ' + time.strftime('%H:%M:%S', time.localtime())
		# When done successfully, update the remaining files
		# and the pickle file appropriately
		input_file_list = input_file_list[batch_size:]
		f = open(remaining_files_pickle, 'wb')
		pickle.dump(input_file_list, f)
		f.close()		
	
				
