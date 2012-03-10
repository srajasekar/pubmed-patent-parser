class ParserHelper:
	
	def __init__(self):
		self.rtext = ''
	
	def rectext(self, node, tag):
		# It is necessary that we have to probe into an abstract 
		# recursively and pull out data wherever <p> tag appears
		for tagChild in node.childNodes:
			if tagChild.nodeName == tag:
				for pVals in tagChild.childNodes:
					if pVals.nodeType == 3:
						self.rtext += pVals.data
					else:
						self.rectext(pVals, tag)
			else:
				self.rectext(tagChild, tag)
