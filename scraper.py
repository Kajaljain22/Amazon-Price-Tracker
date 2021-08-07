# Python App to track prices of Amazon Product
import requests
from bs4 import BeautifulSoup
import smtplib    #Simple Mail Transfer Protocol Library (for sending mails)
import time       #for setting delays in a while(True) loop
from passw import *

URL = ""
name = ""
email_id = ""
budget = 2500
headers = {"User-Agent" : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'}
# got headers value by searching "my user agent" on google

def convert(s):
    intPrice = ""
    for i in s:
        if i.isdigit():
            intPrice+=i
        if i=='.':
            break
    
    return float(intPrice)


def check_price():

    if(URL == ""):
        return
    page = requests.get(URL, headers = headers)
    soup1 = BeautifulSoup(page.content, 'html.parser')
    soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

    title = soup2.find(id="productTitle").get_text()
    #due to the fact that amazon keeps changing its js part, this line sometimes will give none keep running the program 3-4 times, it wil work
    print(title.strip())

    price = soup2.find(id="priceblock_ourprice")   
    if(price == None):
        price = soup2.find(id="priceblock_dealprice")     
    if(price == None):
        price = soup2.find(id="priceblock_saleprice")
    if(price == None):
        print("Check ID for price")
        return
    # print(price)                              #price -> entire span division
    price = price.get_text()          
    # print(price)                                #price = price value 
    
    converted_price = convert(price)            #converting price from string to int
    # print(converted_price)

    if(converted_price <= budget):
        send_mail()

def send_mail():
    if(email_id == ""):
        return
    server = smtplib.SMTP('smtp.gmail.com', 587  )
    server.ehlo() #builds connection b/w 2 mail servers
    server.starttls() #for encryption
    server.ehlo()

    server.login(mail,pw)

    subject ="Price of " + name + " fell down!"
    body = "Check the amazon link :: " + URL
    msg =f"Subject: {subject}\n\n{body}"

    server.sendmail(
         mail,
         email_id,
         msg
    )

    print("Email Sent!")

    server.quit()
     

while(True):
    name = input("Enter name of your product ")
    URL = input("Enter the amazon link of the product you want to track! ")
    budget = int(input("What's your budget? "))
    email_id = input("Enter your email :: ")
    check_price()
    time.sleep(24*3600) #to check once a day
