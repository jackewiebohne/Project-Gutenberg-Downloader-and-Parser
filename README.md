# Project-Gutenberg-Downloader-and-Parser
There is a Project Gutenberg downloader (at current settings it downloads all German texts; I've indicated where to change this in the code if, say, English or French texts were desired) and a Project Gutenberg file parser (which assumes that you've unzipped all the PG txt files into a single folder). The parser will iterate over PG txt files and filter out author and translator name, title of the text, and the text's geodata (in a very similar manner as my DTA parser). 
After parsing, if you wish for geodata csv file to be filtered acc. to country-specific geodata, unique geodata, non-european geodata etc.

I should add that the geodata parser is a simple rule-based parser and outdated. You will obtain better results using SpaCy, esp. the transformer based trf version. It is available for a number of languages, see (for English): https://spacy.io/models/en 

# Please feel free to use under MIT License
