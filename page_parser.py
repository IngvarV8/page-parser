import requests
from bs4 import BeautifulSoup

class PageParser:
    def __init__(self, url):
        self._url = url
        self._html = None
        self.set_html()
        
    def get_url(self):
        return self._url
    
    def get_html(self):
        return self._html
    
    def set_html(self):
        try:
            req = requests.get(self.get_url())
            self._html = req.text
        except Exception as e:
            print(f"Error fetching HTML content: {e}")
            self._html = None
    
    def get_logo(self):
        pass
    
    def get_element(self, element, class_name):
        soup = BeautifulSoup(self.get_html(), "html.parser")

        try:
            target_div = soup.find(element, class_=class_name)
            return target_div
        except Exception as e:
            print(f"Error finding HTML element {element} with classname {class_name}: {e}")
        
    