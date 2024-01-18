import requests
from bs4 import BeautifulSoup

class RailInfoScraperApp:
    def __init__(self):
        pass
    def retrieve_rail_info(self):
        url = "https://www.nationalrail.co.uk/travel-information/industrial-action/"
        response = requests.get(url)

        if response.status_code == 200:
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')

            target_class = "styled__StyledFreeFormRichTextWrapper-sc-qxvy7x-0 hSXtqU"
            target_div = soup.find("div", class_=target_class)

            result = []
            current_heading = None

            for element in target_div.children:
                if element.name == 'p' and element.find("strong"):
                    current_heading = element.text.strip()
                elif element.name == 'ul' and current_heading:
                    result.append(f"{current_heading}\n")
                    for li in element.find_all("li"):
                        result.append(f"{li.text.strip()}\n")
                    result.append("\n")
                    current_heading = None

            formatted_result = "".join(result)
            return formatted_result
        else:
            error_message = f"Failed to retrieve content. Status code: {response.status_code}"
            return error_message
