import requests
from bs4 import BeautifulSoup
import requests
from twilio.rest import Client
import time
from variables import * #import your variables from variables.py
import html2text

#variables
#get page url
url = input("url of website: ")
#get page content
client = Client(account_sid, auth_token)
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
newtext = str(soup)
web_text = html2text.html2text(newtext)
#print page content
print("text from page: \n" + str(web_text))
#get operation type
op_type = input("look for word [w] or changes [c]?: ")
#get time between checks
time_between_checks = int(input("time between checks (seconds): "))
if(time_between_checks < 10):
    print("value too low, defaulting to 15 seconds")
    time_between_checks = 15
amount_of_checks = int(input("times to check: "))
#get whether to cancell process after success
cancel_after_success = input("cancel process after a successful check? [Y/N] recommend Y: ")
if(cancel_after_success == 'Y' or cancel_after_success == 'y'):
    cancel_after_success = True
elif(cancel_after_success == 'N' or cancel_after_success == 'n'):
    cancel_after_success = False
else:
    print("input not recognized")


#look for word function
#send messages if the input word is found in the page text
def look_for_word():
    #count checks to break if they exceed the specified amount
    count_checks = 0
    #get the actual word to check for
    #this is essentially an over-complicated, under-powered ctrl+F
    word_to_find = input("word to find: ")
    #start the main checking process
    while True:
        #increment the number of checks
        count_checks += 1
        print("Checks: " + str(count_checks))
        #check if the word is in the page content
        if(word_to_find in web_text):
            #send the message saying the word was found
            client.messages.create(body="Word '" + word_to_find + "' found in page",to=my_phone_number,from_=twilio_phone_number)
            #cancel the process if the user sepcified to
            if(cancel_after_success):
                print("sent message, process cancelled")
                break
            else:
                print("sent message, process still running")
        #break if the count is greater than the specified amount
        if(count_checks >= amount_of_checks):
            break
        time.sleep(time_between_checks)


#look for changes function
#send a message if the content of a page has changed since the script ran
def look_for_changes():
    #get original page content
    client = Client(account_sid, auth_token)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    newtext = str(soup)
    web_text = html2text.html2text(newtext)
    #count checks to break if they exceed the specified amount
    count_checks = 0
    #start the main checking process
    while True:
        #increment count of checks
        count_checks += 1
        print("Checks: " + str(count_checks))
        #get page content since original declaration
        page_new = requests.get(url)
        soup_new = BeautifulSoup(page_new.content, 'html.parser')
        newtext_new = str(soup_new)
        web_text_new = html2text.html2text(newtext_new)
        #check for changes between original content and new content
        if(web_text_new != web_text):
            #send the message if changes were made
            client.messages.create(body="Page has changed since last check",to=my_phone_number,from_=twilio_phone_number)
            #cancel the process if the user specified it
            if(cancel_after_success):
                print("sent message, process cancelled")
                break
            else:
                if(count_checks >= amount_of_checks):
                    print("max checks exceeded, process cancelled")
                    break
                else:
                    print("sent message, process still running")
                    time.sleep(time_between_checks)
                    continue
        #continue checking process
        else:
            #cancel the process if enough changes were made
            if(count_checks >= amount_of_checks):
                print("max checks exceeded, process cancelled")
                break
            #re-declare original page content
            #we don't want to check against the first original content, we want to check for changes between each check
            #if no changes were made, it shouldn't matter, and if they were, it also doesn't matter
            #this doesn't seem to be working
            #the function still bases changes on the first original content
            client = Client(account_sid, auth_token)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            newtext = str(soup)
            web_text = html2text.html2text(newtext)
            #wait for the specified amount of time
            time.sleep(time_between_checks)
            #continue the check
            continue
            

#call function
#run the function that the user specifies
if(op_type == 'w' or op_type == 'W'):
    look_for_word()
elif(op_type == 'c' or op_type == 'C'):
    look_for_changes()
    