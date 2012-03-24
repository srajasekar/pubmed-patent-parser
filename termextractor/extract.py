from topia.termextract import extract
import MySQLdb

class TermExtractor(object):
	
	def __init__(self):
		self.extractor = extract.TermExtractor()
		self.extractor.filter = extract.DefaultFilter(singleStrengthMinOccur=3)
	
	def _removeNonAscii(self, string):
		return filter(lambda x: ord(x) < 128, string)
	
	def _removePuncts(self, string):
		punct_list = ['.', ',', '(', ')', '{', '}', '...']
		for punct in punct_list:
			if string[0].count(punct) > 0:
				return False
		else:
			return True
	
	def extract(self, string):
		string = self._removeNonAscii(string)
		return filter(self._removePuncts, self.extractor(string))
