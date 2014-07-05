#urlrouter.py

"""Url rooter allow user to associate a function to an URL."""

import re

good_url = re.compile(r'^(\w+/)*(\w+((:(\w|/|\?|\.|\-|\_)+)|/)?)?$')

def concatenate_list_of_str(lis):
	r = ''
	for i in lis:
		r += str(i)
	return r

def is_malformed_url(url):
	if good_url.match(url):
		return False
	else:
		return True

class UnknowURL(Exception):
	pass
class MalformedURL(Exception):
	pass

class router:
	def __init__(self, dic = {}):
		self.main_node = Node()
		self.create_tree_from_dict(dic)

	def create_tree_from_dict(self, dic):
		self.main_node.create_children(dic)


	def run(self, url):
		if is_malformed_url(url):
			raise MalformedURL('The URL \'{}\' is not valid.'.format(url))
		else:
			try:
				self.main_node.next_url_or_func(url)
			except UnknowURL as error:
				raise UnknowURL("The url \'{}\' is not registered yet.".format(url))

class Node(dict):
	def __init__(self, dic={}):
		self.url_parse = re.compile(r'/')
		self.arg_parse = re.compile(r':')
		dict.__init__(self, dic)
	def next_url_or_func(self, url):
		first_word = self.url_parse.split(url)[0]
		args = concatenate_list_of_str(self.arg_parse.split(first_word)[1:])
		first_word = self.arg_parse.split(first_word)[0]
		next_url = args + re.sub(args, '', re.sub(first_word, '', url)[1:])
		if first_word in self.keys():
			try:
				self[first_word].next_url_or_func(next_url)
			except UnknowURL:
				raise UnknowURL()
		else:
			raise UnknowURL()

	def create_children(self, dic):
		for url in dic.keys():
			first_word = self.url_parse.split(url)[0]
			next_url = re.sub(first_word, '', url)[1:]
			if next_url is not '':			
				if not first_word in self.keys():
					self[first_word] = Node()
				self[first_word].create_children({next_url : dic[url]})
			else :
				self[first_word] = Element(dic[url])

class Element:
	def __init__(self, func):
		self.func = func
		self.args_parse = re.compile(r'/')
	def next_url_or_func(self, args):
		self.func(self.parse_args(args))
	def parse_args(self, args):
		return self.args_parse.split(args)
