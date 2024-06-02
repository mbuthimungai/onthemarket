import re
from bs4 import BeautifulSoup

html_content = '<span class="lg:mr-4 font-bold">1,000+ results</span>'
soup = BeautifulSoup(html_content, 'html.parser')

# Find the span element with the specific class
span = soup.find('span', class_='lg:mr-4 font-bold')

if span:
    text = span.get_text()
    # Use regex to extract the number part
    match = re.search(r'(\d[\d,]*)\+', text)
    if match:
        number_str = match.group(1).replace(',', '')
        number = int(number_str)
        print(number)  # Output will be 1000
