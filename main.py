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

# IDEAL SAMPLE INPUTS AND OUTPUTS:
#   Sample input is the url "https://clinicaltrials.gov/ct2/show/results/NCT00934544?recrs=e&rslt=With&type=Intr&cond=Myelofibrosis&phase=2&draw=2&rank=1"
#   Sample output is 
#       Data (HTML) is scraped to a file        
#       Print out the location of where the keyword phrase is
#       Creates the CSV file: clinical_trial_data.csv that has all the information scraped (number of patients & participants of patients as numerical data)


# Set your OpenAI API key (different for each chatGPT account)
openai.api_key = "API-KEY"

# Define a function to search for the total number of patients analyzed at week 24
def search_for_week24_patients(url):
    # Use requests to get the HTML content of the webpage
    response = requests.get(url)
    # Check if the response object is valid
    if response.status_code == 200:
        # If the response is valid, parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
    else:
        # If the response is invalid, print an error message
        print(f"Error: {response.status_code}")
    html_content = response.content

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Search for the "Spleen response assessment" table in the HTML content
    table = soup.find("table", {"id": "Spleen Volume"}) #problem somewhere here? 
    if table:
        # If the table is found, search for the "Week 24" row in the table
        rows = table.find_all("tr")
        for row in rows:
            columns = row.find_all("th")
            if columns and "Week 24" in columns[0].get_text().strip():
                week24_row = row
                break

        # If the "Week 24" row is found, search for the "Number of patients analyzed" cell in the row
        cells = week24_row.find_all("td")
        for cell in cells:
            if "Number of patients analyzed" in cell.get_text().strip():
                num_patients_analyzed = cell.find_next_sibling().get_text().strip()

                # Search for the treatment options and number of patients per treatment option
                treatment_rows = table.find_all("tr", {"class": "ctdata"})
                treatments = {}
                for row in treatment_rows:
                    treatment_cols = row.find_all("td")
                    treatment = treatment_cols[0].get_text().strip()
                    num_patients = treatment_cols[2].get_text().strip()
                    treatments[treatment] = num_patients

                # If the "Number of patients analyzed" cell and treatment options are found, return the data as a dictionary
                return {"url": url, "num_patients_week24": num_patients_analyzed, **treatments}
        return f"No 'Number of patients analyzed' cell was found in the 'Week 24' row on {url}"
    else:
        return f"No spleen response assessment was found on {url}"

# Define a list of URLs to search
urls = [
    "https://clinicaltrials.gov/ct2/show/results/NCT00934544?recrs=e&rslt=With&type=Intr&cond=Myelofibrosis&phase=2&draw=2&rank=1",
    "https://clinicaltrials.gov/ct2/show/results/NCT00952289?recrs=e&rslt=With&type=Intr&cond=Myelofibrosis&phase=2&draw=2&rank=5"
]

# Create a list to hold the dictionaries for each URL
data_list = []

# Call the search_for_week24_patients function for each URL and append the resulting data to the data_list
for url in urls:
    data = search_for_week24_patients(url)
    if isinstance(data, str):
        print(data)
    else:
        data_list.append(data)

# Write the data from the data_list to a CSV file
with open("clinical_trial_data.csv", "w", newline="", encoding="utf-8") as csvfile:
    #fieldnames: is an example input (column titles)
    fieldnames = ["url", "num_patients_week24", "num_patients_Ruxolitinib", "num_patients_Pacritinib", "num_patients_Fedratinib"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in data_list:
        writer.writerow(data)


# Integrate chatGPT with features
bot = ChatGPT()

answer = bot.ask("In what section do the words spleen volume occur in? Scrape the data from the saved file.") #TO-DO: from the scraped HTML in the stored file. Change question to chunk data into sections. 

parser = BeautifulSoup(answer.content, 'html.parser') #TO-DO: Integrate with scraped data

# Find all the text elements on the webpage
text_elements = parser.find_all(string=True)

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

# Convert the sections dictionary to a string with section titles and content
result = ''
for title, content in sections.items():
    result += title + '\n'
    result += '\n'.join(content) + '\n\n'

#To-Do: return to a CSV file to make the final output. 

