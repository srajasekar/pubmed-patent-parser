class ParserHelper:
	
	def __init__(self):
		self.rtext = ''
	
	def rectext(self, node, tag):
		# author : ajbharani
		# It is necessary that we have to probe into the node 
		# recursively and pull out data wherever 'tag' appears
		for tagChild in node.childNodes:
			if tagChild.nodeName == tag:
				for pVals in tagChild.childNodes:
					if pVals.nodeType == 3:
						self.rtext += pVals.data
					else:
						self.rectext(pVals, tag)
			else:
				self.rectext(tagChild, tag)

	def date_format_helper(self,value):
		# author : saran
		prefix = '0'
		L = list(value)
		if len(L) < 2:
			prefix += value
		return prefix
