from xml.dom.minidom import parse

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
		pass
	
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
							result = result.join(pVals.data)
		return result
