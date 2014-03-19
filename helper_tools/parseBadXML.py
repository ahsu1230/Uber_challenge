#!/usr/bin/python
# Given a XML file, replace 'bad' XML traits
# 	i.e. XML file came with hyperlinks on separate lines, remove them
#		replace '&' with '&amp;'

old_file = open("trucks.xml", "r")
new_file = open("trucks_.xml", "w")

flagHeader = True
for line in old_file:
	if line.find("http:") == 0:
		continue # remove hyperlinks that are their own contents!
	newline = line.replace("&", "&amp;")
	new_file.write(newline)
	
new_file.close()
old_file.close()