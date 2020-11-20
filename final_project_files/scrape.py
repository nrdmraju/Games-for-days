# import dependencies
import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
import requests
from bs4 import BeautifulSoup as BS
import time
import sys 

# get the file to run
file = sys.argv[1]
df = pd.read_csv(file)

# create a summaries column in the dataframe
df['Summary'] = ''

# set up webdriver
# options = Options()
# options.headless = True
# driver = webdriver.Firefox(options=options)

# create a log file for errors
log = open(f'scrape_errors_{file.replace(".csv","")}.log', 'a')

# perform scrape

for index, row in df.iterrows():
    time.sleep(10)
    
    url=row['url']
#     print(url)
    game=row['Name']

    try:    
        # driver.get(url)      
        # body = driver.find_element_by_tag_name("body")
        # body_html = body.get_attribute("innerHTML")
        # soup = BS(body_html)

        s = requests.Session()
        r = s.get(url).content
        soup = BS(r)
        
        try:
            # url_summary = soup.find('',{'id':'gameBody'}).text
            url_summary = soup.find('',{'id':'gameBody'}).get_text()
            print(f'successfully retrieved row summary for {game} at row {index}')
        except:
            print(f'summary retrieval failed for {game} at row {index}')
            log.writerow(f'summary retrieval failed for {game}')
    
    except:
        print(f'driver could not pull the {game} from {url}')
        log.writelines(f'driver could not pull the {game} from {url}')
    df.at[index, "Summary"] = url_summary

# driver.quit()

# write the dataframe to an output csv
df.to_csv(f'../clean_csv_files/{file}', index=False)

