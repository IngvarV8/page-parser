from page_parser import PageParser

parser = PageParser("https://www.prospektmaschine.de/hypermarkte/")

print(f'Parser set URL: {parser.get_url()}')

json_list = parser.get_json_list()

with open("output.json", "w", encoding="utf-8") as f:
    f.write(json_list)

#print(json_list)