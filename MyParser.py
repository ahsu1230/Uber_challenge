#!/usr/bin/python
"""
	ASSUMPTIONS:
	all hyperlinks are removed
	all '&' are replaced with '&amp;'
		run parseHyperlinks.py on specified xml file to replace '&' and remove hyperlinks
"""
import re
import xml.dom.minidom

# Extracts text in the specified xml minidom
def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

# Given a list of elements (within a tag), parse out text for that first element instance
def handleElement(xList):
	if len(xList) == 0:
		return ""
	txt = str(getText(xList[0].childNodes))
	txt = txt.lstrip('\n\t')
	return txt
	
class XMLParser:
	PARSE_FAIL = "error: PARSING FAIL!"
	# Constructor for XML Parser
	def __init__(self, filepath):
		self.fileobj = open(filepath, 'r')
		self.document = self.fileobj.read()
		self.dom = xml.dom.minidom.parseString(str(self.document))
		self.tagList = []
		return
	
	"""	@func HandleDocument - For a specific tag in a XML document, for each tag instance, parse out specified elements
		- @Parameters: tag and target attribute list (all strings)
		- @ReturnValue: List of elements in tag (len(List) == # of tag instances)
	"""
	def HandleDocument(self, tag, elements):
		tags = self.dom.getElementsByTagName(tag)
		for t in tags:
			tagData = []
			for ele in elements:
				entry = handleElement(t.getElementsByTagName(str(ele)))
				tagData.append(entry)
			if len(tagData) == len(elements):
				self.tagList.append(tagData)
			else:
				# error! tagData is not correct!
				return PARSE_FAIL
		return self.tagList
	
	"""	@func PrintToTxt - Writes out tagList to a new file, for debugging purposes
		- @Parameters:
		- @ReturnValue:
	"""
	def PrintToTxt(self):
		fileobj = open("parsed_xml.txt", 'w')
		for t in self.tagList:
			fileobj.write(t)