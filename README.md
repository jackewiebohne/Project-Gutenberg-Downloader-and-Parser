# Project-Gutenberg-Downloader-and-Parser
There is a Project Gutenberg downloader (at current settings it downloads all German texts; I've indicated where to change this in the code if, say, English or French texts were desired) and a Project Gutenberg file parser (which assumes that you've unzipped all the PG txt files into a single folder). The parser will iterate over PG txt files and filter out author and translator name, title of the text, and the text's geodata (in a very similar manner as my DTA parser).
