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
driver.fullscreen_window()

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


def getHotelNameAndLink(url:str):
    try:
        driver.get(url)
    except:
        print('error while loading page')
        return None 
    anchor=driver.find_element(by=By.CLASS_NAME,value='soom-name')
    hotelName = anchor.find_element(by=By.CSS_SELECTOR,value='span').text
    return (anchor.get_attribute(name='href'),hotelName)


def getAHotel(url):
    driver.get(url)
    for btn in driver.find_elements(by=By.TAG_NAME, value='button'):
        try:
            if 'view all photos'.lower() == btn.find_element(by=By.CSS_SELECTOR,value='.Iqt3-button-content').text.lower():
                btn.click()
                labelButtons = driver.find_element(by=By.CLASS_NAME,value='DTct-categories-container').find_elements(by=By.TAG_NAME, value='button')
                buttonWithLabel = [(button.find_element(by=By.CSS_SELECTOR, value='div div div').text.rstrip(string.digits), button) for button in labelButtons]
                return buttonWithLabel[1:]
        except:
            print('View all button not found')
        
    # for button in labelButtons:
 # take tuple list of button and label and return a dictionary containing label and corresponding image list
 # dict={
 # 'label1': [img1,img2],
 # 'label-2': [img1,img2,img3]  
 # }      
def getImageWithLabel(buttonWithLabel:list)-> dict:
    obj={}
    for button in buttonWithLabel:
        # time.sleep(2)
        print(button[0])
        label = button[0].split(' ')[0]
        try:
            button[1].click()
        except:
            print('button is not clickable')
            print(button[1])
            continue
        images = driver.find_elements(by=By.CSS_SELECTOR, value='.ZVFD-dots-container img')
        if len(images)>1:
            for image in images:
                link = image.get_attribute('src')
                print(link)
                if link != None:
                    try:
                        obj[button[0]]+= [link]
                    except KeyError:
                        obj[button[0]] = [link]
                
        else:
            image = driver.find_element(by=By.CSS_SELECTOR, value=f'img[alt*={label}]').get_attribute('src')
            print(image)
            obj[button[0]] = [image]
    return obj


#program start executing from here
def main():
    hotelName = ''
    dest=getDestinationLink('kolkata')
    hotel=getHotelNameAndLink(dest)
    hotelName=hotel[1]
    hotelUrl=hotel[0]
    image=getImageWithLabel(getAHotel(hotelUrl))
    
    print(image)
    
main()