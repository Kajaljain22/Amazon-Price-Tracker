# Python App to track prices of Amazon Product
import requests
from bs4 import BeautifulSoup
import smtplib    #Simple Mail Transfer Protocol Library (for sending mails)
import time       #for setting delays in a while(True) loop

URL = 'https://www.amazon.in/Amazon-FireTVStick-Alexa-Voice-Remote-Streaming-Player/dp/B0791YHVMK/ref=sr_1_1?crid=17203M5F873P3&dchild=1&keywords=amazon+fire+stick+tv&qid=1589970278&sprefix=amazon+fire%2Caps%2C491&sr=8-1'

headers = {"User-Agent" : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'}
# got headers value by searching "my user agent" on google

def convert(s):
    intPrice=""
    for i in s:
        if i.isdigit():
            intPrice+=i
        if i=='.':
            break
    
    return float(intPrice)



def check_price():
    page = requests.get(URL, headers = headers)

    soup1 = BeautifulSoup(page.content, 'html.parser')
    soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

    title = soup2.find(id="productTitle").get_text()
    #due to the fact that amazon keeps changing its js part, this line sometimes will give none keep running the program 3-4 times, it wil work
    print(title.strip())

    price = soup2.find(id="priceblock_ourprice").get_text()          #price is string 
    #print(price)

    converted_price = convert(price)
    # print(converted_price)

    if(converted_price <= 2500.0):
        send_mail()

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587  )
    server.ehlo() #builds connection b/w 2 mail servers
    server.starttls() #for encryption
    server.ehlo()
     
    server.login('kajalj256@gmail.com', 'pggwdzcqotaxwuvv')

    subject ="Price of Amazon Fire TV Stick fell down!"

    body = "Check the amazon link :: https://www.amazon.in/Amazon-FireTVStick-Alexa-Voice-Remote-Streaming-Player/dp/B0791YHVMK/ref=sr_1_1?crid=17203M5F873P3&dchild=1&keywords=amazon+fire+stick+tv&qid=1589970278&sprefix=amazon+fire%2Caps%2C491&sr=8-1"

    msg =f"Subject: {subject}\n\n{body}"

    server.sendmail(
         'kajalj256@gmail.com',
         'usha.jain03@gmail.com',
         msg
    )

    print("Email Sent!")

    server.quit()
     

check_price()

# while(True):
#     check_price()
#     time.sleep(24*3600) #to check once a day