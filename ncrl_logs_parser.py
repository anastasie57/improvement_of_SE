## This is script for parsing logs from National Corpus of Russian Language. Also you can use it to create frequency list of different search patterns.

import codecs
import urllib
import os
import re

def decoder(path): ## all logs from NCRL should be decoded, as there are problems with showing all symbols before decoding
	all_queries = 0 ## counter of all queries from all given days
	for root, dirs, files in os.walk(path):
		for name in files:
			if name.endswith(".log"): ## logs from NCRL are usually kept in many files, one file (format .log) for one day 
				file = codecs.open(name, encoding = "utf-8")
				strings = file.read().split("\n")
				all_queries += len(strings)

				decoded_file = codecs.open("new" + name, "w", encoding = "cp1251")

				for i in strings:
					try:
						decoded_file.write(urllib.parse.unquote(i, encoding = "cp1251"))
					except:
						continue
					decoded_file.write("\n")

	return all_queries

def clear_tags_from_queries(path): ## function of clearing out tags of filtering corpus, numbers of found documents and so on
	common_file = codecs.open("common_ncrl_queries.log", "a", encoding = "cp1251")

	for root, dirs, files in os.walk(path):
		for name in files:
			if name.startswith("new") and name.endswith(".log"):
				f = codecs.open(name)
				strings = f.read().split("\n")
				for i in strings:
				try:
					time = i.split(" ")[0]
					tags = i.split(" ")[1].split("&")
					needed_tags = []
					for k in tags:
						if any(k.startswith(tag) for tag in ["req", "lex", "gramm", "use"]) and not k.endswith("="): ## these tags are, respectively, "exact request", "exact lexeme", "grammatical pattern", "used distance between words"
							needed_tags.append(k)
					common_file.write(time + " " + "&".join(needed_tags))
					common_file.write("\n")
				except:
					continue 

	return True

def create_morph_frequency_list(file): ## function of creating frequency list of morphological query patterns
	freq_grammar_tags = {}
	gramms = 0
	onegramms = 0

	for root, dirs, files in os.walk('.'):
		for name in files:
			if name.endswith(".log") and name.startswith("new"):
				f = codecs.open(name)
				strings = f.read().split("\n")
				for i in strings:
				try:
					time = i.split(" ")[0]
					tags = i.split(" ")[1].split("&")
					needed_tags = []
					gi = 0
					for k in tags:
						if any(k.startswith(tag) for tag in ["req", "lex", "gramm", "use"]) and not k.endswith("="):
							needed_tags.append(k)
							if k.startswith("gramm"):
								gi += 1
								if k.split("=")[1] not in freq_grammar_tags:
									freq_grammar_tags[k.split("=")[1]] = 1
								else:
									freq_grammar_tags[k.split("=")[1]] += 1
					#f_new.write(time + " " + "&".join(needed_tags))
					#f_new.write("\n")
					if gi > 1:
						gramms += 1
					if gi == 1:
						onegramms += 1

				except:
					continue
				f_new.write("\n")

def sort_frequency_dict(dictionary, method): ## function of sorting and printing frequency list, which can be printed in console or in file
	if method == "print out":
		for case in sorted(dictionary, key=dictionary.get, reverse=True):
			print (case, dictionary[case])
	if method == "in file":
		dict_file = codecs.open("frequency_list.txt", "w", encoding = "utf-8")
		for case in sorted(dictionary, key=dictionary.get, reverse=True):
			dict_file.write(case + str(dictionary[case]))
	else:
		return False
	return True

decoder(".") ## decode all files with logs in this folder
clear_tags_from_queries(".") ## collect all logs from all days into one file, at the same time clearing out unneeded tags

common_file_with_queries = codecs.open("common_ncrl_queries.log", encoding = "utf-8").read() ## open common file with Russian logs
morph_dict = create_morph_frequency_list(russian_logs) ## create frequency dictionary of morphological query patterns

sort_frequency_dict(morph_dict, "print out") ## print sorted frequency list of morphological patterns in console
sort_frequency_dict(morph_dict, "in file") ## print sorted frequency list of morphological patterns in file "frequency_list.txt"
