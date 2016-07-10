from BaseHandler import BaseHandler
import torndb
import tornado.web
import concurrent.futures
import tornado.escape
from tornado import gen
import unicodedata
import re
import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence

class  SearchHandler(BaseHandler):
	def  get(self):
		keyName = "s"
		keyword = self.get_argument(keyName)
		text = keyword.decode("utf8")
		str = '%%' + text + '%%'
		users = self.db.query("SELECT * FROM users WHERE name like %s", str)
		entries = self.db.query("SELECT * FROM entries WHERE html like %s", str)
		tr4w = TextRank4Keyword()
		keywordSearchUser(self.db, text, tr4w, users)
		keywordSearchEntries(self.db, text, tr4w, entries)
		self.render("search.html", users = users, entries = entries)
	def  post(self): 
		pass

def  keywordSearchUser(database, text, tr4w, users):
	tr4w.analyze(text = text, lower = True, window=100)
	for words in tr4w.words_no_stop_words:
		for word in words:
			#print word
			str = '%%' + word + '%%'
			items = database.query("SELECT * FROM users WHERE name like %s", str)
			if items:
				for item in items:
					if not item in users:
						users.append(item)

def  keywordSearchEntries(database, text, tr4w, entries):
	tr4w.analyze(text = text, lower = True, window=100)
	for item in tr4w.get_keywords(20, word_min_len=1):
		str = '%%' + item.word + '%%'
		items = database.query("SELECT * FROM entries WHERE html like %s", str)
		if items:
			for item in items:
				if not item in entries:
					entries.append(item)