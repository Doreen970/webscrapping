from bs4 import BeautifulSoup
import requests
import pandas as pd

html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=as&searchTextText=Python&txtKeywords=Python&txtLocation=').text
soup = BeautifulSoup(html_text, 'lxml')
jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
#dictionary to show count of each unique location
location_count = {}

for job in jobs:
    published_date = job.find('span', class_='sim-posted').span.text
    if 'few' or 'today' in published_date:
        company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ','')
        skills = job.find('span', class_='srp-skills').text.replace(' ','')
        location = job.find('span')['title']
        # increment occurrence of each unique location
        location_count[location] = location_count.get(location, 0) + 1
        more_info = job.find('h2').a['href']
        # create a dataframe from the dictionary
        df = pd.DataFrame(list(location_count.items()), columns=['Location', 'Job Count'])
        # sort dataframe by job count
        df_sorted = df.sort_values(by='Job Count', ascending=False)
    

        print(f'Company name: {company_name.strip()}')
        print(f'skills: {skills.strip()}')
        print(f'location: {location.strip()}')
        print(f'More info: {more_info}')

        print()
        print(df_sorted)