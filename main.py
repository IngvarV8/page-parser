from page_parser import PageParser

parser = PageParser("https://www.prospektmaschine.de/hypermarkte/")

print(parser.get_url())
print(parser.get_element("div", "letak-description"))