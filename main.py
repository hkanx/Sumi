import csv
import openai
import requests
from bs4 import BeautifulSoup

# Set your OpenAI API key
openai.api_key = "ENTER-API"

# Define a function to scrape the HTML content of a webpage and search for the total number of patients analyzed at week 24
def search_for_week24_patients(url):
    # Use requests to get the HTML content of the webpage
    response = requests.get(url)
    html_content = response.content

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Search for the "Spleen response assessment" table in the HTML content
    table = soup.find("table", {"id": "results_spleen"})
    if table:
        # If the table is found, search for the "Week 24" row in the table
        rows = table.find_all("tr")
        for row in rows:
            columns = row.find_all("th")
            if columns and "Time Frame" in columns[0].get_text().strip() and "Week 24" in row.get_text().strip():
                week24_row = row
                break

        # If the "Week 24" row is found, search for the "Number of patients analyzed" cell in the row
        cells = week24_row.find_all("td")
        for cell in cells:
            if "Number of patients analyzed" in cell.get_text().strip():
                num_patients_analyzed = cell.find_next_sibling().get_text().strip()
                # If the "Number of patients analyzed" cell is found, use ChatGPT to generate a response
                prompt = f"Can you tell me more about spleen reduction on {url}? How many patients were analyzed at week 24?"
                response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=prompt,
                    max_tokens=1024,
                    n=1,
                    stop=None,
                    temperature=0.7
                )
                return response.choices[0].text.strip()
        return f"No 'Number of patients analyzed' cell was found in the 'Week 24' row on {url}"
    else:
        return f"No spleen response assessment was found on {url}"

# Call the search_for_week24_patients function with the URL you want to search
url = "https://clinicaltrials.gov/ct2/show/results/NCT00934544?recrs=e&rslt=With&type=Intr&cond=Myelofibrosis&phase=2&draw=2&rank=1"
result = search_for_week24_patients(url)

# Save the result to a CSV file
with open('results.csv', mode='w') as results_file:
    writer = csv.writer(results_file)
    writer.writerow(['URL', 'Result'])
    writer.writerow([url, result])

print(result)
