from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a target="_blank" href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a target="_blank" href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a target="_blank" href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'html.parser')

# print(soup.prettify())

links = soup.find_all('a')
# for link in links:
    # print(link.get('href'))
    # print(link.get_text())

paragraphs = soup.find_all('p')
# for paragraph in paragraphs:
    # print(paragraph.get_text())
    # print(paragraph.name)
    # print(paragraph.attrs)
    # print(paragraph.next_sibling)
    # print(paragraph.parent)


from bs4 import BeautifulSoup
soup = BeautifulSoup(open("top_100_ebooks.html"), features="html.parser")

# print(soup.prettify())

# titles = soup.find_all('li')
# for title in titles:
    # print(title.get_text())


from bs4 import BeautifulSoup
import requests

response = requests.get("https://www.gutenberg.org/browse/scores/top")
print("Status code:", response.status_code)
print("Headers:", response.headers)