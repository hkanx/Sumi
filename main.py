import requests
from bs4 import BeautifulSoup
# from chatgpt_wrapper import ChatGPT

# bot = ChatGPT()
# # return the full result. This is much slower
# response = bot.ask("tell me a story about cats and dogs")
# print(response)

# Set the URL of the webpage to scrape
url = 'https://clinicaltrials.gov/ct2/show/results/NCT00934544?recrs=e&rslt=With&type=Intr&cond=Myelofibrosis&phase=2&draw=2&rank=1'

# Set the keyword phrase to search for
keyword = 'spleen volume'

# Make a request to the webpage and get the HTML content
response = requests.get(url)
html_content = response.text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all the text on the webpage and check if the keyword phrase is present
found_keyword = False
for text in soup.stripped_strings:
    if keyword in text:
        found_keyword = True
        break

# Print the result
if found_keyword:
    print(f'The keyword "{keyword}" was found on the webpage.')
else:
    print(f'The keyword "{keyword}" was not found on the webpage.')
