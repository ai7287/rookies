from bs4 import BeautifulSoup

html_doc = """
<html>
<head>
    <title>The Dormouse's story</title>
</head>
<body>
    <div data-role="page" data-last-modified="2022-01-01" data-foo="value">This is a div with data attributes.</div>
    <p class="title"><b>The Dormouse's story</b></p>
    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie" class="sister" id="link2" data-info="more info">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3" data-info="even more info">Tillie abcd</a>
    ; and they lived at the bottom of a well.</p>
    <p class="story">...</p>
</body>
</html>
"""

soup = BeautifulSoup(html_doc, 'html.parser')

for link in soup.find_all('a'):
    print(link.string)
    print(link.get('href'))