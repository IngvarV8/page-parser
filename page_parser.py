import requests
from bs4 import BeautifulSoup

class PageParser:
    def __init__(self, url):
        self._url = url
        self._html = None  #contents of the whole page
        self.set_html()
        self._target_class = "letak-description"
        
    def get_list(self):
        soup = BeautifulSoup(self.get_html(), "html.parser")
        
        for root in soup.find_all("div", "brochure-thumb"): # list of parent objects of each leaflet (root)
            letak_date = self.get_date(root)
            
            # description element
            desc = self.get_element(root, "div", "letak-description")
                
            thumbnail = self.get_thumbnail(desc)
            title = self.get_title(desc)
            name = self.get_shop_name(desc)
                
            print(f'Title: {title}')
            print(f'Thumbnail: {thumbnail}')
            print(f'Shop name: {name}')
            print(f'Letak date: {letak_date}')
            
            
            print(" ")
        
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
    
    def get_element(self, parent, element, class_name=None):
        try:
            target = parent.find(element, class_=class_name)
            return target
        except Exception as e:
            print(f"Error finding HTML element {element} with classname {class_name}: {e}")
            
    def get_elements(self, parent, element, class_name):
        try:
            targets = parent.find_all(element, class_=class_name)
            return targets
        except Exception as e:
            print(f"Error finding HTML element {element} with classname {class_name}: {e}")
            
    def get_img_source(self, parent):
        try:
            targets = parent.find("img", attrs={"class": "lazyloadLogo"})
            return targets
        except Exception as e:
            print(f"Error: {e}")
    
    def get_title(self, parent):
        try:
            target = parent.find("strong").get_text()
            return target
        except Exception as e:
            print(f"Error in get_title: {e}")
            
    def get_shop_name(self, parent):
        try:
            target = parent.find("img").get("alt")
            return target
        except Exception as e:
            print(f"Error in get_shop_name(): {e}")
            
    def get_thumbnail(self, parent):
        try:
            target = parent.find("img").get("data-src")
            return target
        except Exception as e:
            print(f"Error in get_shop_name(): {e}")
            
    def get_date(self, parent):
        try:
            target = parent.find("small", "hidden-sm").get_text()
            return target
        except Exception as e:
            print(f"Error in get_date(): {e}")
        
        
    