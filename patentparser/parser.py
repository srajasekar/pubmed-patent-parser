from xml.dom.minidom import parse
from parserhelper import ParserHelper

class Parser:
	
	def __init__(self, fileName):
		self.fileName = fileName
		self.dom = parse(self.fileName)
	
	def pubdates(self):
		# author : saran
		# article -> front -> article-meta -> pub-date
		# [date1, date2]
		# date:
		# {'pub-type':'val','pub-date':'mm-dd-yyyy'}
		pass
	
	def ids(self):
		# author : saran
		# article -> front -> article-meta -> article-id
		# [{'id-type':'id-type-val','id':'id-val'}]
		pass

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
		# author : saran
		# article -> front -> article-meta -> title-group -> article-title
		# ['tit1', 'tit2']
		pass
	
	def contributors(self):
		# author : saran
		# article -> front -> article-meta -> contrib-group
		# [Person1, Person2]
		# Person:
		# {'type':'val', 'surname':'val', 'given-names':'val'}
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
								if refattr.nodeName == 'element-citation' or refattr.nodeName == 'mixed-citation':
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
															personDict['surname'] = name.firstChild.data
														elif name.nodeName == 'given-names':
															personDict['given-names'] = name.firstChild.data
													personDictList.append(personDict)
											refdict['person-list'] = personDictList	
										elif element.nodeName == 'source':
											refdict['source'] = element.firstChild.data
										elif element.nodeName == 'article-title':
											refdict['article-title'] = element.firstChild.data
										elif element.nodeName == 'year':
											refdict['year'] = element.firstChild.data
										elif element.nodeName == 'pub-id':
											refdict['pub-id-type'] = element.getAttribute('pub-id-type')
											refdict['pub-id'] = element.firstChild.data						
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
			
