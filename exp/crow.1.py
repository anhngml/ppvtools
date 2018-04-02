import requests
from bs4 import BeautifulSoup
import re

page = requests.get("https://www.google.com/search?q=0978000831+email")
html = page.content

soup = BeautifulSoup(html, "html.parser")
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()
# print(text)

# match = re.findall(r'[\w\.-]+@[\w\.-]+[^\u0000-\u007F]+', text)

# match = re.findall(r'/[A-Z0-9._%+-]+@[A-Z0-9-]+.+.[A-Z]{2,4}/igm', text)

match = re.findall(
    r'[\w\.-]+@[\w\.-]+com|[\w\.-]+@[\w\.-]+net|[\w\.-]+@[\w\.-]+vn', text)

print(match)
