from xml.dom.minidom import parse
from parserhelper import ParserHelper

class Parser:
	
	def __init__(self, fileName):
		self.fileName = fileName
		self.dom = parse(self.fileName)
	
	def pubdates(self):
		# author : saranya
		# article -> front -> article-meta -> pub-date
		# [date1, date2]
		# date:
		# {'pub-type':'val','pub-date':'mm-dd-yyyy'}
		ph = ParserHelper()
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
									try:
										month = tagsInPubDate.firstChild.data
									except AttributeError:
										month = '01'
									month = ph.date_format_helper(month)
									month += '-'
								if tagsInPubDate.nodeName == 'day':
									try:
										day = tagsInPubDate.firstChild.data
									except AttributeError:
										day = '01'
									day = ph.date_format_helper(day)
									day += '-'
								if tagsInPubDate.nodeName == 'year':
									try:
										year = tagsInPubDate.firstChild.data
									except AttributeError:
										year = '1900'
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
							try:
								articleId['id'] = articleMetaTags.firstChild.data
							except AttributeError:
								articleId['id'] = None
							result.append(articleId)
		return result

	def body(self):
		# author : ajbharani
		# article -> body -> sec(recursive) -> p
		# 'body'
		result = ''
		bodies = self.dom.getElementsByTagName('body')
		for body in bodies:
			ph = ParserHelper()
			ph.rectext(body,'p')
			result += ph.rtext
		return result
	
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
									try:
										_aTitle = articleTitles.firstChild.data
									except AttributeError:
										_aTitle = None
									result.append(_aTitle)
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
													try:
														contributor['surname'] = tagsInName.firstChild.data
													except AttributeError:
														contributor['surname'] = None	
												if tagsInName.nodeName == 'given-names':
													try:
														contributor['given-names'] = tagsInName.firstChild.data
													except AttributeError:
														contributor['given-names'] = None
											result.append(contributor)
		return result
	
	def keywords(self):
		# author : ajbharani
		# article -> front -> article-meta -> kwd-group
		# ['kwd1', 'kwd2]
		pass
		
	def references(self):
		# author : ajbharani
		# article -> back -> ref-list -> ref
		# ['Ref1', 'Ref2']
		# Ref:
		# {'id':'id-val', 'type':'type-val', 'person-list':['list-of-persons'], 'source':'source-val', 
		#	'article-title':'val', 'year': 'val', 'pub-id-type':'val', 'pub-id':'val'}
		# Person:
		# {'type':'val', 'surname':'val', 'given-names':'val'}
		refs = []
		rtags = self.dom.getElementsByTagName('back')
		for rtag in rtags:
			for reflist in rtag.childNodes:
				if reflist.nodeName == 'ref-list':
					for ref in reflist.childNodes:
						if ref.nodeName == 'ref':
							refdict = dict()
							refdict['id'] = ref.getAttribute('id')
							for refattr in ref.childNodes:
								if refattr.nodeName.find('citation') != -1:
									refdict['type'] = refattr.getAttribute('publication-type')
									for element in refattr.childNodes:
										if element.nodeName == 'person-group':
											grptype = element.getAttribute('person-group-type')
											personDictList = []
											for person in element.childNodes:												
												if person.nodeName == 'name':
													personDict = dict()
													personDict['type'] = grptype
													for name in person.childNodes:
														if name.nodeName == 'surname':
															try:
																personDict['surname'] = name.firstChild.data
															except AttributeError:
																personDict['surname'] = None
														elif name.nodeName == 'given-names':
															try:
																personDict['given-names'] = name.firstChild.data
															except AttributeError:
																personDict['given-names'] = None
													personDictList.append(personDict)
											refdict['person-list'] = personDictList	
										elif element.nodeName == 'source':
											try:
												refdict['source'] = element.firstChild.data
											except AttributeError:
												refdict['source'] = None
										elif element.nodeName == 'article-title':
											try:
												refdict['article-title'] = element.firstChild.data
											except AttributeError:
												refdict['article-title'] = None
										elif element.nodeName == 'year':
											try:
												refdict['year'] = element.firstChild.data
											except AttributeError:
												refdict['year'] = None
										elif element.nodeName == 'pub-id':
											refdict['pub-id-type'] = element.getAttribute('pub-id-type')
											try:
												refdict['pub-id'] = element.firstChild.data
											except AttributeError:
												refdict['pub-id'] = None					
							refs.append(refdict)
		return refs
	
	def abstract(self):
		# author : ajbharani
		# article -> front -> abstract
		# 'abstract'
		result = ''
		abstracts = self.dom.getElementsByTagName('abstract')
		for abstract in abstracts:
			ph = ParserHelper()
			ph.rectext(abstract,'p')
			result += ph.rtext
		return result
			
