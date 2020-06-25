import time, json, unittest, time, re, sys, pandas as pd
from datetime import datetime
import os #enviroment variable
import smtplib #Import smtplib for the actual sending function
from email.message import EmailMessage # for building mail's messages

from dateutil import parser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions  
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager #error check stackoverflow



'''#scrolling
def scrollDown(driver, value):
    driver.execute_script("window.scrollBy(0,"+str(value)+")")'''

def searchProduct(product):
    #load Amazon home page
    driver.get(url)
    time.sleep(5)
    try:
        #search bar
        search = driver.find_element_by_id('twotabsearchtextbox')
        search.send_keys(product)
        search.send_keys(Keys.RETURN)
        #retrieve all prices in loaded page
        #TODO: click su primo elemento e recupera prezzo da quella page
        productsPrice = driver.find_elements_by_class_name('a-price-whole')
        totalPrice = productsPrice[0].get_attribute('innerHTML')
        print('Total price: ',totalPrice) #searched product's price
        #transform price's string into float
        price = float(totalPrice.replace(',','.'))
        return price
    except IndexError as i:
        print(i)

def sendMail(receiver):
    #build message
    msg = EmailMessage()
    msg['Subject'] = "Hey! Product's price dropped!"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = receiver
    msg.set_content(product,' price dropped ! Check this out')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        try:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("\nMail sent")
            mailSent = True
        except Exception as e:
            print(e)
            mailSent = False
    #control check for sending mail
    return mailSent

        

#WebDriver Configuration
options = Options()
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

url = 'https://www.amazon.it/'
urlAuthentication = 'https://www.amazon.it/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.it%2F%3Fref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=itflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&'
senderAddress = ''
receiverAddress = ''

#address and password are saved as environment variable (find it at .zshrc)
EMAIL_PASSWORD = os.environ['PASSWORD_MAIL']
EMAIL_ADDRESS = os.environ['ADDRESS_MAIL']
# migliorare caricando la pagina delle liste, dare la possibilità di selezionarne una per poi scraping
# aggiungere "cronologia" prezzi (ogni volta che si esegue il check del prezzo salvare data e ora in un df?)
prices = []
product = 'amazon fire stick'

#initialize df
#TODO: check if file exists before reading it
df = pd.read_csv('history.csv', delimiter = ',')
print(df)

#start scraping
try:
    #productToSearch = input('Insert product to seach: ')
    productsPrice = searchProduct(product)
    print(productsPrice)
    #check price
    if productsPrice < 30:
        print("#####################################\n######### PRICE DROPPED ##########\n#####################################")
        mailSent = sendMail('mattia.crispino@gmail.com')
        #TODO: building dataFrame
    else:
        mailSent = False
    time.sleep(2)
    
    #save current date
    date = datetime.now().strftime('%d-%m-%Y %H:%M:%S') 
    #insert data to df
    new_row = {'date': date, 'product': product, 'price':productsPrice, 'mail_sent':mailSent}
    historyDF = df.append(new_row,ignore_index=True)
    #export df to csv
    historyDF.to_csv('history.csv', header=True, index=False)
    driver.quit()


   
except Exception as e:
    print("exception found: ",e)
    driver.quit()
