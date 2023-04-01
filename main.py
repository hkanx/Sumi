import openai
import requests
from bs4 import BeautifulSoup
from chatgpt_wrapper import ChatGPT
import csv
import re

# Gameplan: 
#   -   With a given URL, scrape all the text on the webpage.
# 	⁃	chunk up the text on the website 
# 	⁃	Feed chunked up texts to chatpgpt to    
#           1) check whether its what you’re looking for 
#                - Ask chatGPT if the words found talks about at Least 35% Reduction in Spleen Volume From Baseline at Week 24
#           2) and get the results you want
#               - If so, then ask chatGPT the different treatment options and the number of patients per treatment
# 	⁃	If not, go to the next keyword occurrence 


# Make an HTTP request to the webpage
url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

#print(response.content)

# Find all the text elements on the webpage
text_elements = soup.find_all(string=True)

# Combine the text elements into a single string
text = ' '.join(text_elements)

# Define the regex pattern to match section titles
pattern = r'^\s*(Chapter|Section|Part|Chapter \d+|Section \d+|Part \d+|[A-Z][A-Za-z\s&]*)\s*$'

# Split the text into sections based on the section titles
sections = {}
current_title = None
for line in text.splitlines():
    match = re.match(pattern, line)
    if match:
        current_title = match.group(0).strip()
        sections[current_title] = []
    elif current_title is not None:
        sections[current_title].append(line.strip())
        
print(sections)

# Convert the sections dictionary to a string with section titles and content
result = ''
for title, content in sections.items():
    result += title + '\n'
    result += '\n'.join(content) + '\n\n'

print(result)


