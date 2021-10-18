from bs4 import BeautifulSoup # for parsing html
import requests # for getting the website
from twilio.rest import Client # for sending the text
import time # for delays
from variables import * # personal information
import html2text # extra

# get variables
count = 0 # for counting checks
url = input('url: ') # get url
interval = int(input('interval [seconds]: ')) # get delay between checks
if(interval <= 10): # failsafe so you don't DDOS the site
    print('too low, defaulting to 15')
    interval = 15

def send_message(): # declare function to send message
    client = Client(account_sid, auth_token)
    client.messages.create(body='Page has changed',to=my_phone_number,from_=twilio_phone_number)

def scrape_site(): # decalre function to get text content from the website
    page = requests.get(url) # find and download the page
    soup = BeautifulSoup(page.content, 'html.parser') # parse the page using BS4
    text = str(soup) # convert to a string
    web_text = html2text.html2text(text) # use HTML2text to make it into text
    return(web_text) # return the final string

while True: # loop to check for changes
    text_original = scrape_site() # get original content
    time.sleep(interval) # delay
    text_updated = scrape_site() # get new content
    count += 1 # increment count
    print('check ' + str(count)) # print incremented count
    if(text_original != text_updated): # check if the strings are equal
        print('changed') # print that it changed
        send_message() # send the message
        continue # restart the loop