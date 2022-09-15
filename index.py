from xml.dom.minidom import Element
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import string
option = Options()
option.headless=False
service = Service(executable_path="/home/w3e103/web_drivers/geckodriver")
driver = webdriver.Firefox(service=service,options=option)


# #strip number from string
# def stripNumber(label:str):
#     return label.rstrip(string.digits)
#get a link for given destination
def getDestinationLink(destination:str):
    driver.get('https://www.kayak.co.in/?ispredir=true')
    elements= driver.find_elements(by=By.CLASS_NAME,value='P_Ok-wrapper')
    for element in elements:
        place=element.find_element(by=By.CLASS_NAME, value='P_Ok-title').text
        if(place.lower() == destination.lower()):
            anchor= element.find_element(by=By.CSS_SELECTOR, value='.P_Ok-header-links span:last-child a')
    return anchor.get_attribute(name='href')


def getHotelNameAndLink(url):
    driver.get(url)
    anchor=driver.find_element(by=By.CLASS_NAME,value='soom-name')
    hotelName = anchor.find_element(by=By.CSS_SELECTOR,value='span').text
    return (anchor.get_attribute(name='href'),hotelName)


def getAHotel(url):
    driver.get(url)
    for btn in driver.find_elements(by=By.TAG_NAME, value='button'):
        try:
            if 'view all photos'.lower() == btn.find_element(by=By.CSS_SELECTOR,value='.Iqt3-button-content').text.lower():
                btn.click()
        except:
            pass
    labelButtons = driver.find_element(by=By.CLASS_NAME,value='DTct-categories-container').find_elements(by=By.TAG_NAME, value='button')
    buttonWithLabel = [(button.find_element(by=By.CSS_SELECTOR, value='div div div').text.rstrip(string.digits), button) for button in labelButtons]
    # for button in labelButtons:
    return buttonWithLabel[1:]
        
def getImageWithLabel(buttonWithLabel):
    obj={}
    for button in buttonWithLabel:
        time.sleep(5)
        print(button[0])
        button[1].click()
        for image in driver.find_elements(by=By.CSS_SELECTOR, value=f'img[alt={button[0]}]'):
            # print(image.get_attribute('src'))
            obj[button[0]]
def main():
    hotelName = ''
    dest=getDestinationLink('hyderabad')
    hotel=getHotelNameAndLink(dest)
    hotelName=hotel[1]
    hotelUrl=hotel[0]
    getImageWithLabel(getAHotel(hotelUrl))
    
main()