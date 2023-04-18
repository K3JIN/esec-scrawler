from telegram._update import Update
from telegram.ext import (Application,CommandHandler,ContextTypes,ConversationHandler,MessageHandler,filters,CallbackContext, Defaults)
import telegram
import csv, io
import subprocess
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import time
import logging


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

SURL, URLD, UNKOWN, CURL= range(4)

m_start = "\n\nWelcome to Esec Scrawler Bot (ESB). This bot is created"\
"to help you scrape and crawl websites. Happy hacking....\n\n"\
"use /surl to start scrawler prompt 🤖\n\n"\
"use /help to see available commands ✍️\n\n"

m_help = "\n\nYou can use following commands:\n\n"\
"/start : Initializes the bot and displays welcome message.\n\n"\
"/surl : Starts the scralwer for exploration 🌐\n\n"


async def start (update: Update, context: CallbackContext,):
    await update.message.reply_text(text=m_start)
    
    
async def help (update: Update, context: CallbackContext):
    await update.message.reply_text(text=m_help)	
    
async def unknown (update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)
  
  
async def unknown_text (update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Sorry I can't recognize what you said '%s'" % update.message.text)
    
# Add a function to store input from user and and paste it on scraper.py

async def surl (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Scrawler started. Enter the URL you wish to scrape."""
    await update.message.reply_text('Scrawler started 🤖\nEnter the 🔗 URL you wish to scrape.')

    return URLD

async def scrape(update: Update, context: CallbackContext) -> None:
    firefox_browser = webdriver.Firefox()
    url = update.message.text
    await update.message.reply_text(f"Scrawling 🔗 \n {url.lower()} sit tight. \n I will send you the csv file after scrawling is completed.")
    firefox_browser.get(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
    #chrome_browser.find_element(By.XPATH,'xpath')
       #firefox_browser.find_element(By.XPATH,'xpath')
       firefox_browser.find_element(By.TAG_NAME,'a')  
       is_dynamic = True
    except NoSuchElementException:
       is_dynamic = False

    if  is_dynamic:
    # Used Selenium to interact with the page and find all available of the links
     links = []
    #for link in chrome_browser.find_elements(By.TAG_NAME,'a'):
        #links.append(link.get_attribute('href'))
     for link in firefox_browser.find_elements(By.TAG_NAME,'a'):
       links.append(link.get_attribute('href'))

     data = []
     for link in links:
        #chrome_browser.get(link)
           firefox_browser.get(link)
    
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
    # Add your scraping logic here
    
    
    with open(r'data.csv'.encode('utf-8'), 'w') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    await context.bot.send_document(chat_id=update.effective_chat.id, document=open('data.csv', 'rb'))
    firefox_browser.quit()
    await update.message.reply_text("Scrawl successfully completed 🎉. Here is your csv file.\n happy to help 😊 .\n Use /surl to scrawl a new 🔗 URL")
    return URLD
    
#async def regular_choice(update: Update, context: CallbackContext) -> str:
#    """Ask the user for info about the selected predefined choice."""
#    slink = update.message.chat.id
#    slink = update.message.text
#    context.user_data["slink"] = slink
#    await update.message.reply_text(f"Scrawling\n 🔗 {slink.lower()} sit tight.\n I will send you the csv file after scrawling is completed.")
#    #os.system("python3 scraper.py")
#    subprocess.call("python3 scraper.py", shell=True)
#    return CURL

class pass_link:
    async def store_link(update: Update, context: CallbackContext) -> str:
     slink = update.message.chat.id
     slink = update.message.text
     context.user_data["slink"] = slink

	#Conversation handler with states 
def main() -> None:

    """Run the bot."""

    # Create the Application and pass it your bot's token.

    application = Application.builder().token("5879413008:AAESp3YA670spXhfex3PWWNIIyOtPMpowjU").read_timeout(90).write_timeout(90).build()

    conv_handler = ConversationHandler(
entry_points=[CommandHandler("start", start),CommandHandler("surl", surl),CommandHandler("help", help)],
states={
SURL: [MessageHandler(filters.Regex('surl'), surl)],
URLD: [MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("surl")), scrape)],
UNKOWN: [MessageHandler(filters.TEXT, unknown)],
CURL: [MessageHandler(filters.TEXT & ~ filters.COMMAND, pass_link)],
},
fallbacks=[MessageHandler(filters.Regex('surl'), surl)],
)
    application.add_handler(conv_handler)
    
# Run the bot until the user presses Ctrl-C

    application.run_polling()
    
if __name__ == "__main__":

    main()