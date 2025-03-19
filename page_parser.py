import requests
from datetime import datetime
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
            
            valid_from = self.get_valid_from(root)
            valid_to = self.get_valid_to(root)
            
            # description element
            desc = self.get_element(root, "div", "letak-description")
                
            thumbnail = self.get_thumbnail(desc)
            title = self.get_title(desc)
            name = self.get_shop_name(desc)
            parsed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
            print(f'Title: {title}')
            print(f'Thumbnail: {thumbnail}')
            print(f'Shop name: {name}')
            print(f'Valid from: {valid_from}')
            print(f'Valid to: {valid_to}')
            print(f'Parsed time: {parsed_time}')
            
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
            
    def get_valid_from(self, parent):
        try:
            target = parent.find("small", class_="hidden-sm").get_text()
            valid_from = target.split(" - ")[0]  # extract first date
            return self.format_date(valid_from)
        except Exception as e:
            print(f"Error in get_valid_from(): {e}")
            return None

    def get_valid_to(self, parent):
        try:
            target = parent.find("small", class_="hidden-sm").get_text()
            valid_to = target.split(" - ")[1]  # extract second date
            return self.format_date(valid_to)
        except Exception as e:
            print(f"Error in get_valid_to(): {e}")
            return None

    def format_date(self, date_str):
        """Convert 'DD.MM.YYYY' to 'YYYY-MM-DD' """
        try:
            return datetime.strptime(date_str, "%d.%m.%Y").strftime("%Y-%m-%d")
        except ValueError as e:
            print(f"Error in format_date(): {e}")
            return None
        
    