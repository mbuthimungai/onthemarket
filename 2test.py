import asyncio
from tools.tools import Response
from bs4 import BeautifulSoup
import re


response = Response()

async def main():
    content = await response.fetch("https://www.onthemarket.com/for-sale/property/london/?max-price=90000&recently-reduced=true")
    with open('filelddld.txt', 'w', encoding='utf-8') as file:
        file.write(str(content))
    soup = BeautifulSoup(content, 'html.parser')
    total_properties_element = soup.find('span', class_='lg:mr-4 font-bold')
    print("total_properties_element", total_properties_element)
    if total_properties_element:
        text = total_properties_element.get_text()
        text = total_properties_element.get_text().lower()
        text = int(text.replace("results", "").replace("+", ""))            
        print(type(text))
asyncio.run(main())