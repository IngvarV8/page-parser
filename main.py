from page_parser import PageParser

parser = PageParser("https://www.prospektmaschine.de/hypermarkte/")

print(f'Parser set URL: {parser.get_url()}')

json_list = parser.get_json_list()

try:
    with open("output.json", "w", encoding="utf-8") as f:
        f.write(json_list)
except Exception as e:
    print(f"Error writing to file: {e}")
    print("Printing to stdout...")
    print(json_list)