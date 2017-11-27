## This is script for parsing logs from corpus of Leeds. Also you can use it to create frequency list of different search patterns.

import codecs
import re

def collect_russian_logs(file):
	logs = file.read().split("ended: ") ## each log starts with "ended: ", so it's rational to split logs by this word
	
	russian_corpora = ["RNC2010-MOCKY", "NEWS-RU", "I-RU", "BIZ-RU", "WIKI-RU", "RU-AC", "BMR-RU", "LJ-RU", "MAGZ-RU", "RUWAC"]
	needed_logs = []

	for i in logs:
	if any(title in i for title in russian_corpora):
		needed_logs.append(i)

	f_new = codecs.open("russian_logs.txt", "w", encoding = "utf-8")
	for each in needed_logs:
		f_new.write(each + "\n")

	return True

def create_morph_frequency_list(file): ## function of creating frequency list of morphological query patterns
	logs = file.read().split("\n")
	freq_list_pos = {}
	pos_pattern = re.compile("pos=.+?\]")

	for i in logs:
	pos = re.findall(pos_pattern, i)
	for each in pos:
		if each not in freq_list_pos:
			freq_list_pos[each] = 1
		else:
			freq_list_pos[each] += 1

	return freq_list_pos

def create_word_frequency_list(file): ## function of creating frequency list of word query patterns
	logs = file.read().split("\n")
	freq_list_word = {}
	word_pattern = re.compile("\[word=.+?\]")

	for i in logs:
	word = re.findall(word_pattern, i)
	for each in word:
		if each not in freq_list_word:
			freq_list_word[each] = 1
		else:
			freq_list_word[each] += 1

	return freq_list_word
	
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

f = codecs.open("queries.log", encoding = "utf-8") ## open common file with logs
collect_russian_logs(f) ## create single file with all query logs in Russian language

russian_logs = codecs.open("russian_logs.txt", encoding = "utf-8") ## open common file with Russian logs
morph_dict = create_morph_frequency_list(russian_logs) ## create frequency dictionary of morphological query patterns
word_dict = create_word_frequency_list(russian_logs) ## create frequency dictionary of lexical query patterns

sort_frequency_dict(morph_dict, "print out") ## print sorted frequency list of morphological patterns in console
sort_frequency_dict(morph_dict, "in file") ## print sorted frequency list of morphological patterns in file "frequency_list.txt"
