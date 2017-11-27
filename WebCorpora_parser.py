import codecs

log_filename = input("Input name of the logfile: ")
clear_logs = input("Input name for the logfile with onlny needed tags: ")
stat_filename = input("Input name for the file with statistics: ")

f = codecs.open(log_filename)

requests = f.read().split("\n")

f_new = codecs.open(clear_logs, "w")

freq_grammar_tags = {}

for i in requests:
	try:
		tags = i.split(",")[10].split("&")
		for k in tags:
			if k.endswith("="):
				tags.remove(k)
		needed_tags = []
		for k in tags:
			if any(k.startswith(tag) for tag in ["full", "gr", "lex", "use"]) and not k.endswith("="):
				needed_tags.append(k)
				if k.startswith("gr"):
					if k.split("=")[1] not in freq_grammar_tags:
						freq_grammar_tags[k.split("=")[1]] = 1
					else:
						freq_grammar_tags[k.split("=")[1]] += 1
		f_new.write(i.split(",")[9] + ", " + "&".join(needed_tags))
		f_new.write("\n")
	except:
		print (i)

f_dict = codecs.open(stat_filename, "w")
for case in sorted(freq_grammar_tags, key=freq_grammar_tags.get, reverse=True):
        f_dict.write(case + " - " + str(freq_grammar_tags[case]) + "\n")
