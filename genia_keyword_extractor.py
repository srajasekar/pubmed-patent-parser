from __future__ import with_statement
from xml.dom.minidom import parse

import MySQLdb
import os
import pickle

def get_keywords_as_csv(xml_filename):
	doc = parse(xml_filename)
	elements = doc.getElementsByTagName('ENAMEX')
	keywords = []
	for element in elements:
		keywords.append(element.firstChild.nodeValue.replace("'","''"))
	return ','.join(keywords)

def get_file_list(doc_path):
	file_list = []
	for root, dirs, files in os.walk(doc_path):
		for val in files:
			if val.find('.xml') != -1:
				file_path = root + '/' + val
				file_list.append({'Id':int(val[:-4]),'Path':file_path})
	return file_list

def get_keywords_from_xml(doc_path):
	print 'Getting file list'
	file_list = get_file_list(doc_path)
	total_files = len(file_list)
	for index,_file in enumerate(file_list):
		print 'Extracting keyword %d of %d' % (index + 1, total_files)
		_file['Keywords'] = get_keywords_as_csv(_file['Path'])
	return file_list

def upload_keywords(doc_path):
	with open('genia_keyword.pickle','rb') as f:
		file_keywords_list =  pickle.load(f)
	total_files = len(file_keywords_list)
	query_template = '''update pubmed_article set GeniaKeywords = '%s' where Id = %d'''
	conn = MySQLdb.connect('mysql1.cs.stonybrook.edu', 'yvijayakumar', '108112539', 'yvijayakumar')
	cur = conn.cursor()
	for index,file_keywords in enumerate(file_keywords_list):
		query = query_template % (file_keywords['Keywords'], file_keywords['Id'])
		print 'Uploading keyword list %d of %d' % (index + 1, total_files)
		try:
			cur.execute(query)
		except:
			print query
	conn.commit()
	conn.close()
				
if __name__ == '__main__':
	upload_keywords('/Users/bharani/Documents/CSE507-CL/Project/abs_kwd')
