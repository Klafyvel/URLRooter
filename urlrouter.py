#urlrouter.py

"""Url rooter allow user to associate a function to an URL."""

import re

good_url = re.compile(r'^/?(\w+/)*(\w+(:\w+)*)?$') # some black magic :p

class UnknowURL(Exception):
	pass
class MalformedURL(Exception):
	pass
class OverWritingExistingURL(Exception):
	pass

class router:
	"""
	The control class. 
	"""
	def __init__(self, dic = {}):
		self.main_node = Node()
		self.dic = dic
		self.create_tree_from_dict()

	def create_tree_from_dict(self):
		"""
		Creates the Nodes and the Elements from a dictionary.
		"""
		try:
			self.main_node.create_children(self.dic)
		except OverWritingExistingURL as url:
			raise OverWritingExistingURL("The URL \'{}\'  is in conflict with a function. \
				Cannot be created.".format(url))


	def run(self, url):
		"""
		Tries to run the function associated to an url.
		"""
		if not good_url.match(url):
			raise MalformedURL('The URL \'{}\' is not valid.'.format(url))
		else:
			url_cpy = url
			if url[0] is not '/':
				url_cpy = '/' + url
			try:
				self.main_node.next_url_or_func(url_cpy)
			except UnknowURL as error:
				raise UnknowURL("The URL \'{}\' is not registered yet.".format(url))

class Node(dict):
	"""
	The Nodes contain only other Nodes or Elements.
	"""
	def __init__(self, dic={}):
		self.url_parse = re.compile(r'/')
		self.arg_parse = re.compile(r':')
		dict.__init__(self, dic)
	def next_url_or_func(self, url):
		"""
		Tries to give to the appropriate child the url.
		"""
		first_word = self.url_parse.split(url)[0]
		first_word = self.arg_parse.split(first_word)[0]
		next_url = re.sub(first_word, '', url)[1:]
		if first_word in self.keys():
			try:
				self[first_word].next_url_or_func(next_url)
			except UnknowURL:
				raise UnknowURL()
		else:
			raise UnknowURL()

	def create_children(self, dic):
		"""
		Creates the children from a dictionary.
		"""
		for url in dic.keys():
			first_word = self.url_parse.split(url)[0]
			next_url = re.sub(first_word, '', url)[1:]
			if next_url is not '':
				if not first_word in self.keys():
					self[first_word] = Node()
				if isinstance(self[first_word], Element):
					raise OverWritingExistingURL(url)
				try:
					self[first_word].create_children({next_url : dic[url]})
				except OverWritingExistingURL:
					raise OverWritingExistingURL(url)
			else :
				self[first_word] = Element(dic[url])

class Element:
	"""
	The Elements are used to call the functions.
	"""
	def __init__(self, func):
		self.func = func
		self.args_parse = re.compile(r':')
	def next_url_or_func(self, args):
		"""
		Call the function.
		"""
		self.func(self.parse_args(args))
	def parse_args(self, args):
		"""
		The arguments given as 'e:foo:bar' are parsed as ['e', 'foo', 'bar'].
		"""
		return self.args_parse.split(args)

