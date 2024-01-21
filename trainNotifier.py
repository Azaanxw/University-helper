# Imports
import requests
from bs4 import BeautifulSoup

class RailInfoScraperApp:
    def __init__(self):
        pass
    def retrieve_rail_info(self):  # Gets the rail information from the given url website
        url = "https://www.nationalrail.co.uk/travel-information/industrial-action/"
        response = requests.get(url)

        if response.status_code == 200:
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Target classes and div to be extracted from
            target_class = "styled__StyledFreeFormRichTextWrapper-sc-qxvy7x-0 hSXtqU"
            target_div = soup.find("div", class_=target_class)

            result = []
            current_heading = None

            # Loops through the children of the target div
            for element in target_div.children:
                if element.name == 'p' and element.find("strong"): 
                    # If there's an element that is a paragraph and with a strong tag then strip the contents
                    current_heading = element.text.strip()
                elif element.name == 'ul' and current_heading:
                    # If there's an element that is an unordered list and there's a current heading then extract the list items
                    result.append(f"{current_heading}\n")
                    for li in element.find_all("li"): # Loops through the list and adds it to the results
                        result.append(f"{li.text.strip()}\n")
                    result.append("\n")
                    current_heading = None
            
            formatted_result = "".join(result)
            return formatted_result
        else:
            error_message = f"Failed to retrieve content. Status code: {response.status_code}"
            return error_message
