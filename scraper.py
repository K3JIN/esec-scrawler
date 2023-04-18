import csv
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from telegram.ext import (Updater, ContextTypes, ConversationHandler, MessageHandler)
from esb import CURL, pass_link




#chrome is disabled due to unstable driver version issue.

# Welcome Banner of the script.

script_logo = '''
   ('-.     .-')       ('-.                    
 _(  OO)   ( OO ).   _(  OO)                
(,------. (_)---\_) (,------.    .-----.    
 |  .---' /    _ |   |  .---'   '  .--./    
 |  |     \  :` `.   |  |       |  |('-.    
(|  '--.   '..`''.) (|  '--.   /_) |OO  )   
 |  .--'  .-._)   \  |  .--'   ||  |`-'|    
 |  `---. \       /  |  `---. (_'  '--'\    
 `------'  `-----'   `------'    `-----'   Scrawler v 0.01
                                                  
'''
print(script_logo)
print('Scwaler will help you scrape and crawl inside a target website.\n\n')
time.sleep(1)
# Ask the user for the URL of the website
async def regular_choice(update: Updater, context: ContextTypes.DEFAULT_TYPE) -> str:
   CURL = update.message.text
   context.user_data["CURL"] = CURL
try:
  url = input(pass_link)
  is_url = True
except:
  is_url = False

if is_url:
  url = input('Enter the URL you wish to scrawl >> ')
else:
  url = input('try something else')




# Set up the browsers


options = webdriver.ChromeOptions()
options.add_argument("--headless")

#chrome_browser = webdriver.Chrome(options=options)
firefox_browser = webdriver.Firefox()

# GET request to the URL
#chrome_browser.get(url)
firefox_browser.get(url)
response = requests.get(url)



# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Check if the website is dynamic or static
try:
    #chrome_browser.find_element(By.XPATH,'xpath')
    firefox_browser.find_element(By.XPATH,'xpath')
    is_dynamic = True
except NoSuchElementException:
    is_dynamic = False

# Scrape data from every single page on the website
if is_dynamic:
    # Used Selenium to interact with the page and find all available of the links
    links = []
    #for link in chrome_browser.find_elements(By.TAG_NAME,'a'):
        #links.append(link.get_attribute('href'))
    for link in firefox_browser.find_elements(By.TAG_NAME,'a'):
        links.append(link.get_attribute('href'))    

    # Scrape data from each page using both browsers
    data = []
    for link in links:
        #chrome_browser.get(link)
        firefox_browser.get(link)
        time.sleep(1)

        # Find all of the data you want to scrape using the appropriate tags and classes
        # For example, to scrape all of the images on the page:
       # chrome_images = []
       # firefox_images = []
       # for img in chrome_browser.find_elements(By.CLASS_NAME,'nav nav-list'):
          #  chrome_browser.append(img.get_attribute('src'))
       # for img in firefox_browser.find_elements(By.CLASS_NAME,'nav nav-list'):
        #    firefox_images.append(img.get_attribute('src'))

        # Add the scraped data to the data list
        data.append([link])

else:
    # Find all of the data you want to scrape using the appropriate tags and classes
    # For example, to scrape all of the links and images on the page:
    links = [a["href"] for a in soup.find_all("a", href=True)]
    #images = [img.get('src') for img in soup.find_all('img')]

    # Add the scraped data to the data list
    data = []
    for link in links:
        data.append([link])



# Write the scraped data to a text file
#with open('results.txt', 'r', newline='') as file:
    #file.write(link.text)
    #writer = file.write(str(data))
    #writer.writerow(['Scrawled Page Links'])
    #for row in data:
    #    writer.writerow(row)

# Write the scraped data to a csv file

with open('results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Scrawled Page Links'])
    for row in data:
        writer.writerow(row)

# Close the browser windows
firefox_browser.quit()
#chrome_browser.quit()
time.sleep(1)
print('\nScrawl successfully completed.\n')
time.sleep(1)
print('You can find the scrawled data in results.csv file.\n')

