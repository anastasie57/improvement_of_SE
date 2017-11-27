## This is script for parsing logs from General Internet Corpus of Russian Language. Also you can use it to create frequency list of different search patterns.

import codecs

f = codecs.open("logs_final.txt")

strings = f.read().split("\n")
needed = []

for i in range(len(strings)):
	if strings[i].startswith(" ["):
		needed.append([strings[i], strings[i+1]])

f_new = codecs.open("new_file.txt", "w")

for i in needed:
	f_new.write(i[0])
	f_new.write("\n")
	f_new.write(i[1])
	f_new.write("\n\n")
