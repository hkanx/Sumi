This is a project utilizing NLP and GPT to streamline the process of analyzing medical data. 

**Resolved Challenges:**
Spanning different code commits, resolved challenges include scrapping the majority of the text from the webpage (utilizing APIs and Beautiful Soup), documenting the locations of keyword phrase locations to a readable CSV file, integrating a NLP like chatGPT.

It was determined that several webpages in a given pool of data regarding a disease/ sickness may not pertain exactly to the data being searched for. For instance, even if a webpage is about the correct consequences of a treatment, if the recorded timeframe isn’t what we are looking for, the webpage data may be rendered unusable for our purposes.

It was also determined that the number of treatments vary for each webpage, which changes how the keyword phrase should be utilized to search on a page. Some studies have three treatments, while some have just one treatment. In particular, the key phrases for webpages with just 1 treatment being analyzed should be less restricting since the factors that make up the success of a treatment may already be implied in a previous or different section from where the outcomes are recorded. 

**Current Challenges:**
There are currently quite a few challenges being tackled. 

One of them is successfully web scraping the entire text from a webpage URL, due to different formatting. Some approaches being explored at the moment include HTML processing to find the different titles and subtitles of sections within the document, using regular expressions (Regex). 

Another major challenge is successfully locating the sections that pertain to the specified task. 
The approach I attempted initially was to utilize a natural language processor (chatGPT) to locate where several keyword phrases (ex. “Week 24”, “Spleen Reduction”) occur and to write down all the locations of occurrences to a file. From the obtained locations, web scrape the previous 50 words and post 50 words of the keyword phrase using a HTML parser (Beautiful Soup) and by utilizing the API of Clinical Trials Gov (https://clinicaltrials.gov/api/gui). I realized that this approach is difficult to standardize especially with the various formats of the webpage and the inconsistency of keywords. Some key phrases are in terms of days instead of weeks, some use three treatments while some only use one, some don’t even specify which week it is in (specified in terms of years), which makes me believe that I should not even use the webpage as part of the dataset. As I did this, some of the search words I ended up using the most were: spleen volume, spleen length, reduction, baseline, week 24, and 24 weeks. 

The next approach that I am trying out at the moment is to:
1. First scrape all the text from a webpage
2. Chunk up the text on the website
3. Feed chunked up texts to chatGPT to    
				1) check whether its what you’re looking for    
				2) and get the results you want
4. If so, then ask chatGPT the different treatment options and the number of patients per treatment
5. If not, go to the next keyword occurrence 

I decided to first attempt to scrape all the text by using Regex, and I am currently working on how to parse information such that the chunked up data sections would be most intuitive for later tasks. I am thinking that I will focus on the Primary Outcome and Secondary Outcomes sections on the webpages because the data is most commonly located in these two large sections. 

