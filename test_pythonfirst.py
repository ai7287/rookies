import re

text = "abc def"
pattern = re.compile(r'a.')

match = pattern.search(text)
if match:
    print(match.group())  # 'ab' 출력
else:
    print("No match found")