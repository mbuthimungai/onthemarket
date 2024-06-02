from bs4 import BeautifulSoup
import re
import json

from tools.tools import Response




class OnTheMarket:
    def __init__(self) -> None:
        pass
    
    async def extract_total_number_properties(self, url: str) -> int:
        response = Response()
        content = await response.fetch(url=url)
        
        soup = BeautifulSoup(content, 'html.parser')
        total_properties_element = soup.find('span', class_='lg:mr-4 font-bold')
        if total_properties_element:
            text = total_properties_element.get_text().lower()
            text = int(text.replace("results", "").replace("+", ""))            
            return text
        return None
    
    async def extract_contact_form_links(self, url: str) -> list:
        response = Response()
        content = await response.fetch(url=url)
        
        request_viewing_links = []
        
        soup = BeautifulSoup(content, 'html.parser')
        
        properties_listings_li = soup.find_all('li', class_='otm-PropertyCard')
        if properties_listings_li:
            for property_listing_li in properties_listings_li:
                title_span = property_listing_li.find('span', class_='title')                
                if title_span:
                    property_anchor_tag = title_span.find('a')
                    
                    if property_anchor_tag:                        
                        property_link = f"https://www.onthemarket.com{property_anchor_tag.get('href')}"
                        if property_link:
                            content_2 = await response.fetch(url=property_link)
                            soup_2 = BeautifulSoup(content_2, 'html.parser')
                            agent_info_div = soup_2.find('div', class_='agent-info-contact')
                            if agent_info_div:
                                request_viewing_tag = agent_info_div.find('a')
                                
                                if request_viewing_tag:
                                    request_viewing_link = f"https://www.onthemarket.com{request_viewing_tag.get('href')}"
                                    request_viewing_links.append(request_viewing_link)
        return request_viewing_links
    
    async def extract_user_agents(self, url: str) -> None:
        content = await Response().fetch(url=url)
        
        soup = BeautifulSoup(content, "html.parser")        
        
        # find div with user agents
        div_with_json_ua = soup.find('div', id='most-common-desktop-useragents-json-csv')
                
        # find the text area        
        textarea = div_with_json_ua.find('textarea', {'class': 'form-control'})
        
        if textarea:
            user_agents = json.loads(textarea.text)
            
            # This deletes content from the user agent.txt file
            with open("./user-agents.txt", "w") as file:
                pass
            with open("./user-agents.txt", "a") as file:
                for user_agent in user_agents:
                    file.write(f'{user_agent.get("ua")}\n')


