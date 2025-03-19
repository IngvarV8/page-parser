from page_parser import PageParser

parser = PageParser("https://www.prospektmaschine.de/hypermarkte/")

print(f'Parser set URL: {parser.get_url()}')

print(parser.get_json_list())