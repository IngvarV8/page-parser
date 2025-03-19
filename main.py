from page_parser import PageParser

parser = PageParser("https://www.prospektmaschine.de/hypermarkte/")

print(parser.get_url())

parser.get_list()