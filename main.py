import openai
import requests
from bs4 import BeautifulSoup
from chatgpt_wrapper import ChatGPT
import csv

# # Integrate chatGPT with features
# bot = ChatGPT()

# response = bot.ask("in what section does the word?")
# print(response)

# Make a GET request to the webpage you want to search
url = "https://clinicaltrials.gov/ct2/show/results/NCT00934544?rslt=With&type=Intr&cond=Myelofibrosis&phase=2&draw=2&rank=1 "
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all occurrences of a keyword in the webpage
keyword = "safety"
elements = soup.find_all(string=lambda text: text and keyword in text)

if elements:
    # Output the locations of all keyword occurrences to the console
    for element in elements:
        location = element.parent
        print(location)

    # Write the locations of all keyword occurrences to a file
    with open("keyword_locations.txt", "w") as f:
        f.write(f"Found {len(elements)} occurrences of keyword '{keyword}' on the webpage:\n")
        for i, element in enumerate(elements):
            
            location = element.parent
            f.write(f"Keyword occurrence {i+1} found in element: {location}\n")
            f.write("="*80 + "\n")
else:
    print(f"Could not find keyword '{keyword}' on the webpage")
