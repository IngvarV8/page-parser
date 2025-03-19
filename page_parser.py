import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

class PageParser:
    def __init__(self, url):
        self._url = url
        self._html = self._fetch_html()
        
    def get_json_list(self):
        soup = BeautifulSoup(self.get_html(), "html.parser")
        data_list = []
        
        for root in soup.find_all("div", "brochure-thumb"): # list of parent objects of each leaflet (root)
            data_list.append(self._extract_leaflet_data(root))
        
        return self._to_json(data_list)
        
    def get_url(self):
        return self._url
    
    def get_html(self):
        return self._html
    
    def _fetch_html(self):
        try:
            res = requests.get(self.get_url())
            return res.text
        except Exception as e:
            print(f"Error fetching HTML content: {e}")
            return None
    
    def _get_element(self, parent, element, class_name=None):
        try:
            target = parent.find(element, class_=class_name)
            return target
        except Exception as e:
            print(f"Error finding HTML element {element} with classname {class_name}: {e}")
            return None
            
    """
    def get_elements(self, parent, element, class_name):
        try:
            targets = parent.find_all(element, class_=class_name)
            return targets
        except Exception as e:
            print(f"Error finding HTML element {element} with classname {class_name}: {e}")      
    """
    
    def _get_text(self, parent, tag):
        # extract text from given tag
        try:
            return parent.find(tag).get_text() if parent else None
        except Exception as e:
            print(f"Error extracting text from <{tag}>: {e}")
            return None
    
    def _get_title(self, parent):
        try:
            target = parent.find("strong").get_text()
            return target
        except Exception as e:
            print(f"Error in get_title: {e}")
            return None
            
    def _get_shop_name(self, parent):
        try:
            target = parent.find("img").get("alt")
            return target
        except Exception as e:
            print(f"Error in get_shop_name(): {e}")
            return None
            
    def _get_image_attr(self, parent, attr):
        try:
            img = parent.find("img")
            return img.get(attr) if img else None
        except Exception as e:
            print(f"Error extracting '{attr}' from <img>: {e}")
            return None
            
    def _get_validity_text(self, parent):
        element = parent.find("small", class_="hidden-sm")
        return element.get_text() if element else None

    def _get_valid_from(self, parent):
        try:
            date_range = self._get_validity_text(parent)
            return self._format_date(date_range.split(" - ")[0]) if date_range else None
        except Exception as e:
            print(f"Error in _get_valid_from(): {e}")
            return None

    def _get_valid_to(self, parent):
        try:
            date_range = self._get_validity_text(parent)
            return self._format_date(date_range.split(" - ")[1]) if date_range else None
        except Exception as e:
            print(f"Error in _get_valid_to(): {e}")
            return None

    def _format_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%d.%m.%Y").strftime("%Y-%m-%d")
        except ValueError as e:
            print(f"Error in _format_date(): {e}")
            return None
        
    def _extract_leaflet_data(self, root):
        desc = self._get_element(root, "div", "letak-description")

        return {
            "title": self._get_text(desc, "strong"),
            "thumbnail": self._get_image_attr(desc, "data-src"),
            "shop_name": self._get_image_attr(desc, "alt"),
            "valid_from": self._get_valid_from(root),
            "valid_to": self._get_valid_to(root),
            "parsed_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _to_json(self, data):
        return json.dumps(data, indent=4, ensure_ascii=False)