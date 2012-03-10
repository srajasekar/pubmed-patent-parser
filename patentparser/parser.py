from xml.dom.minidom import parse

class Parser:
	
	def __init__(self, fileName):
		self.fileName = fileName
		self.dom = parse(self.fileName)
	
	def date_format_helper(self,value):
		prefix = '0'
		L = list(value)
		if len(L) < 2:
			prefix += value
		return prefix
	
	def pubdates(self):
		# author : saranya
		# article -> front -> article-meta -> pub-date
		# [date1, date2]
		# date:
		# {'pub-type':'val','pub-date':'mm-dd-yyyy'}
		result = []		
		startTag = self.dom.getElementsByTagName('front')
		for front in startTag:
			for tagsInFront in front.childNodes:
				if tagsInFront.nodeName == 'article-meta':
					for articleMetaTags in tagsInFront.childNodes:
						if articleMetaTags.nodeName == 'pub-date':
							date = dict()
							datestr = '' 
							month = '01-'
							day = '01-'
							year = ''
							date['pub-type'] = articleMetaTags.getAttribute('pub-type')
							for tagsInPubDate in articleMetaTags.childNodes:
								if tagsInPubDate.nodeName == 'month':
									month = tagsInPubDate.firstChild.data
									month = self.date_format_helper(month)
									month += '-'
								if tagsInPubDate.nodeName == 'day':
									day = tagsInPubDate.firstChild.data
									day = self.date_format_helper(day)
									day += '-'
								if tagsInPubDate.nodeName == 'year':
									year = tagsInPubDate.firstChild.data
							datestr += month
							datestr += day
							datestr += year
							date['pub-date'] = datestr
							result.append(date)
		return result
			
	def ids(self):
		# author : saranya
		# article -> front -> article-meta -> article-id
		# [{'id-type':'id-type-val','id':'id-val'}]
		result = []	
		startTag = self.dom.getElementsByTagName('front')
		for front in startTag:
			for tagsInFront in front.childNodes:
				if tagsInFront.nodeName == 'article-meta':
					for articleMetaTags in tagsInFront.childNodes:
						if articleMetaTags.nodeName == 'article-id':	
							articleId = dict()
							articleId['id-type'] = articleMetaTags.getAttribute('pub-id-type')
							articleId['id'] = articleMetaTags.firstChild.data
							result.append(articleId)
		return result

	def body(self):
		# author : ajbharani
		# article -> body -> sec(recursive) -> p
		# 'body'
		pass
	
	def titles(self):
		# author : saranya
		# article -> front -> article-meta -> title-group -> article-title
		# ['tit1', 'tit2']
		result = []		
		startTag = self.dom.getElementsByTagName('front')
		for front in startTag:
			for tagsInFront in front.childNodes:
				if tagsInFront.nodeName == 'article-meta':
					for titleGroups in tagsInFront.childNodes:
						if titleGroups.nodeName == 'title-group':
							for articleTitles in titleGroups.childNodes:
								if articleTitles.nodeName == 'article-title':
									result.append(articleTitles.firstChild.data)
		return result
	
	def contributors(self):
		# author : saran
		# article -> front -> article-meta -> contrib-group
		# [Person1, Person2]
		# Person:
		# {'type':'val', 'surname':'val', 'given-names':'val'}
		result = []		
		startTag = self.dom.getElementsByTagName('front')
		for front in startTag:
			for tagsInFront in front.childNodes:
				if tagsInFront.nodeName == 'article-meta':
					for contribGroups in tagsInFront.childNodes:
						if contribGroups.nodeName == 'contrib-group':
							for contrib in contribGroups.childNodes:
								if contrib.nodeName == 'contrib':
									contributor = dict()
									contributor['type'] = contrib.getAttribute('contrib-type')
									for tagsInContrib in contrib.childNodes:
										if tagsInContrib.nodeName == 'name':
											for tagsInName in tagsInContrib.childNodes:
												if tagsInName.nodeName == 'surname':
													contributor['surname'] = tagsInName.firstChild.data		
												if tagsInName.nodeName == 'given-names':
													contributor['given-names'] = tagsInName.firstChild.data
											result.append(contributor)
		return result
			
	def references(self):
		# author : ajbharani
		# article -> back -> ref-list -> ref
		# ['Ref1', 'Ref2']
		# Ref:
		# {'id':'id-val', 'type':'type-val', 'person-list':['list-of-persons'], 'source':'source-val', 
		#	'article-title':'val', 'year':'val', 'pub-id-type':'val', 'pub-id':'val'}
		# Person:
		# {'type':'val', 'surname':'val', 'given-names':'val'}
		pass

	def abstract(self):
		# author : ajbharani
		# article -> front -> abstract
		# 'abstract'
		result = ''
		abstracts = self.dom.getElementsByTagName('abstract')
		for abstract in abstracts:
			for abstractChild in abstract.childNodes:
				if abstractChild.nodeName == 'p':
					for pVals in abstractChild.childNodes:
						if pVals.nodeType == 3:
							result += (pVals.data)
		return result
