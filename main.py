import openai
import requests
from bs4 import BeautifulSoup
from chatgpt_wrapper import ChatGPT
import csv

# Set your OpenAI API key (different for each chatGPT account)
openai.api_key = "ENTER-API"

# Define a function to search for the total number of patients analyzed at week 24
def search_for_week24_patients(url):
    # Use requests to get the HTML content of the webpage
    response = requests.get(url)
    html_content = response.content
    #print(html_content)

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
    fieldnames = ["url", "num_patients_week24", "num_patients_Ruxolitinib", "num_patients_Pacritinib", "num_patients_Fedratinib"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in data_list:
        writer.writerow(data)


# Integrate chatGPT with features
# bot = ChatGPT()

# response = bot.ask("what is the number of participants with at least 35 percent reduction in spleen volume from baseline at week 24 for each treatment type mentioned?")
# print(response)


