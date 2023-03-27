import openai
import requests
from bs4 import BeautifulSoup

# Set your OpenAI API key
openai.api_key = "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"

# Define a function to scrape the HTML content of a webpage and search for a keyword phrase
def search_webpage_for_phrase(url, phrase):
    # Use requests to get the HTML content of the webpage
    response = requests.get(url)
    html_content = response.content

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Search for the keyword phrase in the text content of the page
    text_content = soup.get_text()
    if phrase in text_content:
        # If the phrase is found, use ChatGPT to generate a response
        prompt = f"What was the total number of patients analyzed for the different outcomes?"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    else:
        return f"The phrase '{phrase}' was not found on {url}"

# Call the search_webpage_for_phrase function with the URL and keyword phrase you want to search for
url = "https://clinicaltrials.gov/ct2/show/results/NCT00934544?recrs=e&rslt=With&type=Intr&cond=Myelofibrosis&phase=2&draw=2&rank=1"
phrase = "spleen volume"
result = search_webpage_for_phrase(url, phrase)
print(result)
